# Generic ASK SDK imports
from typing import Dict, Any

# from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk.standard import StandardSkillBuilder

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.connections import SendRequestDirective
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_core.utils import viewport

# Custom skill code
from alexa.intents import Intents
from alexa.slots import Slots
from planet_story.planet_story import PlanetStory
from planet_story.solar_questions import Question
from planet_story.narrator import Narrator
from alexa.assets import Assets
from alexa.device import Device
from logger import Logger
from apl import planet_apl, star_apl

# Purchasing
from ask_sdk_model.services.monetization import EntitledState, InSkillProductsResponse
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult

# For APL
import json
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective)

# Const strings

STAR = 'star'
PLANET = 'planet'

BRIGHTNESS = 'brightness'
SIZE = 'size'
DISTANCE = 'distance'

SKILL_TITLE = 'Build A Planet'

# sb = SkillBuilder()

sb = StandardSkillBuilder()
planet_story: PlanetStory
device: Device


def get_slot_value_from_handler(handler_input, slot_name):
    return str(
        handler_input.request_envelope.request.intent.slots[slot_name].resolutions.resolutions_per_authority[
            0].values[0].value.name
    ).lower()


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


def get_all_entitled_products(in_skill_product_list):
    """Get list of in-skill products in ENTITLED state."""
    entitled_product_list = [
        l for l in in_skill_product_list if (
                l.entitled == EntitledState.ENTITLED)]
    return entitled_product_list


def in_skill_product_response(handler_input):
    """Get the In-skill product response from monetization service."""
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    return ms.get_in_skill_products(locale)

def get_product_list(entitled_products_list):
    product_names = [item.name for item in entitled_products_list]
    if len(product_names) > 1:
        speech = " and ".join(
            [", ".join(product_names[:-1]), product_names[-1]])
    else:
        speech = ", ".join(product_names)
    return speech

def get_speak_ask_response(handler_input):
    handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt)
    return handler_input.response_builder.response


def get_apl_response(handler_input, datasource):
    if isinstance(datasource, str):
        handler_input.response_builder.speak(
            planet_story.speech_text
        ).ask(
            planet_story.reprompt
        ).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=_load_apl_document(datasource)
            )
        )
    else:
        handler_input.response_builder.speak(
            planet_story.speech_text
        ).ask(
            planet_story.reprompt
        ).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=datasource
            )
        )
    return handler_input.response_builder.response


# TODO: Fix rest of audio
# TODO: Make clean ending
# TODO: Add other properties for planet and star
# TODO: Check that re-prompts work correctly, eg... play same question back
# TODO: Adding tracking of long explanations so players doesnt have to listen to it every time
# TODO: Look into refactoring decision tree stuff / finding apl files stuff


class SetupRequestInterceptor(AbstractRequestInterceptor):
    """
    Request interceptors are invoked immediately before execution of the request handler for an incoming request.
    """

    def process(self, handler_input):
        print("Request received: {}".format(
            handler_input.request_envelope.request))
        print("Entire request envelope: {}".format(
            viewport.get_viewport_profile(handler_input.request_envelope)))
        global planet_story
        global device

        device = Device(viewport.get_viewport_profile(handler_input.request_envelope))
        session_attributes = handler_input.attributes_manager.session_attributes
        planet_story = PlanetStory(session_attributes)


class LaunchRequestHandler(AbstractRequestHandler):
    """

    L A U N C H

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'LaunchRequestHandler handle() called.')

        planet_story.launch()
        planet_story.previous_speech_text = planet_story.speech_text

        # Check purchased products
        in_skill_response = in_skill_product_response(handler_input)
        if isinstance(in_skill_response, InSkillProductsResponse):
            entitled_prods = get_all_entitled_products(in_skill_response.in_skill_products)
            # if spacecowboy in entitled_prods
            if entitled_prods:
                planet_story.cowboy_unlocked = True

        if device.apl_support:
            if planet_story.narrator == Narrator.cowboy:
                return get_apl_response(handler_input, datasource='./data/main_space_cowboy.json')
            else:
                return get_apl_response(handler_input, datasource='./data/main.json')
        else:
            return get_speak_ask_response(handler_input)


class WhatCanIBuyHandler(AbstractRequestHandler):
    """

    W H A T  C A N  I  B U Y

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.WHAT_CAN_I_BUY)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'WhatCanIBuyHandler handle() called.')

        planet_story.what_can_i_buy()
        planet_story.previous_speech_text = planet_story.speech_text

        planet_story.speech_text += get_question_speech_text(planet_story.current_question)

        if device.apl_support:
            return get_apl_response(handler_input, datasource='./data/main.json')
        else:
            return get_speak_ask_response(handler_input)


