from planet_story.solar_questions import Question

from translator.translator import Translator

# Custom skill code

from planet_story.planet import Planet
from planet_story.star import Star


# constants
CURRENT_QUESTION = 'current_question'
STAR = 'star'
PLANET = 'planet'
AGE = 'age'
PLANET_STORY = 'planet_story'
PREVIOUS_SPEECH_TEXT = 'previous_speech_text'

# TODO Removed the redudant tpyes in the questions


class PlanetStory:
    current_question: str  # The question currently being asked
    planet: Planet
    star: Star
    is_planet_habitable: bool
    planet_story: str
    speech_text: str  # The response given to the user
    previous_speech_text: str

    def __init__(self, session_variables):
        if session_variables is None:
            self._set_default_session_variables()
        else:
            self.current_question = session_variables[
                CURRENT_QUESTION] if CURRENT_QUESTION in session_variables else Question.Star.STAR_BRIGHTNESS

            star_brightness = session_variables[STAR][Star.BRIGHTNESS] if STAR in session_variables else ''
            star_size = session_variables[STAR][Star.SIZE] if STAR in session_variables else ''
            star_age = session_variables[STAR][AGE] if STAR in session_variables else ''
            self.star = Star(star_brightness, star_size, star_age)

            planet_size = session_variables[PLANET][Planet.SIZE] if PLANET in session_variables else ''
            planet_distance = session_variables[PLANET][Planet.DISTANCE] if PLANET in session_variables else ''
            planet_age = session_variables[PLANET][AGE] if PLANET in session_variables else ''
            self.planet = Planet(planet_size, planet_distance, planet_age)

            self.planet_story = session_variables[
                PLANET_STORY] if PLANET_STORY in session_variables else ''

            self.previous_speech_text = session_variables[
                PREVIOUS_SPEECH_TEXT] if PREVIOUS_SPEECH_TEXT in session_variables else ''

            self.is_planet_habitable = False

            self.speech_text = ''

    def get_session_variables(self):
        return {
            CURRENT_QUESTION: self.current_question,
            STAR: vars(self.star),
            PLANET: vars(self.planet),
            PLANET_STORY: self.planet_story,
            PREVIOUS_SPEECH_TEXT: self.previous_speech_text,
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
        self.current_question = Question.REVIEW

    def learn_about_solar_systems(self):
        self.speech_text = Translator.SolarSystem.planetary_system_yes
        self.speech_text += Translator.Star.star_brightness

    def do_not_learn_about_solar_systems(self):
        self.speech_text = Translator.SolarSystem.planetary_system_no
        self.speech_text += Translator.Star.star_brightness

    def review_solar_system(self):
        self.speech_text += self.planet_story
        self.speech_text += Translator.Purchase.purchase_request
        # self.speech_text += Translator.EndGame.game_play_again

        # self.current_question = Question.PLAY_AGAIN
        self.current_question = Question.PURCHASE

    def do_not_review_solar_system(self):
        self.speech_text += Translator.Purchase.purchase_request
        self.speech_text = Translator.EndGame.game_play_again

        # self.current_question = Question.PLAY_AGAIN
        self.current_question = Question.PURCHASE

    def play_again(self):
        self.speech_text = Translator.EndGame.game_play_again_yes
        self.speech_text += Translator.Star.star_brightness

        self.current_question = Question.Star.STAR_BRIGHTNESS

    def help(self):
        self.speech_text = Translator.help

    def repeat(self):
        self.speech_text = self.previous_speech_text

    def exit_skill(self):
        self.speech_text = Translator.EndGame.game_play_again_no

    def test_if_planet_habitable(self):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        if (self.star.brightness == 'red' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Large planets like this are called super earths and they have varying degrees of habitability depending on its atmospheric conditions, gravity, and so on. Just be mindful that red star are prone to flares so your planet may be exposed to this from time to time."
        elif (self.star.brightness == 'red' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'near' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Large planets like this are called super earths and they have varying degrees of habitability depending on its atmospheric conditions, gravity, and so on. Just be mindful that red star are prone to flares so your planet may be exposed to this from time to time."
        elif (self.star.brightness == 'red' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Your planet is the holy grail of habitable planets - it's about the same size as our earth and the right distance from your star. Just be mindful that red star are prone to flares so your planet may be exposed to this from time to time."
        elif (self.star.brightness == 'red' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'near' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Large planets like this are called super earths and they have varying degrees of habitability depending on its atmospheric conditions, gravity, and so on."
        elif (self.star.brightness == 'yellow' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Large planets like this are called super earths and they have varying degrees of habitability depending on its atmospheric conditions, gravity, and so on."
        elif (self.star.brightness == 'yellow' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'large' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Large planets like this are called super earths and they have varying degrees of habitability depending on its atmospheric conditions, gravity, and so on."
        elif (self.star.brightness == 'yellow' and self.star.size == 'giant' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Your planet is the holy grail of habitable planets - it's about the same size as our earth and the right distance from your star."
        elif (self.star.brightness == 'yellow' and self.star.size == 'dwarf' and (self.star.age == 'middle-aged' or self.star.age == 'old') and self.planet.distance == 'midway' and self.planet.size == 'medium' and self.planet.age != 'young'):
            self.is_planet_habitable = True
            self.planet_story += "Perfect! The conditions in your planetary system is just right for your planet to be habitable. Your planet is the holy grail of habitable planets - it's about the same size as our earth and the right distance from your star."
        else:  # Planet is not habitable
            self.is_planet_habitable = False
            self.planet_story += self.construct_not_habitable_text()

    def construct_not_habitable_text(self):
        if self.star.brightness == 'blue':
            return """The blue star is simply too warm for any planet in your system! Blue stars tend to be volatile and eject large amounts of matter into space. They emit lethal radiation and is prone to extreme flares. A blue star that burns bright and dies young, only lasting a few million years. Planets around such a star would have only just formed (they may still have molten surfaces). Thus, your planet is uninhabitable."""

        if self.star.brightness == 'yellow' and self.planet.distance == 'neighbouring':
            return """Your planet is too close to its star and it's too hot. There is no sign of life on your fireball planet."""

        if self.star.brightness == 'red' and self.star.size == 'supergiant' and self.planet.distance == 'neighbouring':
            return """Your planet is too close to its star and it's too hot. There is no sign of life on your fireball planet."""

        if self.star.size == 'supergiant':
            return """Supergiant stars simply live too short a life for any planet to develop conditions for sustaining life! The star's lifespan will be just a few million years long and will die out long before life is able to evolve on your planet."""

        if self.planet.age == 'young':
            return """Your star is still in early stages in its evolution and thus is too volatile and unstable. Unfortunately the star need to be a bit more mature before it can sustain life on planets in its system."""

        if self.planet.distance == 'far':
            return """Your planet is too far from its host star, where light and energy struggles to reach. Even if there were water it would be completely frozen solid. There is no sign of life on your iceball planet. Everything is frozen."""

        if self.planet.size == 'small':
            return """Your planet is too small, and won't have enough gravity to be able to hold on to its atmosphere, which is essential for sustaining life. It's pretty much a barren rock."""

        if self.planet.age == 'young':
            return """Your planet is still early stags in its evolution, and it's still forming. It's very likely that the surface is still full of molten rocks and not able to support liquid water."""

    def _set_default_session_variables(self):
        self.current_question = Question.Star.STAR_BRIGHTNESS
        self.planet = Planet()
        self.star = Star()
        self.is_planet_habitable = False
        self.planet_story = ''
        self.previous_speech_text = ''
