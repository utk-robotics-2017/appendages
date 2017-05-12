from component import Component
from ..utils.decorators import attr_check, type_check


@attr_check
class Encoder(Component):
    TIER = 1

    label = str
    pin_a = int
    pin_b = int
    tick_per_revolution = float

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        Component.__init__(self, json_item, class_dict, device_dict)