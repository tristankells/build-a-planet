# Generic ASK SDK imports
from typing import Dict, Any, Union, List

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.connections import SendRequestDirective
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from translator.translator import Translator
from ask_sdk_core.utils import viewport

# Custom skill code
from alexa.intents import Intents
from alexa.intent_slots import Slots
from planet_story.planet_story import PlanetStory
from planet_story.solar_questions import Question
from alexa.assets import Assets
from alexa.device import Device

# Purchasing
from ask_sdk_model.services.monetization import EntitledState, InSkillProductsResponse, Error, InSkillProduct
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult
from planet_story.store import Store

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

sb = SkillBuilder()
planet_story: PlanetStory
device: Device

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
    """

    Get the In-skill product response from monetization service.

    """
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    return ms.get_in_skill_products(locale)


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
        planet_story.launch()
        planet_story.previous_speech_text = planet_story.speech_text

        # Cowboy mode check
        # in_skill_response = in_skill_product_response(handler_input)
        # if isinstance(in_skill_response, InSkillProductsResponse):
        #     entitled_prods = get_all_entitled_products(in_skill_response.in_skill_products)
        #     if entitled_prods:
        #         Store.cowboyMode = 'PURCHASED'
        #     else:
        #         Store.cowbodeMode = 'NO'

        if device.apl_support:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=_load_apl_document("./data/main.json")
                )
            )
        else:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt)
        return handler_input.response_builder.response


