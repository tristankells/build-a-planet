def set_apl_datasource_image_sources(apl_datasource, image_url):
    apl_datasource['bodyTemplate7Data']['image']['sources'][0]['url'] = image_url
    apl_datasource['bodyTemplate7Data']['image']['sources'][1]['url'] = image_url
    return apl_datasource
