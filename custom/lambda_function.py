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
from build_states import State
from planet_story.planet_story import PlanetStory

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
session_variables: dict = {}
planet_story: PlanetStory


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


class SetupRequestInterceptor(AbstractRequestInterceptor):
    """
    Request interceptors are invoked immediately before execution of the request handler for an incoming request.
    """
    def process(self, handler_input):
        print("Request received: {}".format(
            handler_input.request_envelope.request))

        global session_variables, planet_story
        session_variables = handler_input.attributes_manager.session_attributes
        planet_story = PlanetStory(session_variables)


class LaunchRequestHandler(AbstractRequestHandler):
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

# region Star Handlers
class StarBrightnessIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.STAR_BRIGHTNESS)(handler_input) \
               and session_variables["state"] == State.STAR_BRIGHTNESS

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global session_variables
        session_variables["state"] = State.STAR_SIZE

        # Store answer in session variables
        star_brightness = str(
            handler_input.request_envelope.request.intent.slots[Slots.BRIGHTNESS].value).lower()
        session_variables[STAR] = {BRIGHTNESS: star_brightness}

        apl_datasource = _load_apl_document("./data/main.json")
        speech_text = f'Your star brightness is {star_brightness}. '

        if star_brightness == "red":
            speech_text += Translator.Star.star_brightness_red
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/red_star.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/red_star.png'
        if star_brightness == "blue":
            speech_text += Translator.Star.star_brightness_blue
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/blue_star.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/blue_star.png'
        if star_brightness == "yellow":
            speech_text += Translator.Star.star_brightness_yellow
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/yellow_star.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/yellow_star.png'

        ## Ask next question
        speech_text += Translator.Star.star_size

        handler_input.response_builder.speak(speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


class StarSizeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name(Intents.STAR_SIZE)(handler_input) and session_variables["state"] == State.STAR_SIZE

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global session_variables
        session_variables["state"] = State.PLANET_SIZE

        # Store answer in session variables
        star_size = str(
            handler_input.request_envelope.request.intent.slots[Slots.STAR_SIZE].value).lower()
        session_variables[STAR][SIZE] = star_size

        apl_datasource = _load_apl_document("./data/main.json")

        speech_text = f'Your star size is {star_size}. '

        if star_size == "dwarf":
            speech_text +=Translator.Star.star_size_dwarf
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if star_size == "giant":
            speech_text +=Translator.Star.star_size_giant
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if star_size == "super":
            speech_text +=Translator.Star.star_size_super_giant
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'

        speech_text += Translator.Planet.planet_size

        handler_input.response_builder.speak(speech_text).add_directive(
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
    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_SIZE)(handler_input) \
               and session_variables['state'] == State.PLANET_SIZE

    def handle(self, handler_input):
        global session_variables
        session_variables['state'] = State.PLANET_DISTANCE

        # Store answer in session variables
        planet_size = str(
            handler_input.request_envelope.request.intent.slots[Slots.PLANET_SIZE].value).lower()

        session_variables['planets'].append({SIZE: planet_size})

        apl_datasource = _load_apl_document("./data/main.json")

        speech_text = f'Your planet size is {planet_size}. '

        if planet_size == "large":
            speech_text += Translator.Planet.planet_size_large
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_size == "medium":
            speech_text += Translator.Planet.planet_size_medium
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_size == "small":
            speech_text += Translator.Planet.planet_size_small
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'

        speech_text += Translator.Planet.planet_distance

        handler_input.response_builder.speak(speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


class PlanetDistanceHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name(Intents.PLANET_DISTANCE)(handler_input) \
               and session_variables['state'] == State.PLANET_DISTANCE

    def handle(self, handler_input):
        global session_variables
        session_variables['state'] = State.STAR_BRIGHTNESS

        # Store answer in session variables
        planet_distance = str(
            handler_input.request_envelope.request.intent.slots[Slots.DISTANCE].value).lower()

        session_variables[PLANET][DISTANCE] = planet_distance

        planets: list = session_variables['planets']

        planets[len(planets) - 1][DISTANCE] = planet_distance

        apl_datasource = _load_apl_document("./data/main.json")

        if planet_distance == "near":
            speech_text = Translator.Planet.planet_distance_near
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_distance == "midway":
            speech_text = Translator.Planet.planet_distance_midway
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
        if planet_distance == "far":
            speech_text = Translator.Planet.planet_distance_far
            apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'
            apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = 'https://planet-story.s3.amazonaws.com/stars-02.png'

        speech_text = Translator.Planet.planet_distance + '. ' + Translator.Launch.launch + ' ' + Translator.Star.star_brightness

        handler_input.response_builder.speak(speech_text).add_directive(
            RenderDocumentDirective(
                token="pagerToken",
                document=_load_apl_document("./templates/main.json"),
                datasources=apl_datasource
            )
        )

        return handler_input.response_builder.response


# endregion


class HelpIntentHandler(AbstractRequestHandler):
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
            State.STAR_BRIGHTNESS: {
                Translator.Star.star_brightness
            },
            State.STAR_SIZE: {
                Translator.Star.star_age
            },
            State.PLANET_DISTANCE: {
                Translator.Planet.planet_distance
            },
            State.PLANET_SIZE: {
                Translator.Planet.planet_size
            }
        }

        speech_text += property_question_dict[session_variables['state']]

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
        global session_variables
        handler_input.attributes_manager.session_attributes = session_variables


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# region Custom handlers

# Star
# sb.add_request_handler(StarAgeIntentHandler())
sb.add_request_handler(StarBrightnessIntentHandler())
sb.add_request_handler(StarSizeIntentHandler())

# Planets
# sb.add_request_handler(PlanetAtmosphereHandler())
sb.add_request_handler(PlanetDistanceHandler())
sb.add_request_handler(PlanetSizeHandler())

# endregion

sb.add_global_request_interceptor(SetupRequestInterceptor())

sb.add_global_response_interceptor(SaveSessionAttributesResponseInterceptor())

sb.add_exception_handler(AllExceptionHandler())

sb.add_request_handler(FallbackHandler())

lambda_handler = sb.lambda_handler()
