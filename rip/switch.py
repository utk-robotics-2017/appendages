from .component import Component


class Switch(Component):
    READ = "kReadSwitch"
    READ_RESULT = "kReadSwitchResult"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.sim = sim

        if self.sim:
            self.sim_state = False
        else:
            self.readIndex = commands[self.READ]
            self.readResultIndex = commands[self.READ_RESULT]

    def get_command_parameters(self):
        yield self.readIndex, [self.READ, "i"]
        yield self.readResultIndex, [self.READ_RESULT, "i"]

    def set_state(self, state):
        if self.sim:
            self.sim_state = state

    def read(self):
        if self.sim:
            return self.sim_state

        response = self.spine.send(self.devname, True, self.READ, self.index)
        return [False, True][response[0]]

    def sim_update(self, tm_diff):
        pass

    def get_hal_data(self):
        hal_data = {}
        hal_data['state'] = self.sim_state
        return hal_data

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "read":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{}: {}".format(name, val))

        elif args[0] == "read_until_change":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{} start state: {}".format(name, val))
            time.sleep(0.1)

            while val == self.s.get_appendage(name).read():
                time.sleep(0.1)
            print("{} state changed".format(name, val))

        else:
            help(name)

    def help(self):
        print("usage: <switch:str> read")
        print("       <switch:str> read_until_change")
        print("")
        print("value: [-1023, 1023]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["read", "read_until_change"] if i.startswith(text)]