class YesLearnMoreIntentHandler(AbstractRequestHandler):
    """

    Y E S   -   L E A R N   M O R E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.YES)(handler_input) \
               and planet_story.current_question == Question.Star.BRIGHTNESS

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'YesLearnMoreIntentHandler handle() called.')

        planet_story.learn_about_solar_systems()

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support:
            return get_apl_response(handler_input, datasource='./data/main.json')
        else:
            return get_speak_ask_response(handler_input)


class NoLearnMoreIntentHandler(AbstractRequestHandler):
    """

    N O   -   L E A R N   M O R E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.NO)(handler_input) \
               and planet_story.current_question == Question.Star.BRIGHTNESS

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'NoLearnMoreIntentHandler handle() called.')

        planet_story.do_not_learn_about_solar_systems()

        return get_speak_ask_response(handler_input)


# region Star Handlers


class StarBrightnessIntentHandler(AbstractRequestHandler):
    """

    S T A R   B R I G H T N E S S

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.STAR_BRIGHTNESS)(handler_input) \
               and planet_story.current_question == Question.Star.BRIGHTNESS

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'StarBrightnessIntentHandler handle() called.')

        star_brightness = get_slot_value_from_handler(handler_input, slot_name=Slots.BRIGHTNESS)

        planet_story.set_star_brightness(star_brightness)

        if device.apl_support:
            apl_datasource = _load_apl_document("./data/main.json")
            apl_datasource = star_apl.get_image_star_brightness(apl_datasource, star_brightness=star_brightness)

            return get_apl_response(handler_input, datasource=apl_datasource)
        else:
            return get_speak_ask_response(handler_input)


class StarSizeIntentHandler(AbstractRequestHandler):
    """

    S T A R   S I Z E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.STAR_SIZE)(handler_input) and planet_story.current_question == \
               Question.Star.SIZE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'StarSizeIntentHandler handle() called.')

        star_size = get_slot_value_from_handler(handler_input, slot_name=Slots.STAR_SIZE)

        planet_story.set_star_size(star_size)

        if device.apl_support:
            apl_datasource = _load_apl_document("./data/main.json")

            apl_datasource = star_apl.get_image_star_size(
                apl_datasource,
                star_brightness=planet_story.star.brightness,
                star_size=star_size
            )

            return get_apl_response(handler_input, datasource=apl_datasource)
        else:
            return get_speak_ask_response(handler_input)


