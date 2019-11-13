from alexa.assets import Assets
from alexa.slots import PlanetSize
from apl.apl_helpers import set_apl_datasource_image_sources


def get_image_habitable_planet(apl_datasource, planet_size):
    image_url = None

    if planet_size == PlanetSize.SMALL:
        image_url = Assets.Pictures.EARTH_SMALL
    elif planet_size == PlanetSize.MEDIUM:
        image_url = Assets.Pictures.EARTH_MEDIUM
    elif planet_size == PlanetSize.LARGE:
        image_url = Assets.Pictures.EARTH_LARGE

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource
