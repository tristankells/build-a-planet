from alexa.assets import Assets


def get_image_habitable_planet(apl_datasource, planet_size):
    if planet_size == "large":
        apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.EARTH_LARGE
        apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.EARTH_LARGE
    elif planet_size == "medium":
        apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.EARTH_MEDIUM
        apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.EARTH_MEDIUM
    elif planet_size == "small":
        apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = Assets.Pictures.EARTH_SMALL
        apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = Assets.Pictures.EARTH_SMALL
    return apl_datasource