class WhatCanIBuyHandler(AbstractRequestHandler):
    """

    W H A T  C A N  I  B U Y

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.WHAT_CAN_IBUY)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        planet_story.what_can_i_buy()
        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=_load_apl_document("./data/main.json")
                )
            )
        else:
            return get_speak_ask_response()



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
        planet_story.learn_about_solar_systems()

        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response()


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
        planet_story.do_not_learn_about_solar_systems()

        return get_speak_ask_response()


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

        star_brightness = str(handler_input.request_envelope.request.intent.slots[Slots.BRIGHTNESS].value).lower()

        planet_story.set_star_brightness(star_brightness)

        apl_datasource = _load_apl_document("./data/main.json")

        if star_brightness == "red":
            planet_story.speech_text += Translator.Star.star_brightness_red
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_BRIGHTNESS
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_BRIGHTNESS
        if star_brightness == "blue":
            planet_story.speech_text += Translator.Star.star_brightness_blue
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_BRIGHTNESS
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_BRIGHTNESS
        if star_brightness == "yellow":
            planet_story.speech_text += Translator.Star.star_brightness_yellow
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_BRIGHTNESS
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_BRIGHTNESS

        # Ask next question
        planet_story.speech_text += (' ' + Translator.Star.star_size)

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support == True:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=apl_datasource
                )
            )
        else:
            return get_speak_ask_response()


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
        star_size = str(
            handler_input.request_envelope.request.intent.slots[Slots.STAR_SIZE].value).lower()

        planet_story.set_star_size(star_size)

        apl_datasource = _load_apl_document("./data/main.json")

        if planet_story.star.brightness == "blue":
            if star_size == "dwarf":
                planet_story.speech_text += Translator.Star.star_size_dwarf
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_DWARF
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_DWARF
            if star_size == "giant":
                planet_story.speech_text += Translator.Star.star_size_giant
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_GIANT
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_GIANT
            if star_size == "super":
                planet_story.speech_text += Translator.Star.star_size_super_giant
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_SUPER
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_SUPER
        elif planet_story.star.brightness == "red":
            if star_size == "dwarf":
                planet_story.speech_text += Translator.Star.star_size_dwarf
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_DWARF
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_DWARF
            if star_size == "giant":
                planet_story.speech_text += Translator.Star.star_size_giant
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_GIANT
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_GIANT
            if star_size == "super":
                planet_story.speech_text += Translator.Star.star_size_super_giant
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_SUPER
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_SUPER            
        elif planet_story.star.brightness == "yellow":
            if star_size == "dwarf":
                planet_story.speech_text += Translator.Star.star_size_dwarf
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_DWARF
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_DWARF
            if star_size == "giant":
                planet_story.speech_text += Translator.Star.star_size_giant
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_GIANT
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_GIANT
            if star_size == "super":
                planet_story.speech_text += Translator.Star.star_size_super_giant
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_SUPER
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_SUPER       

        planet_story.speech_text += (' ' + Translator.Star.star_age)

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support == True:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=apl_datasource
                )
            )
        else:
            return get_speak_ask_response()


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
        star_age = str(
            handler_input.request_envelope.request.intent.slots[Slots.AGE].value).lower()

        planet_story.set_star_age(star_age)

        apl_datasource = _load_apl_document("./data/main.json")

        if planet_story.star.brightness == "blue" and planet_story.star.size == "dwarf":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_DWARF_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_DWARF_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_DWARF_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_DWARF_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_DWARF_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_DWARF_OLD
        elif planet_story.star.brightness == "red" and planet_story.star.size == "dwarf":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_DWARF_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_DWARF_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_DWARF_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_DWARF_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_DWARF_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_DWARF_OLD
        elif planet_story.star.brightness == "yellow" and planet_story.star.size == "dwarf":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_DWARF_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_DWARF_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_DWARF_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_DWARF_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_DWARF_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_DWARF_OLD
        elif planet_story.star.brightness == "blue" and planet_story.star.size == "giant":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_GIANT_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_GIANT_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_GIANT_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_GIANT_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_GIANT_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_GIANT_OLD
        elif planet_story.star.brightness == "red" and planet_story.star.size == "giant":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_GIANT_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_GIANT_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_GIANT_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_GIANT_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_GIANT_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_GIANT_OLD
        elif planet_story.star.brightness == "yellow" and planet_story.star.size == "giant":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_GIANT_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_GIANT_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_GIANT_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_GIANT_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_GIANT_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_GIANT_OLD

        elif planet_story.star.brightness == "blue" and planet_story.star.size == "super":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_SUPER_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_SUPER_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_SUPER_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_SUPER_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_SUPER_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_SUPER_OLD
        elif planet_story.star.brightness == "red" and planet_story.star.size == "super":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_SUPER_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_SUPER_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_SUPER_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_SUPER_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.RED_SUPER_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.RED_SUPER_OLD
        elif planet_story.star.brightness == "yellow" and planet_story.star.size == "super":
            if star_age == "young":
                planet_story.speech_text += Translator.Star.star_age_young
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_SUPER_YOUNG
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_SUPER_YOUNG
            if star_age == "middle-aged":
                planet_story.speech_text += Translator.Star.star_age_middle
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_SUPER_MIDDLE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_SUPER_MIDDLE
            if star_age == "old":
                planet_story.speech_text += Translator.Star.star_age_old
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.YELLOW_SUPER_OLD
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_SUPER_OLD

        planet_story.speech_text += (' ' + Translator.Planet.planet_size)

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support == True:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=apl_datasource
                )
            )
        else:
            return get_speak_ask_response()


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
        planet_size = str(
            handler_input.request_envelope.request.intent.slots[Slots.PLANET_SIZE].value).lower()

        planet_story.set_planet_size(planet_size)

        apl_datasource = _load_apl_document("./data/main.json")

        if planet_size == "large":
            planet_story.speech_text += Translator.Planet.planet_size_large
            if planet_story.star.brightness == "blue" or planet_story.star.size == "super" or\
                    planet_story.star.age == "young":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_LARGE
            else:
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_LARGE

        if planet_size == "medium":
            planet_story.speech_text += Translator.Planet.planet_size_medium
            if planet_story.star.brightness == "blue" or planet_story.star.size == "super" or\
                    planet_story.star.age == "young":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_MEDIUM
            else:
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_MEDIUM

        if planet_size == "small":
            planet_story.speech_text += Translator.Planet.planet_size_small
            if planet_story.star.brightness == "blue" or planet_story.star.size == "super" or \
                    planet_story.star.age == "young":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_SMALL
            else:
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_SMALL
        
        planet_story.speech_text += (' ' + Translator.Planet.planet_distance)

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support == True:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=apl_datasource
                )
            )
        else:
            return get_speak_ask_response()


class PlanetDistanceHandler(AbstractRequestHandler):
    """

    P L A N E T   D I S T A N C E

    """
    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_DISTANCE)(handler_input) \
               and planet_story.current_question == Question.Planet.DISTANCE

    def handle(self, handler_input):

        planet_distance = str(
            handler_input.request_envelope.request.intent.slots[Slots.DISTANCE].value).lower()

        planet_story.set_planet_distance(planet_distance)

        apl_datasource = _load_apl_document("./data/main.json")

        if planet_distance == "near":
            planet_story.speech_text += Translator.Planet.planet_distance_neighbouring
            if planet_story.star.brightness == "yellow":
                if planet_story.planet.size == "large" or planet_story.star.brightness == "blue" or\
                        planet_story.star.size == "super" or planet_story.star.size == "giant" or planet_story.star.age == "young":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_LARGE
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_LARGE
                elif planet_story.planet.size == "medium" or planet_story.star.brightness == "blue" or \
                        planet_story.star.size == "super" or planet_story.star.size == "giant" or\
                        planet_story.star.age == "young":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_MEDIUM   
                elif planet_story.planet.size == "small" or planet_story.star.brightness == "blue" or\
                        planet_story.star.size == "super" or planet_story.star.size == "giant"  or \
                        planet_story.star.age == "young":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_SMALL
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_SMALL
            elif (planet_story.star.brightness == "red" and planet_story.star.size == "super") or\
                    planet_story.star.brightness == "blue" or planet_story.star.size == "super" or \
                    planet_story.star.size == "giant"  or planet_story.star.age == "young":
                if planet_story.planet.size == "large":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_LARGE
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_LARGE
                elif planet_story.planet.size == "medium":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_MEDIUM
                elif planet_story.planet.size == "small":
                    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.FIREBALL_SMALL
                    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.FIREBALL_SMALL
        elif planet_distance == "midway":
            planet_story.speech_text += Translator.Planet.planet_distance_near
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_SMALL
        elif planet_distance == "far":
            planet_story.speech_text += Translator.Planet.planet_distance_far
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.ICEBALL_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.ICEBALL_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.ICEBALL_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.ICEBALL_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.ICEBALL_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.ICEBALL_SMALL
                
        planet_story.speech_text += ' ' + Translator.Planet.planet_age

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support == True:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=apl_datasource
                )
            )
        else:
            return get_speak_ask_response()


class PlanetAgeIntentHandler(AbstractRequestHandler):
    """

    P L A N E T  A G E

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.AGE)(handler_input) and planet_story.current_question == Question.Planet.AGE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        planet_age = str(
            handler_input.request_envelope.request.intent.slots[Slots.AGE].value).lower()

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
            elif (planet_story.star.brightness == "red" and planet_story.star.size == "super") or\
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
            planet_story.speech_text += Translator.Planet.planet_age_young
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.GENERIC_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.GENERIC_SMALL
        if planet_age == "middle-aged":
            planet_story.speech_text += Translator.Planet.planet_age_middleaged
        if planet_age == "old":
            planet_story.speech_text += Translator.Planet.planet_age_old

        # Now solar system is built, test if planet is habitable
        planet_story.test_if_planet_habitable()

        if planet_story.is_planet_habitable:
            # Change to earth pic
            if planet_story.planet.size == "large":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.EARTH_LARGE
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.EARTH_LARGE
            elif planet_story.planet.size == "medium":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.EARTH_MEDIUM
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.EARTH_MEDIUM
            elif planet_story.planet.size == "small":
                apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.EARTH_SMALL
                apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.EARTH_SMALL

        # else:
        #     # Don't change to earth

        planet_story.speech_text += (' ' + Translator.EndGame.game_end)

        planet_story.previous_speech_text = planet_story.speech_text

        if device.apl_support == True:
            handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt).add_directive(
                RenderDocumentDirective(
                    token="pagerToken",
                    document=_load_apl_document("./templates/main.json"),
                    datasources=apl_datasource
                )
            )
        else:
            return get_speak_ask_response()


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
        planet_story.review_solar_system()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response()


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
        planet_story.do_not_review_solar_system()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response()


