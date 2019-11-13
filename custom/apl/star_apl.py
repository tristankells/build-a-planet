from alexa.assets import Assets
from alexa.slots import Brightness, StarSize, Age
from apl.apl_helpers import set_apl_datasource_image_sources

PICTURES = Assets.Pictures


# region Public Functions

def get_image_star_brightness(apl_datasource, star_brightness):
    """
    Returns datasource with APL after the user gives the start brightness answer
    :param apl_datasource: 
    :param star_brightness: 
    :return: 
    """
    image_url = None

    if star_brightness == Brightness.YELLOW:
        image_url = Assets.Pictures.YELLOW_BRIGHTNESS
    elif star_brightness == Brightness.RED:
        image_url = Assets.Pictures.RED_BRIGHTNESS
    elif star_brightness == Brightness.BLUE:
        image_url = Assets.Pictures.BLUE_BRIGHTNESS

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource


def get_image_star_size(apl_datasource, star_brightness, star_size):
    """
    Returns datasource with APL after the user gives the start size answer
    :param apl_datasource: 
    :param star_brightness: 
    :param star_size: 
    :return: 
    """
    image_url = None

    if star_brightness == Brightness.YELLOW:
        image_url = _set_image_url_based_on_star_size(
            star_size,
            dwarf_url=PICTURES.YELLOW_DWARF,
            giant_url=PICTURES.YELLOW_GIANT,
            super_url=PICTURES.YELLOW_SUPER
        )

    elif star_brightness == Brightness.RED:
        image_url = _set_image_url_based_on_star_size(
            star_size,
            dwarf_url=PICTURES.RED_DWARF,
            giant_url=PICTURES.RED_GIANT,
            super_url=PICTURES.RED_SUPER
        )

    elif star_brightness == Brightness.BLUE:
        image_url = _set_image_url_based_on_star_size(
            star_size,
            PICTURES.BLUE_DWARF,
            PICTURES.BLUE_GIANT,
            PICTURES.BLUE_SUPER
        )

    apl_datasource = set_apl_datasource_image_sources(apl_datasource, image_url)

    return apl_datasource


def get_image_star_age(apl_datasource, star_brightness, star_size, star_age):
    image_url = None


# endregion

# region Private Functions


def _set_image_url_based_on_star_size(size, dwarf_url, giant_url, super_url):
    if size == StarSize.DWARF:
        return dwarf_url
    if size == StarSize.GIANT:
        return giant_url
    if size == StarSize.SUPER:
        return super_url


def _set_image_url_based_on_star_age(size, dwarf_url, giant_url, super_url):
    if size == Age.YOUNG:
        return dwarf_url
    if size == Age.MIDDLE:
        return giant_url
    if size == Age.OLD:
        return super_url

# endregion
