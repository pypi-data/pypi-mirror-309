from onoff_mixin import OnOffMixin
from switchbot_device import SwitchbotDevice


class SwitchbotPlug(SwitchbotDevice, OnOffMixin):
    """Switchbot Plug class"""

    def __init__(self, deviceId):
        """Constructor"""
        super().__init__(deviceId)

    def get_power(self) -> str:
        """Returns device power status"""
        status = self.get_status()
        return status["power"]
