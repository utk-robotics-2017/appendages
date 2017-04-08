from appendages.component_list import ComponentList


class Magnetometer:
    def __init__(self, label):
        self.label = label


class MagnetometerList(ComponentList):
    TIER = 1

    def __init__(self):
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        m = Magnetometer(json_item['label'])
        self.list_.append(m)
        return m

    def get_includes(self):
        return '#include <Wire.h>\n#include "Magnetometer.h"\n'

    def get_constructors(self):
        return "Magnetometer magnetometer;\n"

    def get_setup(self):
        return "\tWire.begin();\n\tmagnetometer.config();\n"

    def get_commands(self):
        return "\tkReadX,\n\tkReadXResult,\n\tkReadY,\n\tkReadYResult,\n\tkReadZ,\n\tkReadZResult,\n"

    def get_command_functions(self):
        rv = "void readX() {\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kReadX);\n"
        rv += "\tcmdMessenger.sendBinCmd(kReadXResult, magnetometer.readX());\n"
        rv += "}\n"

        rv += "void readY() {\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kReadY);\n"
        rv += "\tcmdMessenger.sendBinCmd(kReadYResult, magnetometer.readY());\n"
        rv += "}\n"

        rv += "void readZ() {\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kReadZ);\n"
        rv += "\tcmdMessenger.sendBinCmd(kReadZResult, magnetometer.readZ());\n"
        rv += "}\n"

        return rv

    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kReadX, readX);\n"
        rv += "\tcmdMessenger.attach(kReadY, readY);\n"
        rv += "\tcmdMessenger.attach(kReadZ, readZ);\n"
        return rv

    def get_indices(self):
        return [0, self.list_[0].label]

    def get_core_values(self):
        a = {}
        a['index'] = 0
        a['label'] = self.list_[0].label
        a['type'] = "Magnetometer"
        yield a
