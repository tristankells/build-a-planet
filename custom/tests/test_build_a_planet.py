import unittest
from planet_story.planet_story import PlanetStory
from planet_story.solar_questions import Question


class IntegrationTests(unittest.TestCase):
    def test__constructor_take_none(self):
        planet_story = PlanetStory(None)

        self.assertEqual(planet_story.current_question, Question.Star.BRIGHTNESS,
                         'Next question should be star brightness')

        self.assertEqual(planet_story.star.brightness, '', 'Sun should be an empty dictionary')
        self.assertEqual(planet_story.star.size, '', 'Sun should be an empty dictionary')

        self.assertEqual(planet_story.planet.distance, '', 'Sun should be an empty dictionary')
        self.assertEqual(planet_story.planet.size, '', 'Sun should be an empty dictionary')

    def test__constructor_take_empty_session_variables(self):
        planet_story = PlanetStory({})

        self.assertEqual(planet_story.current_question, Question.Star.BRIGHTNESS,
                         'Next question should be star brightness')

        self.assertEqual(planet_story.star.brightness, '', 'Sun should be an empty dictionary')
        self.assertEqual(planet_story.star.size, '', 'Sun should be an empty dictionary')

        self.assertEqual(planet_story.planet.distance, '', 'Sun should be an empty dictionary')
        self.assertEqual(planet_story.planet.size, '', 'Sun should be an empty dictionary')

    def test__get_session_variables_returns_valid_defaults(self):
        planet_story = PlanetStory(None)
        session_variables = planet_story.get_session_variables()
        question = session_variables['current_question']
        sun = session_variables['star']
        planet = session_variables['planet']

        self.assertEqual(question, Question.Star.BRIGHTNESS,
                         'Next question should be star brightness')

        self.assertEqual(sun, {'brightness': '', 'size': '', 'age': ''}, 'Should return valid sun as dictionary')

        self.assertEqual(planet, {'size': '', 'distance': '', 'age': ''}, 'Should return valid planet as dictionary')

    def test__get_session_variables_returns_saved_values(self):
        planet_story = PlanetStory({
            'current_question': 'star_brightness',
            'star': {
                'brightness': 'red', 'size': 'giant', 'age': 'old'
            },
            'planet': {
                'size': 'huge', 'distance': 'far', 'age': 'old'
            }

        })

        session_variables = planet_story.get_session_variables()

        question = session_variables['current_question']
        sun = session_variables['star']
        planet = session_variables['planet']

        self.assertEqual(question, Question.Star.BRIGHTNESS,
                         'Next question should be star brightness')

        self.assertEqual(sun, {'brightness': 'red', 'size': 'giant', 'age': 'old'},
                         'Should return valid sun as dictionary')

        self.assertEqual(planet, {'size': 'huge', 'distance': 'far', 'age': 'old'},
                         'Should return valid planet as dictionary')

    def test__set_sun_brightness_sets_correctly(self):
        planet_story = PlanetStory(None)
        planet_story.set_star_brightness('test')

        self.assertEqual(planet_story.star.brightness, 'test', 'Should be test')

    def test__set_star_size_sets_correctly(self):
        planet_story = PlanetStory(None)
        planet_story.set_star_size('test')

        self.assertEqual(planet_story.star.size, 'test', 'Should be test')

    def test__set_planet_size_sets_correctly(self):
        planet_story = PlanetStory(None)
        planet_story.set_planet_size('test')

        self.assertEqual(planet_story.planet.size, 'test', 'Should be test')

    def test__set_planet_distance_sets_correctly(self):
        planet_story = PlanetStory(None)
        planet_story.set_planet_distance('test')

        self.assertEqual(planet_story.planet.distance, 'test', 'Should be test')


if __name__ == '__main__':
    unittest.main()
