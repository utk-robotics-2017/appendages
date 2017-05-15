from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class Magnetometer(Component):
    TIER = 1

    label = str

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        Component.__init__(self, json_item, class_dict, device_dict)