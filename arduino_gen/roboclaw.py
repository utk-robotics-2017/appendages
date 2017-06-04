from .component import Component
from ..util.decorators import attr_check, type_check


@attr_check
class Roboclaw(Component):
    TIER = 1

    label = str
    
    motor1_enable = bool
    motor1_position_p = float
    motor1_position_i = float
    motor1_position_d = float
    motor1_velocity_p = float
    motor1_velocity_i = float
    motor1_velocity_d = float
    motor1_qpps = float

    motor2_enable = bool
    motor2_position_p = float
    motor2_position_i = float
    motor2_position_d = float
    motor2_velocity_p = float
    motor2_velocity_i = float
    motor2_velocity_d = float
    motor2_qpps = float

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        
        Component.__init__(self, json_item, class_dict, device_dict)