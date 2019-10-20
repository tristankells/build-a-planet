from planet_story.solar_questions import Question

from translator.translator import Translator

# Custom skill code

from planet_story.planet import Planet
from planet_story.star import Star


# constants
CURRENT_QUESTION = 'current_question'
STAR = 'star'
PLANET = 'planet'


# TODO Removed the redudant tpyes in the questions

class PlanetStory:
    speech_text: str  # The response given to the user
    current_question: str  # The question currently being asked
    planet: Planet
    star: Star

    def __init__(self, session_variables):
        if session_variables is None:
            self._set_default_session_variables()
        else:
            self.current_question = session_variables[
                CURRENT_QUESTION] if CURRENT_QUESTION in session_variables else Question.Star.STAR_BRIGHTNESS

            star_brightness = session_variables[STAR][Star.BRIGHTNESS] if PLANET in session_variables else ''
            star_size = session_variables[STAR][Star.SIZE] if PLANET in session_variables else ''
            self.star = Star(star_brightness, star_size)

            planet_size = session_variables[PLANET][Planet.SIZE] if PLANET in session_variables else ''
            planet_distance = session_variables[PLANET][Planet.DISTANCE] if PLANET in session_variables else ''
            self.planet = Planet(planet_size, planet_distance)

    def get_session_variables(self):
        return {
            CURRENT_QUESTION: self.current_question,
            STAR: vars(self.star),
            PLANET: vars(self.planet)
        }

    def launch(self):
        """
        Called in the Launch handler
        :return:
        """
        self.speech_text = Translator.Launch.launch

    def set_star_brightness(self, brightness):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        self.star.brightness = brightness
        self.current_question = Question.Star.STAR_SIZE

    def set_star_size(self, size):
        """
        Called in the PlanetSizeHandler handler
        :return:
        """
        self.star.size = size
        self.current_question = Question.Star.STAR_AGE

    def set_star_age(self, age):
        """
        Called in the PlanetSizeHandler handler
        :return:
        """
        self.star.age = age
        self.current_question = Question.Planet.PLANET_SIZE

    def set_planet_size(self, size):
        """
        Called in the PlanetDistanceHandler handler
        :return:
        """
        self.planet.size = size
        self.current_question = Question.Planet.PLANET_DISTANCE

    def set_planet_distance(self, distance):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        self.planet.distance = distance
        self.current_question = Question.Planet.PLANET_AGE

    def set_planet_age(self, age):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        self.planet.age = age
        self.current_question = Question.Star.STAR_BRIGHTNESS

    def learn_about_solar_systems(self):
        self.speech_text = Translator.Solar_System.planetary_system_yes
        self.speech_text += Translator.Star.star_brightness

    def do_not_learn_about_solar_systems(self):
        self.speech_text = Translator.Solar_System.planetary_system_no
        self.speech_text += Translator.Star.star_brightness

    def test_if_planet_habitable(self):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        if (self.star.brightness == 'red' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'red' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'near' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'red' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'red' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'near' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'yellow' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'yellow' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'yellow' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        elif (self.star.brightness == 'yellow' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.speech_text = 'Your planet is habitable'
        else:  # Planet is not habitable
            self.speech_text = 'Your planet is not habitable'

    def _set_default_session_variables(self):
        self.current_question = Question.Star.STAR_BRIGHTNESS
        self.planet = Planet()
        self.star = Star()
