from planet_story.solar_questions import Question

from translator.translator import Translator

# Custom skill code
from alexa_intents import Intents
from intent_slots import Slots
from build_states import State

# constants
PLANETS = 'planets'
SUN = 'sun'
CURRENT_QUESTION = 'current_question'


class PlanetStory:
    speech_text = ""

    def __init__(self, session_variables):
        if session_variables is None:
            self._set_default_session_variables()
        else:
            self.current_question = session_variables[
                CURRENT_QUESTION] if CURRENT_QUESTION in session_variables else Question.Star.STAR_BRIGHTNESS
            self.planet = session_variables[PLANETS] if PLANETS in session_variables else []

            self.sun = session_variables[SUN] if SUN in session_variables else {}

    def get_session_variables(self):
        return {
            CURRENT_QUESTION: self.current_question,
            SUN: self.sun,
            PLANETS: self.planets
        }

    def launch(self):
        """
        Called in the Launch handler
        :return:
        """
        self.speech_text = Translator.Launch.launch + ' ' + Translator.Star.star_brightness

    def set_star_brightness(self):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """

    def _set_default_session_variables(self):
        self.current_question = Question.Star.STAR_BRIGHTNESS
        self.planets = []
        self.sun = {}
