from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class DigitalOutput(Component):
    TIER = 1

    label = str
    pin = int

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        self.pin = -1
        Component.__init__(self, json_item, class_dict, device_dict)