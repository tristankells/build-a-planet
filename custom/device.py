class Device:
    apl_support: bool

    def __init__(self, viewport_profile):
        if viewport_profile == None:
            self._set_default_session_variables()
        if viewport_profile == 'HUB_LANDSCAPE_LARGE':
            self.apl_support = True
        elif viewport_profile == 'HUB_LANDSCAPE_MEDIUM':
            self.apl_support = True
        elif viewport_profile == 'HUB_LANDSCAPE_SMALL':
            self.apl_support = True
        elif viewport_profile == 'HUB_ROUND_SMALL':
            self.apl_support = True
        elif viewport_profile == 'TV_LANDSCAPE_XLARGE':
            self.apl_support = True
        elif viewport_profile == 'MOBILE_LANDSCAPE_SMALL':
            self.apl_support = True
        else: 
            self.apl_support = False

    def _set_default_session_variables(self):
        self.viewport_profile = False


