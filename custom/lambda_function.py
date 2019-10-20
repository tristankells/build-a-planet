# Generic ASK SDK imports
from typing import Dict, Any

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from translator.translator import Translator

# Custom skill code
from alexa_intents import Intents
from intent_slots import Slots
from planet_story.planet_story import PlanetStory
from planet_story.solar_questions import Question
from assets import Assets

# For APL
import json
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective,
    AutoPageCommand)

# Const strings

STAR = 'star'
PLANET = 'planet'

BRIGHTNESS = 'brightness'
SIZE = 'size'
DISTANCE = 'distance'

SKILL_TITLE = 'Build A Planet'

sb = SkillBuilder()
planet_story: PlanetStory


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)

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
        global planet_story

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

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=_load_apl_document("./data/main.json")
            )
        )
        return handler_input.response_builder.response


class YesLearnMoreIntentHandler(AbstractRequestHandler):
    """

    Y E S   -   L E A R N   M O R E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print("YesLearnMoreIntent Can handler has been CALLED")
        return is_intent_name(Intents.YES)(handler_input) \
               and planet_story.current_question == Question.Star.STAR_BRIGHTNESS

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("YesLearnMoreIntentHandler has been CALLED")
        planet_story.learn_about_solar_systems()

        apl_datasource = _load_apl_document("./data/main.json")

        apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_BRIGHTNESS

        handler_input.response_builder.speak(planet_story.speech_text)
        
        return handler_input.response_builder.response


# class NoLearnMoreIntentHandler(AbstractRequestHandler):
#     """

#     N O   -   L E A R N   M O R E

#     """

#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name(Intents.NO)(handler_input) \
#                and planet_story.current_question == Question.Star.STAR_BRIGHTNESS

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         print("NoLearnMoreIntentHandler has been CALLED")

#         planet_story.do_not_learn_about_solar_systems()

#         apl_datasource = _load_apl_document("./data/main.json")

#         apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.YELLOW_BRIGHTNESS

#         handler_input.response_builder.speak(planet_story.speech_text).add_directive(
#             RenderDocumentDirective(
#                 token="pagerToken",
#                 document=_load_apl_document("./templates/main.json"),
#                 datasources=apl_datasource
#             )
#         )

#         return handler_input.response_builder.response


# region Star Handlers


class StarBrightnessIntentHandler(AbstractRequestHandler):
    """

    S T A R   B R I G H T N E S S

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name(Intents.STAR_BRIGHTNESS)(handler_input) or is_intent_name(Intents.NO)(handler_input)) \
               and planet_story.current_question == Question.Star.STAR_BRIGHTNESS

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        star_brightness = str(handler_input.request_envelope.request.intent.slots[Slots.BRIGHTNESS].value).lower()

        planet_story.set_star_brightness(star_brightness)

        apl_datasource = _load_apl_document("./data/main.json")

        planet_story.speech_text = f'Your star brightness is {star_brightness}. '

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

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


class StarSizeIntentHandler(AbstractRequestHandler):
    """

    S T A R   S I Z E

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.STAR_SIZE)(handler_input) and planet_story.current_question ==\
               Question.Star.STAR_SIZE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        star_size = str(
            handler_input.request_envelope.request.intent.slots[Slots.STAR_SIZE].value).lower()

        planet_story.set_star_size(star_size)

        apl_datasource = _load_apl_document("./data/main.json")

        planet_story.speech_text = f'Your star size is {star_size}. '

        # If blue sun
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

        planet_story.speech_text += (' ' + Translator.Star.star_age)

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


class StarAgeIntentHandler(AbstractRequestHandler):
    """

    S T A R   A G E

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.AGE)(
            handler_input) and planet_story.current_question == Question.Star.STAR_AGE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        star_age = str(
            handler_input.request_envelope.request.intent.slots[Slots.AGE].value).lower()

        planet_story.set_star_age(star_age)

        apl_datasource = _load_apl_document("./data/main.json")

        planet_story.speech_text = f'Your star age is {star_age}. '

        # If blue sun
        if star_age == "young":
            planet_story.speech_text += Translator.Star.star_age_young
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_DWARF
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_DWARF
        if star_age == "middle":
            planet_story.speech_text += Translator.Star.star_age_middle
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_GIANT
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_GIANT
        if star_age == "old":
            planet_story.speech_text += Translator.Star.star_age_old
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_SUPER_GIANT
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_SUPER_GIANT

        planet_story.speech_text += (' ' + Translator.Planet.planet_size)

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


# endregion

# region Planet Handlers


class PlanetSizeHandler(AbstractRequestHandler):
    """

    P L A N E T   S I Z E

    """
    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_SIZE)(handler_input) \
               and planet_story.current_question == Question.Planet.PLANET_SIZE

    def handle(self, handler_input):
        planet_size = str(
            handler_input.request_envelope.request.intent.slots[Slots.PLANET_SIZE].value).lower()

        planet_story.set_planet_size(planet_size)

        apl_datasource = _load_apl_document("./data/main.json")

        planet_story.speech_text = f'Your planet size is {planet_size}. '

        if planet_size == "large":
            planet_story.speech_text += Translator.Planet.planet_size_large
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url']\
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_size == "medium":
            planet_story.speech_text += Translator.Planet.planet_size_medium
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_size == "small":
            planet_story.speech_text += Translator.Planet.planet_size_small
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'

        planet_story.speech_text += (' ' + Translator.Planet.planet_distance)

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


class PlanetDistanceHandler(AbstractRequestHandler):
    """

    P L A N E T   D I S T A N C E

    """
    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_DISTANCE)(handler_input) \
               and planet_story.current_question == Question.Planet.PLANET_DISTANCE

    def handle(self, handler_input):

        planet_distance = str(
            handler_input.request_envelope.request.intent.slots[Slots.DISTANCE].value).lower()

        planet_story.set_planet_distance(planet_distance)

        apl_datasource = _load_apl_document("./data/main.json")

        planet_story.speech_text = f'Your planet is {planet_distance}. '



        if planet_distance == "neighbouring":
            planet_story.speech_text += ' ' + Translator.Planet.planet_distance_neighbouring
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_distance == "near":
            planet_story.speech_text += ' ' + Translator.Planet.planet_distance_near
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url']\
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] \
                = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_distance == "far":
            planet_story.speech_text += ' ' + Translator.Planet.planet_distance_far
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = \
                'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] =\
                'https://planet-story.s3.amazonaws.com/stars-02.png'

        planet_story.speech_text += ' ' + Translator.Planet.planet_distance + ' ' + \
                                    Translator.Launch.launch + ' ' + Translator.Star.star_brightness

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


class PlanetAgeIntentHandler(AbstractRequestHandler):
    """

    P L A N E T  A G E

    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.AGE)(
            handler_input) and planet_story.current_question == Question.Planet.PLANET_AGE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        planet_age = str(
            handler_input.request_envelope.request.intent.slots[Slots.AGE].value).lower()

        planet_story.set_star_age(planet_age)

        apl_datasource = _load_apl_document("./data/main.json")

        planet_story.speech_text = f'Your star age is {planet_age}. '

        if planet_age == "young":
            planet_story.speech_text += Translator.Planet.planet_age_young
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_DWARF
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_DWARF
        if planet_age == "middle":
            planet_story.speech_text += Translator.Planet.planet_age_middleaged
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_GIANT
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_GIANT
        if planet_age == "old":
            planet_story.speech_text += Translator.Planet.planet_age_old
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.BLUE_SUPER_GIANT
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.BLUE_SUPER_GIANT

        planet_story.speech_text += (' ' + Translator.End_Game.game_end)

        handler_input.response_builder.speak(planet_story.speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


# endregion


class HelpIntentHandler(AbstractRequestHandler):
    """

    H E L P

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=_load_apl_document("./data/main.json")
            )
        ).add_directive(
            ExecuteCommandsDirective(
                token="pagerToken",
                commands=[
                    AutoPageCommand(
                        component_id="pagerComponentId",
                        duration=5000)
                ]
            )
        )

        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    """

    C A N C E L   A N D    S T O P

    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
               or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


class FallbackHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speech_text = "Fallback. "

        property_question_dict = {
            Question.Star.STAR_BRIGHTNESS: {
                Translator.Star.star_brightness
            },
            Question.Star.STAR_SIZE: {
                Translator.Star.star_age
            },
            Question.Planet.PLANET_DISTANCE: {
                Translator.Planet.planet_distance
            },
            Question.Planet.PLANET_SIZE: {
                Translator.Planet.planet_size
            }
        }

        speech_text += property_question_dict[planet_story.current_question]

        handler_input.response_builder.speak(speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=_load_apl_document("./data/main.json")
            )
        ).add_directive(
            ExecuteCommandsDirective(
                token="pagerToken",
                commands=[
                    AutoPageCommand(
                        component_id="pagerComponentId",
                        duration=5000)
                ]
            )
        )

        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):
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
    Response interceptors are invoked immediately after execution of the request handler for an incoming request.
    """

    def process(self, handler_input, response):
        print("Response generated: {}".format(response))

        handler_input.attributes_manager.session_attributes = planet_story.get_session_variables()


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

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

sb.add_global_request_interceptor(SetupRequestInterceptor())

sb.add_global_response_interceptor(SaveSessionAttributesResponseInterceptor())

sb.add_exception_handler(AllExceptionHandler())

sb.add_request_handler(FallbackHandler())

lambda_handler = sb.lambda_handler()
