ROOT_URL = 'https://s3.amazonaws.com/planet-story/Audio/'
AUDIO = "<audio src='" + ROOT_URL + "{}.mp3' />"



def kendra(speech_text):
    """
    Female American polly voice Kendra (en-US). For use when we don't have the audio. Slowed to 85% speed.
    :return:
    """
    return f'<voice name="Kendra"><lang xml:lang="en-US">{speech_text}</lang></voice>'


def ivy(speech_text):
    """
    Female American polly voice Ivy (en-US). For use when we don't have the audio. Slowed to 85% speed.
    :return:
    """
    return f'<voice name="Ivy"><lang xml:lang="en-US">{speech_text}</lang></voice>'


def joanna(speech_text):
    """
    Female American polly voice Joanna (en-US). For use when we don't have the audio. Slowed to 85% speed.
    :return:
    """
    return f'<voice name="Joanna"><lang xml:lang="en-US">{speech_text}</lang></voice>'


def kimberly(speech_text):
    """
    Female American polly voice Ivy (en-US). For use when we don't have the audio. Slowed to 85% speed.
    :return:
    """
    return f'<voice name="Kimberly"><lang xml:lang="en-US">{speech_text}</lang></voice>'


def salli(speech_text):
    """
    Female American polly voice Ivy (en-US). For use when we don't have the audio. Slowed to 85% speed.
    :return:
    """
    return f'<voice name="Salli"><lang xml:lang="en-US">{speech_text}</lang></voice>'


class Translator:
    class Launch:
        launch = AUDIO.format("launch")

    help = kendra("To exit at any time, say") \
           + joanna(' Exit. ') \
           + kendra("If you would like to continue building your planet, you can say") \
           + joanna(' Repeat ') \
           + kendra("and have me remind you of the next step in building your planet.")

    class Store:
        what_can_i_buy = "If you would like to support the developers of planet story, you can unlock the alternative" \
                         " space cowboy narrator. You will be able to toggle him on and off by saying toggle narrator."

    class SolarSystem:
        planetary_system_yes = AUDIO.format("planetary_system_yes")
        planetary_system_no = AUDIO.format("planetary_system_no")

    class Star:
        star_create = AUDIO.format("star_create")
        star_create_yes = AUDIO.format("star_create_yes")
        star_create_no = AUDIO.format("star_create_no")
        star_brightness = AUDIO.format("star_brightness")
        star_brightness_blue = AUDIO.format("star_brightness_blue")
        star_brightness_yellow = AUDIO.format("star_brightness_yellow")
        star_brightness_red = AUDIO.format("star_brightness_red")
        star_brightness_other = AUDIO.format("star_brightness_other")

        star_size = AUDIO.format("star_size")
        star_size_super_giant = AUDIO.format("star_size_super_giant")
        star_size_giant = AUDIO.format("star_size_giant")
        star_size_dwarf = AUDIO.format("star_size_dwarf")
        star_size_other = AUDIO.format("star_size_other")

        star_age = AUDIO.format("star_age")
        star_age_young = AUDIO.format("star_age_young")
        star_age_middle = AUDIO.format("star_age_middle")
        star_age_old = AUDIO.format("star_age_old")
        star_age_other = AUDIO.format("star_age_other")

    class Planet:
        planet_create = AUDIO.format("planet_create")
        planet_create_yes = AUDIO.format("planet_create_yes")
        planet_create_no = AUDIO.format("planet_create_no")

        planet_distance = AUDIO.format("planet_distance")
        planet_distance_neighbouring = AUDIO.format("planet_distance_neighbouring")
        planet_distance_near = AUDIO.format("planet_distance_near")
        planet_distance_far = AUDIO.format("planet_distance_far")
        planet_distance_other = AUDIO.format("planet_distance_other")

        planet_size = AUDIO.format("planet_size")
        planet_size_large = AUDIO.format("planet_size_large")
        planet_size_medium = AUDIO.format("planet_size_medium")
        planet_size_small = AUDIO.format("planet_size_small")
        planet_size_other = AUDIO.format("planet_size_other")

        planet_age = AUDIO.format("planet_age")
        planet_age_young = AUDIO.format("planet_age_young")
        planet_age_middleaged = AUDIO.format("planet_age_middleaged")
        planet_age_old = AUDIO.format("planet_age_old")
        planet_age_other = AUDIO.format("planet_age_other")

    class EndGame:
        game_end = AUDIO.format("game_end")
        game_play_again = AUDIO.format("game_play_again")
        game_play_again_yes = AUDIO.format("game_play_again_yes")
        game_play_again_no = AUDIO.format("game_play_again_no")

    class Facts:
        fact_create = AUDIO.format("fact_create")
        facts = [
            'There is no atmosphere in space, which means that sound has no medium or way to travel to be heard. Astronauts use radios to stay in communication while in space, since radio waves can still be sent and received.'
            'Venus is the hottest planet in the solar system and has an average surface temperature of around 450° C. Interestingly, Venus is not the closest planet to the Sun – Mercury is closer but because Mercury has no atmosphere to regulate temperature it has a very large temperature fluctuation.'
            'Of all the planets in our solar system apart from Earth, Mars is the one most likely to be hospitable to life. In 1986, NASA found what they thought may be fossils of microscopic living things in a rock recovered from Mars. '
            'The sheer size of space makes it impossible to accurately predict just how many stars we have. Right now, scientists and astronomers use the number of stars within our galaxy, The Milky Way, to estimate. That number is between 200-400 billion stars and there are estimated to be billions of galaxies so the stars in space really are completely uncountable. '
            'Discovered in 1705 by Edmond Halley, the famous comet was last seen in 1986 and is only seen once every 75 to 76 years.'
            'A FULL NASA SPACE SUIT COSTS $12,000,000. While the entire suit costs a cool $12m, 70% of that cost is for the backpack and control module.'
            'Neutron stars are the densest and tiniest stars in the known universe and although they only have a radius of about 10 km (6 mi), they may have a mass of a few times that of the Sun. They can rotate at up to 60 times per second after they are born from a core-collapse supernova star explosion and have been known to spin as fast as 600-712 times per second because of their physics.'
            'THERE MAY BE A PLANET MADE OUT OF DIAMONDS. As space facts go, this is pretty impressive. Research by Yale University scientists suggests that a rocky planet called 55 Cancri which has a radius twice Earth’s, and a mass eight times greater – may have a surface made up of graphite and diamond. It’s 40 light years away but visible to the naked eye in the constellation of Cancer. '
            'THE FOOTPRINTS ON THE MOON WILL BE THERE FOR 100 MILLION YEARS. The Moon has no atmosphere, which means there is no wind to erode the surface and no water to wash the footprints away. This means the footprints of the Apollo astronauts, along with spacecraft prints, rover-prints and discarded material, will be there for millions of years. '
            'ONE DAY ON VENUS IS LONGER THAN ONE YEAR. Venus has a slow axis rotation which takes 243 Earth days to complete its day. The orbit of Venus around the Sun is 225 Earth days, making a year on Venus 18 days less than a day on Venus.'
        ]

    class Purchase:
        purchase_request = 'There is a premium Space Cowboy voice you can purchase. Say "Purchase Space Cowboy" to buy.'