from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class DigitalInput(Component):
    TIER = 1

    label = str
    pin = int
    pullup = bool

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        self.pin = -1
        self.pullup = False
        Component.__init__(self, json_item, class_dict, device_dict)