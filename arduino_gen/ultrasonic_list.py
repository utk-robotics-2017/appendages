from appendages.component_list import ComponentList


class Ultrasonic:
    def __init__(self, label, trigger, echo):
        self.label = label
        self.trigger = trigger
        self.echo = echo


class UltrasonicList(ComponentList):
    TIER = 1

    def __init__(self):
        self.list_ = []

    def add(self, json_item, device_dict, device_type):
        ultrasonic = Ultrasonic(json_item['label'], json_item['trigger'], json_item['echo'])
        self.list_.append(ultrasonic)
        return ultrasonic

    def get_includes(self):
        return '#include "NewPing.h"\n'

    def get_pins(self):
        rv = ""
        for sensor in self.list_:
            rv += "const char {0:s}_trigger = {1:d};\n".format(sensor.label, sensor.trigger)
            rv += "const char {0:s}_echo = {1:d};\n".format(sensor.label, sensor.echo)
        rv += "\n"
        return rv

    def get_constructors(self):
        rv = ""
        for i, sensor in enumerate(self.list_):
            rv += "const char {0:s}_index = {1:d};\n".format(sensor.label, i)
        rv += "NewPing ultrasonics[{0:d}] = {{\n".format(len(self.list_))

        for sensor in self.list_:
            rv += "\tNewPing({0:s}_trigger, {0:s}_echo),\n".format(sensor.label)
        rv = rv[:-2] + "\n};\n"
        return rv

    def get_commands(self):
        return "\tkReadUltrasonic,\n\tkReadUltrasonicResult,\n"

    def get_command_attaches(self):
        return "\tcmdMessenger.attach(kReadUltrasonic, readUltrasonic);\n"

    def get_command_functions(self):
        rv = "void readUltrasonic() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadUltrasonic);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kReadUltrasonic);\n"
        rv += "\tcmdMessenger.sendBinCmd(kReadUltrasonicResult, ultrasonics[indexNum].ping_cm());\n"
        rv += "}\n\n"
        return rv

    def get_core_values(self):
        for i, ultrasonic in enumerate(self.list_):
            a = {}
            a['index'] = i
            a['label'] = ultrasonic.label
            a['type'] = "Ultrasonic"
            yield a