class StarAgeIntentHandler(AbstractRequestHandler):
    """

    S T A R   A G E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.AGE)(
            handler_input) and planet_story.current_question == Question.Star.AGE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'StarAgeIntentHandler handle() called.')

        star_age = get_slot_value_from_handler(handler_input, slot_name=Slots.AGE)

        planet_story.set_star_age(star_age)

        if device.apl_support:
            apl_datasource = _load_apl_document("./data/main.json")

            apl_datasource = star_apl.get_image_star_age(
                apl_datasource,
                star_brightness=planet_story.star.brightness,
                star_size=planet_story.star.size,
                star_age=star_age
            )

            return get_apl_response(handler_input, datasource=apl_datasource)
        else:
            return get_speak_ask_response(handler_input)

# endregion

# region Planet Handlers


class PlanetSizeHandler(AbstractRequestHandler):
    """

    P L A N E T   S I Z E

    """

    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_SIZE)(handler_input) \
               and planet_story.current_question == Question.Planet.SIZE

    def handle(self, handler_input):
        Logger.info(f'PlanetSizeHandler handle() called.')

        planet_size = get_slot_value_from_handler(handler_input, slot_name=Slots.PLANET_SIZE)

        planet_story.set_planet_size(planet_size)

        if device.apl_support:
            if device.apl_support:
                apl_datasource = _load_apl_document("./data/main.json")

                apl_datasource = planet_apl.get_image_based_on_planet_size(
                    apl_datasource,
                    planet_size,
                    star_brightness=planet_story.star.brightness,
                    star_size=planet_story.star.size,
                    star_age=planet_story.star.age
                )

                return get_apl_response(handler_input, datasource=apl_datasource)
        else:
            return get_speak_ask_response(handler_input)


class PlanetDistanceHandler(AbstractRequestHandler):
    """

    P L A N E T   D I S T A N C E

    """

    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_DISTANCE)(handler_input) \
               and planet_story.current_question == Question.Planet.DISTANCE

    def handle(self, handler_input):
        Logger.info(f'PlanetDistanceHandler handle() called.')

        planet_distance = get_slot_value_from_handler(handler_input, slot_name=Slots.DISTANCE)

        planet_story.set_planet_distance(planet_distance)

        if device.apl_support:
            if device.apl_support:
                apl_datasource = _load_apl_document("./data/main.json")

                apl_datasource = planet_apl.get_image_based_on_planet_distance(
                    apl_datasource,
                    planet_distance,
                    planet_size=planet_story.planet.size,
                    star_brightness=planet_story.star.brightness,
                    star_size=planet_story.star.size,
                    star_age=planet_story.star.age
                )

                return get_apl_response(handler_input, datasource=apl_datasource)
        else:
            return get_speak_ask_response(handler_input)


class PlanetAgeIntentHandler(AbstractRequestHandler):
    """

    P L A N E T  A G E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.AGE)(handler_input) and planet_story.current_question == Question.Planet.AGE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'PlanetAgeIntentHandler handle() called.')

        planet_age = get_slot_value_from_handler(handler_input, slot_name=Slots.AGE)

        planet_story.set_planet_age(planet_age)

        apl_datasource = _load_apl_document("./data/main.json")

        if planet_story.planet.distance == "near":
            if planet_story.star.brightness == "yellow":
                if planet_story.planet.size == "large" or planet_story.star.brightness == "blue" or \
                        planet_story.star.size == "super" or planet_story.star.age == "young":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_LARGE
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_LARGE
                elif planet_story.planet.size == "medium" or planet_story.star.brightness == "blue" or \
                        planet_story.star.size == "super" or planet_story.star.age == "young":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                elif planet_story.planet.size == "small" or planet_story.star.brightness == "blue" or \
                        planet_story.star.size == "super" or planet_story.star.age == "young":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_SMALL
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_SMALL
            elif (planet_story.star.brightness == "red" and planet_story.star.size == "super") or \
                    planet_story.star.brightness == "blue" or planet_story.star.size == "super" or planet_story.star.age == "young":
                if planet_story.planet.size == "large":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_LARGE
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_LARGE
                elif planet_story.planet.size == "medium":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                elif planet_story.planet.size == "small":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_SMALL
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_SMALL
        elif planet_story.planet.distance == "midway":
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_SMALL
        elif planet_story.planet.distance == "far":
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.ICEBALL_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.ICEBALL_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.ICEBALL_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.ICEBALL_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.ICEBALL_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.ICEBALL_SMALL

        if planet_age == "young":
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_SMALL

        if planet_story.is_planet_habitable:
            # Change to earth pic
            apl_datasource = planet_apl.get_image_habitable_planet(apl_datasource, planet_size=planet_story.planet.size)

        if device.apl_support:
            return get_apl_response(handler_input, datasource=apl_datasource)
        else:
            return get_speak_ask_response(handler_input)


# endregion




class YesReviewSolarSystem(AbstractRequestHandler):
    """

    Y E S   -   R E V I E W

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.YES)(handler_input) \
               and planet_story.current_question == Question.REVIEW

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'YesReviewSolarSystem handle() called.')

        planet_story.review_solar_system()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response(handler_input)


class NoReviewSolarSystem(AbstractRequestHandler):
    """

    N O   -   R E V I E W

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.NO)(handler_input) \
               and planet_story.current_question == Question.REVIEW

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'NoReviewSolarSystem handle() called.')

        planet_story.do_not_review_solar_system()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response(handler_input)


class BuyHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.BUY_SKILL_ITEM)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        planet_story.previous_speech_text = planet_story.speech_text

        product_name = get_slot_value_from_handler(handler_input, slot_name=Slots.PRODUCT)

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name="Buy",
                payload={
                    "InSkillProduct": {
                        "productId": 'amzn1.adg.product.9881949f-e95d-4e03-a790-885468e8b080'
                    }
                },
                token="correlationToken")
        ).response


class BuyResponseHandler(AbstractRequestHandler):
    """This handles the Connections.Response event after a buy occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Buy")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        in_skill_response = in_skill_product_response(handler_input)
        product_id = handler_input.request_envelope.request.payload.get("productId")

        if in_skill_response:
            if handler_input.request_envelope.request.status.code == "200":
                purchase_result = handler_input.request_envelope.request.payload.get(
                    "purchaseResult")
                if purchase_result == PurchaseResult.ACCEPTED.value:
                    planet_story.purchase_success()
                elif purchase_result in (
                        PurchaseResult.DECLINED.value,
                        PurchaseResult.ERROR.value,
                        PurchaseResult.NOT_ENTITLED.value):
                    planet_story.purchase_declined()
                elif purchase_result == PurchaseResult.ALREADY_PURCHASED.value:
                    planet_story.purchase_success()
                else: # Invalid purchase result value
                    planet_story.purchase_declined()
            else:
                planet_story.purchase_declined()

        planet_story.speech_text += get_question_speech_text(planet_story.current_question)

        if device.apl_support:
            return get_apl_response(handler_input, datasource='./data/main_space_cowboy.json')
        else:
            return get_speak_ask_response(handler_input)


class RefundPurchaseHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.REFUND_SKILL_ITEM)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        planet_story.previous_speech_text = planet_story.speech_text

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name="Cancel",
                payload={
                    "InSkillProduct": {
                        "productId": 'amzn1.adg.product.9881949f-e95d-4e03-a790-885468e8b080'
                    }
                },
                token="correlationToken")
        ).response


class YesPlayAgainHandler(AbstractRequestHandler):
    """

    Y E S   -   P L A Y   A G A I N

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.YES)(handler_input) \
               and planet_story.current_question == Question.PLAY_AGAIN

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'YesPlayAgainHandler handle() called.')

        planet_story.play_again()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response(handler_input)


class NoPlayAgainHandler(AbstractRequestHandler):
    """

    N O   -   P L A Y   A G A I N

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.NO)(handler_input) \
               and planet_story.current_question == Question.PLAY_AGAIN

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'NoPlayAgainHandler handle() called.')

        planet_story.exit_skill()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response(handler_input)


class HelpIntentHandler(AbstractRequestHandler):
    """

    H E L P

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.HELP)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'HelpIntentHandler handle() called.')

        planet_story.help()

        return get_speak_ask_response(handler_input)


class RepeatHandler(AbstractRequestHandler):
    """

    R E P E A T

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.REPEAT)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'RepeatHandler handle() called.')

        planet_story.repeat()

        return get_speak_ask_response(handler_input)


class CancelAndStopIntentHandler(AbstractRequestHandler):
    """

    C A N C E L   A N D    S T O P

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.CANCEL)(handler_input) \
               or is_intent_name(Intents.STOP)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'CancelAndStopIntentHandler handle() called.')

        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Goodbye!", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response


class ToggleVoiceHandler(AbstractRequestHandler):
    """

    T O G G L E   N A R R A T O R

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.TOGGLE_VOICE)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'ToggleVoiceHandler handle() called.')

        planet_story.toggle_voice()

        if device.apl_support:
            if planet_story.narrator == Narrator.cowboy and planet_story.current_question == Question.Star.BRIGHTNESS:
                return get_apl_response(handler_input, datasource='./data/main_space_cowboy.json')
            else:
                return get_apl_response(handler_input, datasource='./data/main.json')
        else:
            return get_speak_ask_response(handler_input)


class SessionEndedRequestHandler(AbstractRequestHandler):
    """

    S K I L L   E N D E D

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'SessionEndedRequestHandler handle() called.')

        return handler_input.response_builder.response


