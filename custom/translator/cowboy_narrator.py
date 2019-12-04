from translator.translator import Translator

ROOT_URL = 'https://s3.amazonaws.com/planet-story/Audio/Ranul/'
AUDIO = "<audio src='" + ROOT_URL + "{}.mp3' />"


class CowboyTranslator(Translator):


    class Launch:
        launch = AUDIO.format("cowboy_launch")

    class Store:
        what_can_i_buy = AUDIO.format("cowboy_what_can_i_buy")

    class SolarSystem:
        planetary_system_yes = AUDIO.format("cowboy_planetary_system_yes")
        planetary_system_no = AUDIO.format("cowboy_planetary_system_no")

    class Star:
        star_create = AUDIO.format("cowboy_star_create")
        star_create_yes = AUDIO.format("cowboy_star_create_yes")
        star_create_no = AUDIO.format("cowboy_star_create_no")
        star_brightness = AUDIO.format("cowboy_star_brightness")
        star_brightness_blue = AUDIO.format("cowboy_star_brightness_blue")
        star_brightness_yellow = AUDIO.format("cowboy_star_brightness_yellow")
        star_brightness_red = AUDIO.format("star_brightness_red")
        star_brightness_other = AUDIO.format("cowboy_star_brightness_other")

        star_size = AUDIO.format("cowboy_star_size")
        star_size_super_giant = AUDIO.format("cowboy_star_size_super_giant")
        star_size_giant = AUDIO.format("cowboy_star_size_giant")
        star_size_dwarf = AUDIO.format("cowboy_star_size_dwarf")
        star_size_other = AUDIO.format("cowboy_star_size_other")

        star_age = AUDIO.format("cowboy_star_age")
        star_age_young = AUDIO.format("cowboy_star_age_young")
        star_age_middle = AUDIO.format("cowboy_star_age_middle")
        star_age_old = AUDIO.format("cowboy_star_age_old")
        star_age_other = AUDIO.format("star_age_other")

    class Planet:
        planet_create = AUDIO.format("planet_create")
        planet_create_yes = AUDIO.format("planet_create_yes")
        planet_create_no = AUDIO.format("planet_create_no")

        planet_distance = AUDIO.format("cowboy_what_is_planet_distance_AND_distance_options")
        planet_distance_neighbouring = AUDIO.format("cowboy_planet_distance_neighbouring")
        planet_distance_near = AUDIO.format("cowboy_planet_distance_near")
        planet_distance_far = AUDIO.format("cowboy_planet_distance_far")
        planet_distance_other = AUDIO.format("cowboy_invalid_distance")

        planet_size = AUDIO.format("cowboy_what_is_the_size_of_your_planet") + AUDIO.format(
            "cowboy_planet_size_options")
        planet_size_large = AUDIO.format("cowboy_planet_size_is_gigantic")
        planet_size_medium = AUDIO.format("cowboy_planet_size_medium")
        planet_size_small = AUDIO.format("cowboy_planet_size_small")
        planet_size_other = AUDIO.format("planet_size_other")

        planet_age = AUDIO.format("cowboy_what_is_the_age_of_your_planet")
        planet_age_young = AUDIO.format("cowboy_planet_age_young")
        planet_age_middleaged = AUDIO.format("cowboy_planet_age_middle")
        planet_age_old = AUDIO.format("cowboy_planet_age_old")
        planet_age_other = AUDIO.format("planet_age_other")

    class EndGame:
        game_end = AUDIO.format("game_end")
        game_play_again = AUDIO.format("game_play_again")
        game_play_again_yes = AUDIO.format("game_play_again_yes")
        game_play_again_no = AUDIO.format("game_play_again_no")

    class Purchase:
        purchase_request = AUDIO.format("purchase_request")
