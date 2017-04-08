from appendages.component_list import ComponentList


class Servo:
    def __init__(self, label, pin, servo_type):
        self.label = label
        self.pin = pin
        self.servo_type = servo_type


class ServoList(ComponentList):
    TIER = 1

    def __init__(self):
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        servo = Servo(json_item['label'], json_item['pin'], json_item['servo_type'])
        self.list_.append(servo)
        return servo

    def get_includes(self):
        return '#include "Servo.h"\n'

    def get_pins(self):
        rv = ""
        for actuator in self.list_:
            rv += "const char {0:s}_pin = {1:d};\n".format(actuator.label, actuator.pin)
        rv += "\n"
        return rv

    def get_constructors(self):
        rv = ""
        for i, servo in enumerate(self.list_):
            rv += "const char {0:s}_index = {1:d};\n".format(servo.label, i)

        rv += "char servo_pins[{0:d}] = {{\n".format(len(self.list_))
        for servo in self.list_:
            rv += ("\t{0:s}_pin,\n").format(servo.label)
        rv = rv[:-2] + "\n};\n"

        rv += ("Servo servos[{0:d}];\n").format(len(self.list_))
        return rv

    def get_setup(self):
        rv = ""
        for servo in self.list_:
            rv += "\tservos[{0:s}_index].attach({0:s}_pin);\n".format(servo.label)
        rv += "\n"

        return rv

    def get_commands(self):
        return "\tkSetServo,\n\tkDetachServo,\n"

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kSetServo, setServo);\n"
        rv += "\tcmdMessenger.attach(kDetachServo, detachServo);\n"
        return rv

    def get_command_functions(self):
        rv = "void setServo() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetServo);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tint value = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk()){\n"
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kSetServo);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tif(!servos[indexNum].attached()){\n"
        rv += "\t\tservos[indexNum].attach(servo_pins[indexNum]);\n"
        rv += "\t}\n"
        rv += "\tservos[indexNum].write(value);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kSetServo);\n"
        rv += "}\n\n"

        rv += "void detachServo() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kDetachServo);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tservos[indexNum].detach();\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kDetachServo);\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, servo in enumerate(self.list_):
            config = {}
            config['index'] = i
            config['label'] = servo.label
            config['type'] = "Servo"
            config['servo_type'] = servo.servo_type
            yield config
