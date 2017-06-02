from .component import Component
from ..util import units


class Ultrasonic(Component):
    READ = "kReadUltrasonic"
    READ_RESULT = "kReadUltrasonicResult"

    def __init__(self, spine: object, devname: str, config: dict, commands: dict, sim: bool):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.sim = sim

        if self.sim:
            self.sim_distance = units.Constant(0)
        else:
            self.readIndex = commands[self.READ]
            self.readResultIndex = commands[self.READ_RESULT]

    def get_command_parameters(self):
        yield self.readIndex, [self.READ, "i"]
        yield self.readResultIndex, [self.READ_RESULT, "L"]

    def set_distance(self, distance) -> None:
        if self.sim:
            self.sim_distance = distance

    def read(self):
        '''
        Reads the ultrasonics
        :return: distance in specified unit
        '''
        if self.sim:
            return self.sim_distance

        response = self.spine.send(self.devname, True, self.READ, self.index)

        if response == 0:
            response = float('inf')

        converted_response = units.Length(float(response[0]), units.Length.cm)

        return converted_response

    def sim_update(self, tm_diff) -> None:
        pass

    def get_hal_data(self):
        hal_data = {}
        hal_data['distance'] = self.sim_distance
        return hal_data

    ### RIP_COM
    def interact(self, parseResults: list) -> None:
        def help(name) -> None:
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_distance":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_distance(val)

        elif args[0] == "read":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{}: {} cm".format(name, val.to(Length.cm)))

        else:
            help(name)

    def help(self):
        print("usage: <ultrasonic:str> set_distance <distance:float>")
        print("       <ultrasonic:str> read")

    def complete(self, text: str, line: str, begidx: int, endidx: int):
        return [i for i in ["set_distance", "read"] if i.startswith(text)]
