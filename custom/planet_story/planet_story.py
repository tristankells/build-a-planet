from planet_story.solar_questions import Question

from translator.default_narrator import DefaultTranslator
from translator.cowboy_narrator import CowboyTranslator


# Custom skill code

from planet_story.planet import Planet
from planet_story.star import Star
from planet_story.narrator import Narrator
from alexa.slots import Brightness, StarSize, Age, PlanetSize, Distance

# constants
CURRENT_QUESTION = 'current_question'
STAR = 'star'
PLANET = 'planet'
PLANET_STORY = 'planet_story'
PREVIOUS_SPEECH_TEXT = 'previous_speech_text'
NARRATOR = 'narrator'
COWBOY_UNLOCKED = 'cowboy_unlocked'


class PlanetStory:
    current_question: str  # The question currently being asked
    planet: Planet
    star: Star
    is_planet_habitable: bool
    planet_story: str
    speech_text: str  # The response given to the user
    previous_speech_text: str
    reprompt: str
    narrator: str
    cowboy_unlocked: bool
    translator: DefaultTranslator or CowboyTranslator

    def __init__(self, session_variables):
        if session_variables is None:
            self._set_default_session_variables()
        else:
            self.current_question = session_variables[
                CURRENT_QUESTION] if CURRENT_QUESTION in session_variables else Question.Star.BRIGHTNESS

            star_brightness = session_variables[STAR][Star.BRIGHTNESS] if STAR in session_variables else ''
            star_size = session_variables[STAR][Star.SIZE] if STAR in session_variables else ''
            star_age = session_variables[STAR][Star.AGE] if STAR in session_variables else ''
            self.star = Star(star_brightness, star_size, star_age)

            planet_size = session_variables[PLANET][Planet.SIZE] if PLANET in session_variables else ''
            planet_distance = session_variables[PLANET][Planet.DISTANCE] if PLANET in session_variables else ''
            planet_age = session_variables[PLANET][Planet.AGE] if PLANET in session_variables else ''
            self.planet = Planet(planet_size, planet_distance, planet_age)

            self.planet_story = session_variables[
                PLANET_STORY] if PLANET_STORY in session_variables else ''

            self.previous_speech_text = session_variables[
                PREVIOUS_SPEECH_TEXT] if PREVIOUS_SPEECH_TEXT in session_variables else ''

            self.narrator = session_variables[
                NARRATOR] if NARRATOR in session_variables else Narrator.default

            self.cowboy_unlocked = session_variables[
                COWBOY_UNLOCKED] if COWBOY_UNLOCKED in session_variables else False

            self.is_planet_habitable = False

            self.speech_text = ''

            self.reprompt = 'Please say again.'

        if self.narrator == Narrator.cowboy:
            self.translator = CowboyTranslator()
        else:
            self.translator = DefaultTranslator()

    def get_session_variables(self):
        return {
            CURRENT_QUESTION: self.current_question,
            STAR: vars(self.star),
            PLANET: vars(self.planet),
            PLANET_STORY: self.planet_story,
            PREVIOUS_SPEECH_TEXT: self.previous_speech_text,
            NARRATOR: self.narrator,
            COWBOY_UNLOCKED: self.cowboy_unlocked
        }

    def launch(self):
        """
        Called in the Launch handler
        :return:
        """
        self.speech_text = self.translator.Launch.launch

    def set_star_brightness(self, brightness):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        self.star.brightness = brightness

        if brightness == Brightness.RED:
            self.speech_text += self.translator.Star.star_brightness_red
        if brightness == Brightness.BLUE:
            self.speech_text += self.translator.Star.star_brightness_blue
        if brightness == Brightness.YELLOW:
            self.speech_text += self.translator.Star.star_brightness_yellow

        # Ask next question
        self.speech_text += '' + self.translator.Star.star_size

        self.previous_speech_text = self.speech_text

        self.current_question = Question.Star.SIZE

    def set_star_size(self, size):
        """
        Called in the PlanetSizeHandler handler
        :return:
        """
        self.star.size = size

        if size == StarSize.DWARF:
            self.speech_text += self.translator.Star.star_size_dwarf
        if size == StarSize.GIANT:
            self.speech_text += self.translator.Star.star_size_giant
        if size == StarSize.SUPER:
            self.speech_text += self.translator.Star.star_size_super_giant

        self.speech_text += ' ' + self.translator.Star.star_age

        self.previous_speech_text = self.speech_text

        self.current_question = Question.Star.AGE

    def set_star_age(self, age):
        """
        Called in the PlanetSizeHandler handler
        :return:
        """
        self.star.age = age

        if age == Age.YOUNG:
            self.speech_text += self.translator.Star.star_age_young
        if age == Age.MIDDLE:
            self.speech_text += self.translator.Star.star_age_middle
        if age == Age.OLD:
            self.speech_text += self.translator.Star.star_age_old

        self.speech_text += ' ' + self.translator.Planet.planet_size

        self.previous_speech_text = self.speech_text

        self.current_question = Question.Planet.SIZE

    def set_planet_size(self, size):
        """
        Called in the PlanetDistanceHandler handler
        :return:
        """
        self.planet.size = size

        if size == PlanetSize.SMALL:
            self.speech_text += self.translator.Planet.planet_size_small
        if size == PlanetSize.MEDIUM:
            self.speech_text += self.translator.Planet.planet_size_medium
        if size == PlanetSize.LARGE:
            self.speech_text += self.translator.Planet.planet_size_large

        self.speech_text += self.translator.Planet.planet_distance

        self.previous_speech_text = self.speech_text

        self.current_question = Question.Planet.DISTANCE

    def set_planet_distance(self, distance):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        self.planet.distance = distance

        if distance == Distance.NEAR:
            self.speech_text += self.translator.Planet.planet_distance_near
        if distance == Distance.MIDWAY:
            self.speech_text += self.translator.Planet.planet_distance_midway
        if distance == Distance.FAR:
            self.speech_text += self.translator.Planet.planet_distance_far

        self.speech_text += self.translator.Planet.planet_age

        self.previous_speech_text = self.speech_text

        self.current_question = Question.Planet.AGE

    def set_planet_age(self, age):
        """
        Called in the StarBrightnessIntentHandler handler
        :return:
        """
        self.planet.age = age

        if age == Age.YOUNG:
            self.speech_text += self.translator.Planet.planet_age_young
        if age == Age.MIDDLE:
            self.speech_text += self.translator.Planet.planet_age_middleaged
        if age == Age.OLD:
            self.speech_text += self.translator.Planet.planet_age_old

        # Now solar system is built, test if planet is habitable
        self.test_if_planet_habitable()

        self.speech_text += self.translator.EndGame.game_end

        self.previous_speech_text = self.speech_text

        self.current_question = Question.REVIEW

    def purchase_success(self):
        self.speech_text = 'Thank you for purchasing the space cowboy voice pack. Say "Activate Space Cowboy" at any time to change voice.'
        self.cowboy_unlocked = True

    def purchase_declined(self):
        self.speech_text = 'Resuming your game.'

    def learn_about_solar_systems(self):
        self.speech_text = self.translator.SolarSystem.planetary_system_yes
        self.speech_text += self.translator.Star.star_brightness

    def do_not_learn_about_solar_systems(self):
        self.speech_text = self.translator.SolarSystem.planetary_system_no
        self.speech_text += self.translator.Star.star_brightness

    def review_solar_system(self, isp_enabled):
        self.speech_text += self.planet_story
        if self.cowboy_unlocked is False and isp_enabled:
            self.speech_text += self.translator.Purchase.purchase_request
        self.speech_text += self.translator.EndGame.game_play_again

        self.current_question = Question.PLAY_AGAIN

    def do_not_review_solar_system(self, isp_enabled):
        if self.cowboy_unlocked is False and isp_enabled:
            self.speech_text += self.translator.Purchase.purchase_request
        self.speech_text = self.translator.EndGame.game_play_again

        self.current_question = Question.PLAY_AGAIN

    def play_again(self):
        self.speech_text = self.translator.EndGame.game_play_again_yes
        self.speech_text += self.translator.Star.star_brightness

        self.current_question = Question.Star.BRIGHTNESS

    def help(self):
        self.speech_text = self.translator.help

    def repeat(self):
        self.speech_text = self.previous_speech_text

    def exit_skill(self):
        self.speech_text = self.translator.EndGame.game_play_again_no

    def what_can_i_buy(self):
        self.speech_text = self.translator.Store.what_can_i_buy

    def toggle_voice(self):
        if self.narrator == Narrator.default:
            if self.cowboy_unlocked:
                self.narrator = Narrator.cowboy
                self.speech_text = self.translator.ToggleVoice.cowboy
                self.speech_text += self.previous_speech_text.replace('Tristan/', 'Ranul/cowboy_')
            else:
                self.speech_text = self.translator.ToggleVoice.cowboy_locked
                self.speech_text += self.previous_speech_text

        elif self.narrator == Narrator.cowboy:
            self.narrator = Narrator.default
            self.speech_text = self.translator.ToggleVoice.default
            self.speech_text += self.previous_speech_text.replace('Ranul/cowboy_', 'Tristan/')

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
            return """Your planet is in the early stages of its evolution and is still forming. It's very likely that 
            the surface is full of molten rocks and not able to support liquid water."""

    def _set_default_session_variables(self):
        self.current_question = Question.Star.BRIGHTNESS
        self.speech_text = ''
        self.planet = Planet()
        self.star = Star()
        self.is_planet_habitable = False
        self.planet_story = ''
        self.previous_speech_text = ''
        self.narrator = Narrator.default
        self.cowboy_unlocked = False
