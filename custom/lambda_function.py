# Generic ASK SDK imports
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor

# Custom skill code

SKILL_TITLE = 'Build A Planet'
sb = SkillBuilder()
session_variables = {}

class SetupRequestInterceptor(AbstractRequestInterceptor):
    """
    Request interceptors are invoked immediately before execution of the request handler for an incoming request.
    """
    def process(self, handler_input):
        print("Request received: {}".format(handler_input.request_envelope.request))

        global session_variables
        session_variables = handler_input.attributes_manager.session_attributes

        if session_variables is None:
            session_variables = {
                "state": "test"
            }


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speech_text = "You can say hello to me!"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard(SKILL_TITLE, speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
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

sb.add_global_request_interceptor(SetupRequestInterceptor())

sb.add_global_response_interceptor(SaveSessionAttributesResponseInterceptor())

sb.add_exception_handler(AllExceptionHandler())

lambda_handler = sb.lambda_handler()
