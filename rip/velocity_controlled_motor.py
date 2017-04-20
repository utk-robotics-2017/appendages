from .component import Component
from ..util.units import Constant, Angle, AngularVelocity


class VelocityControlledMotor(Component):
    DRIVE = "kSetVCMVoltage"
    SET = "kSetVCMVelocity"
    STOP = "kStopVCM"
    VELOCITY = "kGetVCMVelocity"
    VELOCITY_RESULT = "kGetVCMVelocityResult"
    POSITION = "kGetVCMPosition"
    POSITION_RESULT = "kGetVCMPositionResult"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.sim = sim
        self.motor = config['motor']
        self.encoder = config['encoder']
        self.vpid = config['pid']

        if self.sim:
            self.sim_velocity = Constant(0)
            self.sim_position = Constant(0)
        if not self.sim:
            self.driveIndex = commands[self.DRIVE]
            self.setIndex = commands[self.SET]
            self.stopIndex = commands[self.STOP]
            self.velocityIndex = commands[self.VELOCITY]
            self.velocityResultIndex = commands[self.VELOCITY_RESULT]
            self.positionIndex = commands[self.POSITION]
            self.positionResultIndex = commands[self.POSITION_RESULT]

    def get_command_parameters(self):
        yield self.driveIndex, [self.DRIVE, "ii"]
        yield self.setIndex, [self.SET, "id"]
        yield self.stopIndex, [self.STOP, "i"]
        yield self.velocityIndex, [self.VELOCITY, "i"]
        yield self.velocityResultIndex, [self.VELOCITY_RESULT, "d"]
        yield self.positionIndex, [self.POSITION, "i"]
        yield self.positionResultIndex, [self.POSITION_RESULT, "d"]

    def drive(self, value):
        if self.sim:
            # TODO: update sim_velocity based on sim_motor
            return

        self.spine.send(self.devname, False, self.DRIVE, self.index, value)

    def set(self, velocity):
        if self.sim:
            self.sim_velocity = velocity
            return

        self.spine.send(self.devname, False, self.SET, self.index, velocity.to(AngularVelocity.rpm))

    def get_velocity(self):
        if self.sim:
            return self.sim_velocity

        response = self.spine.send(self.devname, True, self.VELOCITY, self.index)
        response = AngularVelocity(response[0], AngularVelocity.rpm)
        return response

    def get_position(self):
        if self.sim:
            return self.sim_position

        response = self.spine.send(self.devname, True, self.POSITION, self.index)
        response = Angle(response[0], Angle.rev)
        return response

    def set_position(self, position):
        if self.sim:
            self.sim_position = position

    def stop(self):
        if self.sim:
            self.sim_velocity = Constant(0)
            return

        self.spine.send(self.devname, False, self.STOP, self.index)

    def get_dependency_update(self):
        dependencies = {}
        dependencies[self.motor]['sim_velocity'] = self.sim_velocity
        dependencies[self.encoder]['sim_velocity'] = self.sim_velocity
        return dependencies

    def sim_update(self, tm_diff):
        self.sim_position += self.sim_velocity * tm_diff

    def get_hal_data(self):
        hal_data = {}
        hal_data['velocity'] = self.sim_velocity
        hal_data['position'] = self.sim_position
        return hal_data

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "drive":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).drive(val)

        elif args[0] == "set":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(val)

        elif args[0] == "get_velocity":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_position()
            print("{}: {}".format(name, val))

        elif args[0] == "set_position":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_position(val)

        elif args[0] == "stop":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).stop()

        else:
            help(name)

    def help(self):
        print("usage: <vcm:str> drive <value:int>")
        print("       <vcm:str> set <velocity:float>")
        print("       <vcm:str> get_velocity")
        print("       <vcm:str> get_position")
        print("       <vcm:str> set_position <position:float>")
        print("       <vcm:str> stop")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["drive", "set", "get_velocity", "get_position", "set_position", "stop"]
                if i.startswith(text)]
