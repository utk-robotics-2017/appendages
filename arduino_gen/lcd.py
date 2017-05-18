from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class Lcd(Component):
    TIER = 1

    label = str
    rs = int
    enable = int
    d4 = int
    d5 = int
    d6 = int
    d7 = int
    cols = int
    rows = int

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        self.rs = -1
        self.enable = -1
        self.d4 = -1
        self.d5 = -1
        self.d6 = -1
        self.d7 = -1
        self.cols = -1
        self.rows = -1
        Component.__init__(self, json_item, class_dict, device_dict)