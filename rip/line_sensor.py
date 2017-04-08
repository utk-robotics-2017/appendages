from .component import Component


class LineSensor(Component):
    READ_DIGITAL = "kReadDigitalLineSensor"
    READ_DIGITAL_RESULT = "kReadDigitalLineSensorResult"
    READ_ANALOG = "kReadAnalogLineSensor"
    READ_ANALOG_RESULT = "kReadAnalogLineSensorResult"

    def __init__(self, spine, devname, label, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.digital = config['digital']
        self.sim = sim

        if self.sim:
            self.sim_value = 0
        else:
            if self.READ_DIGITAL in commands:
                self.readDigitalIndex = commands[self.READ_DIGITAL]
                self.readDigitalResultIndex = commands[self.READ_DIGITAL_RESULT]

            if self.READ_ANALOG in commands:
                self.readAnalogIndex = commands[self.READ_ANALOG]
                self.readAnalogResultIndex = commands[self.READ_ANALOG_RESULT]

    def get_command_parameters(self):
        if hasattr(self, 'readDigitalIndex'):
            yield self.readDigitalIndex, [self.READ_DIGITAL, "i"]
            yield self.readDigitalResultIndex, [self.READ_DIGITAL_RESULT, "i"]

        if hasattr(self, 'readAnalogIndex'):
            yield self.readAnalogIndex, [self.READ_ANALOG, "i"]
            yield self.readAnalogResultIndex, [self.READ_ANALOG_RESULT, "i"]

    def set_value(self, value):
        if self.sim:
            self.sim_value = value

    def read(self):
        if self.sim:
            return self.sim_value

        if self.digital:
            return self.spine.send(self.devname, True, self.READ_DIGITAL, self.index)
        else:
            return self.spine.send(self.devname, True, self.READ_ANALOG, self.index)

    def sim_update(self, tm_diff):
        # TODO
        pass

    def get_hal_data(self):
        hal_data = {}
        hal_data['value'] = self.sim_value
        return hal_data

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_value":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_value(val)

        elif args[0] == "read":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{}: {}".format(name, val))

        else:
            help(name)

    def help(self):
        print("       <line_sensor:str> set_value <value:int>")
        print("       <line_sensor:str> read")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_value", "read"] if i.startswith(text)]

