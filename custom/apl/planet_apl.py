from alexa.assets import Assets
from alexa.slots import PlanetSize, Brightness, StarSize, Age
from apl.apl_helpers import set_apl_datasource_image_sources

PICTURES = Assets.Pictures


def get_image_planet_size(apl_datasource, planet_size, star_brightness, star_size, star_age):
    image_url = _set_image_url_based_on_planet_size(
        planet_size,
        _set_image_url_based_star_power(
            star_brightness,
            star_size,
            star_age,
            normal_url=PICTURES.GENERIC_SMALL,
            fireball_url=PICTURES.FIREBALL_SMALL
        ),
        _set_image_url_based_star_power(
            star_brightness,
            star_size,
            star_age,
            normal_url=PICTURES.FIREBALL_MEDIUM,
            fireball_url=PICTURES.FIREBALL_SMALL
        ),
        _set_image_url_based_star_power(
            star_brightness,
            star_size,
            star_age,
            normal_url=PICTURES.GENERIC_LARGE,
            fireball_url=PICTURES.FIREBALL_LARGE
        )
    )

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource


def get_image_habitable_planet(apl_datasource, planet_size):
    image_url = _set_image_url_based_on_planet_size(
        planet_size,
        PICTURES.EARTH_SMALL,
        PICTURES.EARTH_MEDIUM,
        PICTURES.EARTH_LARGE
    )

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource


def _set_image_url_based_on_planet_size(size, small_url, medium_url, large_url):
    if size == PlanetSize.SMALL:
        return small_url
    elif size == PlanetSize.MEDIUM:
        return medium_url
    elif size == PlanetSize.LARGE:
        return large_url


def _set_image_url_based_star_power(brightness, size, age, normal_url, fireball_url):
    if brightness == Brightness.BLUE or size == StarSize.SUPER or age == Age.YOUNG:
        return fireball_url
    else:
        return normal_url
