from .component import Component
from ...units import *


class I2CEncoder(Component):
    POSITION = "kI2CEncoderPosition"
    POSITION_RESULT = "kI2CEncoderPositionResult"
    RAW_POSITION = "kI2CEncoderRawPosition"
    RAW_POSITION_RESULT = "kI2CEncoderRawPositionResult"
    SPEED = "kI2CEncoderSpeed"
    SPEED_RESULT = "kI2CEncoderSpeedResult"
    VELOCITY = "kI2CEncoderVelocity"
    VELOCITY_RESULT = "kI2CEncoderVelocityResult"
    ZERO = "kI2CEncoderZero"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.pidSource = 'position'
        self.sim = sim

        if self.sim:
            self.sim_position = Constant(0)
            self.sim_velocity = Constant(0)
        else:
            self.positionIndex = commands[self.POSITION]
            self.positionResultIndex = commands[self.POSITION_RESULT]
            self.rawPositionIndex = commands[self.RAW_POSITION]
            self.rawPositionResultIndex = commands[self.RAW_POSITION_RESULT]
            self.speedIndex = commands[self.SPEED]
            self.speedResultIndex = commands[self.SPEED_RESULT]
            self.velocityIndex = commands[self.VELOCITY]
            self.velocityResultIndex = commands[self.VELOCITY_RESULT]
            self.zeroIndex = commands[self.ZERO]

    def get_command_parameters(self):
        yield self.positionIndex, [self.POSITION, "i"]
        yield self.positionResultIndex, [self.POSITION_RESULT, "d"]
        yield self.rawPositionIndex, [self.RAW_POSITION, "i"]
        yield self.rawPositionResultIndex, [self.RAW_POSITION_RESULT, "d"]
        yield self.speedIndex, [self.SPEED, "i"]
        yield self.speedResultIndex, [self.SPEED_RESULT, "d"]
        yield self.velocityIndex, [self.VELOCITY, "i"]
        yield self.velocityResultIndex, [self.VELOCITY_RESULT, "d"]
        yield self.zeroIndex, [self.ZERO, "i"]

    def set_pid_source(self, source):
        self.pidSource = source

    def get_position(self):
        if self.sim:
            return self.sim_position

        response = self.spine.send(self.devname, True, self.POSITION, self.index)
        response = Angle(response[0], Angle.rev)
        return response

    def set_position(self, position):
        if self.sim:
            self.sim_position = position

    def raw_position(self):
        if self.sim:
            return 0

        return self.spine.send(self.devname, True, self.RAW_POSITION, self.index)[0]

    def get_speed(self):
        if self.sim:
            return abs(self.sim_velocity)

        response = self.spine.send(self.devname, True, self.SPEED, self.index)
        response = AngularVelocity(response[0], AngularVelocity.rpm)
        return response

    def set_velocity(self, velocity):
        if self.sim:
            self.sim_velocity = velocity

    def get_velocity(self):
        if self.sim:
            return self.sim_velocity

        response = self.spine.send(self.devname, True, self.VELOCITY, self.index)
        response = AngularVelocity(response[0], AngularVelocity.rpm)
        return response

    def zero(self):
        if self.sim:
            self.sim_position = Constant(0)
            self.sim_velocity = Constant(0)
            return

        self.spine.send(self.devname, False, self.ZERO, self.index)

    def pid_get(self):
        if self.pidSource == 'position':
            return self.position()
        elif self.pidSource == 'velocity':
            return self.velocity()

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

        elif args[0] == "set_pid_source":
            if len(args) != 2:
                help(name)
                return

            pid_source = args[1]

            if pid_source not in ["position", "velocity"]:
                help(name)
                return

            self.s.get_appendage(name).set_pid_source(pid_source)

        elif args[0] == "get_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_position()
            print("{}: {}".format(name, val.base_value))

        elif args[0] == "set_position":
            if len(args) != 2:
                help(name)
                return

            try:
                pos = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_position(Angle(pos, Angle.rev))

        elif args[0] == "raw_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).raw_position()
            print("{}: {}".format(name, val.base_value))

        elif args[0] == "get_speed":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_speed()
            print("{}: {}".format(name, val.base_value))

        elif args[0] == "set_velocity":
            if len(args) != 2:
                help(name)
                return

            try:
                vel = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_velocity(AngularVelocity(vel, AngularVelocity.rpm))

        elif args[0] == "get_velocity":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_velocity()
            print("{}: {}".format(name, val.base_value))

        elif args[0] == "zero":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).zero()

        elif args[0] == "pid_get":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).pid_get()
            print("{}: {}".format(name, val.base_value))

        else:
            help(name)

    def help(self):
        print("usage: <i2c_encoder:str> set_pid_source <source:str>")
        print("       <i2c_encoder:str> get_position")
        print("       <i2c_encoder:str> set_position <position:float>")
        print("       <i2c_encoder:str> raw_position")
        print("       <i2c_encoder:str> get_speed")
        print("       <i2c_encoder:str> set_velocity <velocity:float>")
        print("       <i2c_encoder:str> get_velocity")
        print("       <i2c_encoder:str> zero")
        print("       <i2c_encoder:str> pid_get")
        print("")
        print("pid_source: [\"position\", \"velocity\"]")
        print("position: rev")
        print("velocity: rpm")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_pid_source", "get_position", "set_position",
                            "raw_position", "get_speed", "set_velocity",
                            "get_velocity", "zero", "pid_get"] if i.startswith(text)]
