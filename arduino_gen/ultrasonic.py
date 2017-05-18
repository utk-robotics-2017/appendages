from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class Ultrasonic(Component):
    TIER = 1

    label = str
    trigger = int
    echo = int

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        self.trigger = -1
        self.echo = -1
        Component.__init__(self, json_item, class_dict, device_dict)