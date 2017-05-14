from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class Encoder(Component):
    TIER = 1

    label = str
    pin_a = int
    pin_b = int
    ticks_per_revolution = (int, float)

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        self.pin_a = -1
        self.pin_b = -1
        self.ticks_per_revolution = -1
        Component.__init__(self, json_item, class_dict, device_dict)
