from .component import Component


class SoftwarePwm(Component):
    SET_PWM = "kSetPWM"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']

        self.sim = sim

        if self.sim:
            self.sim_value = 0
        else:
            self.setPWMIndex = commands[self.SET_PWM]

    def get_command_parameters(self):
        yield self.setPWMIndex, [self.SET_PWM, "ii"]

    def set_pwm(self, value):
        '''Set the value for software pwm'''
        if self.sim:
            self.sim_value = value
        else:
            self.spine.send(self.devname, False, self.SET_PWM, self.index, value)

    def sim_update(self, tm_diff):
        pass

    def get_hal_data(self):
        hal_data = {}
        hal_data['sim_value'] = self.sim_value
        return hal_data

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)
        elif args[0] == "set_pwm":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_pwm(val)

        else:
            help(name)

    def help(self):
        print("usage: <stepper:str> set_pwm <value:int>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_pwm"] if i.startswith(text)]
