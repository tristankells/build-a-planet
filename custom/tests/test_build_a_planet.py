import unittest
from planet_story.planet_story import PlanetStory
from planet_story.solar_questions import Question


class IntegrationTests(unittest.TestCase):
    def test__constructor_take_none(self):
        planet_story = PlanetStory(None)

        self.assertEqual(planet_story.current_question, Question.Star.STAR_BRIGHTNESS,
                         'Next question should be star brightness')
        self.assertEqual(planet_story.sun, {}, 'Sun should be an empty dictionary')
        self.assertEqual(planet_story.planets, [], 'Planets should be an empty list')

    def test__constructor_take_empty_session_variables(self):
        planet_story = PlanetStory({})

        self.assertEqual(planet_story.current_question, Question.Star.STAR_BRIGHTNESS,
                         'Next question should be star brightness')
        self.assertEqual(planet_story.sun, {}, 'True should be True')
        self.assertEqual(planet_story.planets, [], 'True should be True')

    def test__get_session_variables_returns_valid_defaults(self):
        planet_story = PlanetStory(None)
        session_variables = planet_story.get_session_variables()
        question = session_variables['current_question']
        sun = session_variables['sun']
        planets = session_variables['planets']

        self.assertEqual(question, Question.Star.STAR_BRIGHTNESS,
                         'Next question should be star brightness')
        self.assertEqual(sun, {}, 'True should be True')
        self.assertEqual(planets, [], 'True should be True')

    def test__set_sun_brightness_sets_correctly(self):
        planet_story = PlanetStory(None)
        planet_story.set_star_brightness('red')

        self.assertEqual(planet_story.sun.brightness, [], 'True should be True')


if __name__ == '__main__':
    unittest.main()
