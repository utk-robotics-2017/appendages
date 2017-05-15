from .component import Component
from .servo import Servo
from ..util.decorators import attr_check, type_check


@attr_check
class Magnetometer(Component):
    TIER = 1

    label = str
    base = Servo
    shoulder = Servo
    elbow = Servo
    wrist = Servo
    wrist_rotate = Servo

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        base = None
        shoulder = None
        elbow = None
        wrist = None
        wrist_rotate = None
        Component.__init__(self, json_item, class_dict, device_dict)