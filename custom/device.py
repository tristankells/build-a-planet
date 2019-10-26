class Device:
    apl_support: bool

    def __init__(self, viewport_profile):
        if viewport_profile is None:
            self._set_default_session_variables()
        elif viewport_profile == 'ViewportProfile.HUB_LANDSCAPE_LARGE':
            self.apl_support = True
        elif viewport_profile == 'ViewportProfile.HUB_LANDSCAPE_MEDIUM':
            self.apl_support = True
        elif viewport_profile == 'ViewportProfile.HUB_LANDSCAPE_SMALL':
            self.apl_support = True
        elif viewport_profile == 'ViewportProfile.HUB_ROUND_SMALL':
            self.apl_support = True
        elif viewport_profile == 'ViewportProfile.TV_LANDSCAPE_XLARGE':
            self.apl_support = True
        elif viewport_profile == 'ViewportProfile.MOBILE_LANDSCAPE_SMALL':
            self.apl_support = True
        else: 
            self.apl_support = True

    def _set_default_session_variables(self):
        self.viewport_profile = False


