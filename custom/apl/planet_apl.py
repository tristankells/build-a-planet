from alexa.assets import Assets
from alexa.slots import PlanetSize, Brightness, StarSize, Age, Distance
from apl.apl_helpers import set_apl_datasource_image_sources

PICTURES = Assets.Pictures


def get_image_based_on_planet_size(apl_datasource, planet_size, star_brightness, star_size, star_age):
    image_url = _set_image_url_based_on_planet_size(
        planet_size,
        small_url=_set_image_url_based_star_power(
            star_brightness,
            star_size,
            star_age,
            normal_url=PICTURES.GENERIC_SMALL,
            fireball_url=PICTURES.FIREBALL_SMALL
        ),
        medium_url=_set_image_url_based_star_power(
            star_brightness,
            star_size,
            star_age,
            normal_url=PICTURES.GENERIC_MEDIUM,
            fireball_url=PICTURES.FIREBALL_MEDIUM
        ),
        large_url=_set_image_url_based_star_power(
            star_brightness,
            star_size,
            star_age,
            normal_url=PICTURES.GENERIC_LARGE,
            fireball_url=PICTURES.FIREBALL_LARGE
        )
    )

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource


def get_image_based_on_planet_distance(apl_datasource, planet_distance, planet_size, star_brightness, star_size,
                                       star_age):
    image_url = None

    if planet_distance == Distance.NEAR or \
            star_size == StarSize.SUPER or \
            (star_size == StarSize.GIANT and star_age == Age.YOUNG):

        image_url = _set_image_url_based_on_planet_size(
            planet_size,
            small_url=PICTURES.FIREBALL_SMALL,
            medium_url=PICTURES.FIREBALL_MEDIUM,
            large_url=PICTURES.FIREBALL_LARGE
        )

    elif planet_distance == Distance.MIDWAY:
        image_url = _set_image_url_based_on_planet_size(
            planet_size,
            small_url=PICTURES.GENERIC_SMALL,
            medium_url=PICTURES.GENERIC_MEDIUM,
            large_url=PICTURES.GENERIC_LARGE
        )

    elif planet_distance == Distance.FAR:
        image_url = _set_image_url_based_on_planet_size(
            planet_size,
            small_url=PICTURES.ICEBALL_SMALL,
            medium_url=PICTURES.ICEBALL_MEDIUM,
            large_url=PICTURES.ICEBALL_LARGE
        )

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource


def get_image_based_on_planet_age(apl_datasource, planet_distance, planet_size, star_brightness, star_size, star_age):
    raise NotImplementedError


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