class FallbackHandler(AbstractRequestHandler):
    """

    F A L L B A C K

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        Logger.info(f'FallbackHandler handle() called.')

        planet_story.speech_text = get_fallback_question_speech_text(planet_story.previous_speech_text)

        return get_speak_ask_response(handler_input)


def get_fallback_question_speech_text(current_question):
    property_question_dict = {
        Question.Star.BRIGHTNESS:
            planet_story.translator.Star.star_brightness_other
        ,
        Question.Star.SIZE:
            planet_story.translator.Star.star_size_other
        ,
        Question.Star.AGE:
            planet_story.translator.Star.star_age_other
        ,
        Question.Planet.DISTANCE:
            planet_story.translator.Planet.planet_distance_other
        ,
        Question.Planet.SIZE:
            planet_story.translator.Planet.planet_size_other
        ,
        Question.Planet.AGE:
            planet_story.translator.Planet.planet_age_other
    }

    return property_question_dict.get(current_question)


def get_question_speech_text(current_question):
    property_question_dict = {
        Question.Star.BRIGHTNESS:
            planet_story.translator.Star.star_brightness
        ,
        Question.Star.SIZE:
            planet_story.translator.Star.star_size
        ,
        Question.Star.AGE:
            planet_story.translator.Star.star_age
        ,
        Question.Planet.DISTANCE:
            planet_story.translator.Planet.planet_distance
        ,
        Question.Planet.SIZE:
            planet_story.translator.Planet.planet_size
        ,
        Question.Planet.AGE:
            planet_story.translator.Planet.planet_age
    }

    return property_question_dict.get(current_question)


class AllExceptionHandler(AbstractExceptionHandler):
    """

    A L L   E X E C E P T I O N S

    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print('EXCEPTION: ' + str(exception))

        planet_story.speech_text = "Sorry, I didn't get it. Can you please say it again!!"

        return get_speak_ask_response(handler_input)


class SaveSessionAttributesResponseInterceptor(AbstractResponseInterceptor):
    """

    R E S P O N S E   I N T E R C E P T O R

    Response interceptors are invoked immediately after execution of the request handler for an incoming request.
    """

    def process(self, handler_input, response):
        print("Response generated: {}".format(response))
        print("Viewport detected: {}".format(device.apl_support))

        handler_input.attributes_manager.session_attributes = planet_story.get_session_variables()


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# region Store handlers
sb.add_request_handler(RefundPurchaseHandler())
sb.add_request_handler(WhatCanIBuyHandler())
sb.add_request_handler(BuyHandler())
sb.add_request_handler(BuyResponseHandler())
sb.add_request_handler(ToggleVoiceHandler())

# endregion

# region Custom handlers

# Star

sb.add_request_handler(StarBrightnessIntentHandler())
sb.add_request_handler(StarSizeIntentHandler())
sb.add_request_handler(StarAgeIntentHandler())

# Planets

sb.add_request_handler(PlanetDistanceHandler())
sb.add_request_handler(PlanetSizeHandler())
sb.add_request_handler(PlanetAgeIntentHandler())

# endregion

sb.add_request_handler(YesLearnMoreIntentHandler())
sb.add_request_handler(NoLearnMoreIntentHandler())

sb.add_request_handler(YesReviewSolarSystem())
sb.add_request_handler(NoReviewSolarSystem())

sb.add_request_handler(YesPlayAgainHandler())
sb.add_request_handler(NoPlayAgainHandler())

sb.add_request_handler(RepeatHandler())

sb.add_global_request_interceptor(SetupRequestInterceptor())

sb.add_global_response_interceptor(SaveSessionAttributesResponseInterceptor())

sb.add_exception_handler(AllExceptionHandler())

sb.add_request_handler(FallbackHandler())

lambda_handler = sb.lambda_handler()