class PurchaseHandler(AbstractRequestHandler):
    """

    P U R C H A S E

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.YES)(handler_input) \
               or is_intent_name(Intents.NO)(handler_input) \
               and planet_story.current_question == Question.PURCHASE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.add_directive(
                        SendRequestDirective(
                            name="Upsell",
                            payload={
                                "InSkillProduct": {
                                    "productId": 'amzn1.adg.product.9881949f-e95d-4e03-a790-885468e8b080',
                                },
                                "upsellMessage": 'do you want to purchase test...',
                            },
                            token="correlationToken")
                    ).response


class UpsellResponseHandler(AbstractRequestHandler):
    """

    UPSELL RESPONSE

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Upsell")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        all_facts = ""

        if handler_input.request_envelope.request.status.code == "200":
            if handler_input.request_envelope.request.payload.get("purchaseResult") == PurchaseResult.DECLINED.value:
                speech = ("Ok. Here's a random fact: {} {}".format(
                    get_random_from_list(all_facts),
                    get_random_yes_no_question()))
                reprompt = get_random_yes_no_question()
                return handler_input.response_builder.speak(speech).ask(
                    reprompt).response
        else:
            return handler_input.response_builder.speak(
                "There was an error handling your Upsell request. Please try again or contact us for help.").response


def get_random_from_list(all_facts):
    raise NotImplementedError


def get_random_yes_no_question():
    raise NotImplementedError


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
        planet_story.play_again()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response()


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
        planet_story.exit_skill()
        planet_story.previous_speech_text = planet_story.speech_text

        return get_speak_ask_response()


class HelpIntentHandler(AbstractRequestHandler):
    """

    H E L P

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.HELP)(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
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
        planet_story.repeat()
        return get_speak_ask_response(handler_input)


def get_speak_ask_response(handler_input):
    handler_input.response_builder.speak(planet_story.speech_text).ask(planet_story.reprompt)
    return handler_input.response_builder.response


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
        planet_story.toggle_voice()

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
        # any cleanup logic goes here

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
        property_question_dict = {
            Question.Star.BRIGHTNESS:
                Translator.Star.star_brightness_other
            ,
            Question.Star.SIZE:
                Translator.Star.star_size_other
            ,
            Question.Star.AGE:
                Translator.Star.star_age_other
            ,
            Question.Planet.DISTANCE:
                Translator.Planet.planet_distance_other
            ,
            Question.Planet.SIZE:
                Translator.Planet.planet_size_other
            ,
            Question.Planet.AGE:
                Translator.Planet.planet_age_other
        }

        speech_text = property_question_dict.get(planet_story.current_question)
        handler_input.response_builder.speak(speech_text).ask(planet_story.reprompt)
        return handler_input.response_builder.response


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

        speech = "Sorry, I didn't get it. Can you please say it again!!"

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


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
sb.add_request_handler(WhatCanIBuyHandler())
sb.add_request_handler(PurchaseHandler())
sb.add_request_handler(ToggleVoiceHandler())
sb.add_request_handler(UpsellResponseHandler())


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
