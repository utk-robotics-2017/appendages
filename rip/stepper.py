from .component import Component
from ..util.units import Angle, Constant


class Stepper(Component):
    SET_SPEED = "kSetStepperSpeed"
    STEP = "kStepStepper"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.angle_per_step = Angle(config['angle_per_step'], Angle.degree)
        self.sim = sim
        self.step_position = Constant(0)
        self.angle = Constant(0)

        if self.sim:
            self.sim_velocity = Constant(0)
        else:
            self.setSpeedIndex = commands[self.SET_SPEED]
            self.stepIndex = commands[self.STEP]

    def get_command_parameters(self):
        yield self.setSpeedIndex, [self.SET_SPEED, "ii"]
        yield self.stepIndex, [self.STEP, "ii"]

    def set_speed(self, velocity):
        '''
        Set speed for a stepper motor.
        :param value:
            Speed for the stepper to turn at
        :type value: ``int``
        '''
        if self.sim:
            # Current sim assumption is instant move
            self.sim_velocity = velocity
            return

        self.spine.send(self.devname, False, self.SET_SPEED, self.index, velocity)

    def set_angle(self, angle):
        '''
        Set angle for a stepper motor
        :param angle:
            Angle to set the stepper to

        '''
        steps = (angle - self.angle) / self.angle_per_step
        self.step(steps)

    def step(self, steps):
        '''
        Step the motor forward value amount

        :param value:
            Number of steps the motor will turn
        :type value: ``int``
        '''
        if self.sim:
            # Current sim assumption is instant move
            # TODO: add speed to simulation
            self.step_position += steps
            return

        self.spine.send(self.devname, False, self.STEP, self.index, value)
        self.angle += Constant(steps) * self.angle_per_step

    def sim_update(self, tm_diff):
        pass

    def get_hal_data(self):
        hal_data = {}
        hal_data['velocity'] = self.sim_velocity
        hal_data['step_position'] = self.step_position
        hal_data['angle'] = self.angle
        return hal_data

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_speed":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_speed(val)

        elif args[0] == "set_angle":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_angle(val)

        elif args[0] == "step":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).step(val)

        else:
            help(name)

    def help(self):
        print("usage: <stepper:str> set_speed <speed:float>")
        print("       <stepper:str> set_angle <angle:float>")
        print("       <stepper:str> step <steps:int>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_speed", "set_angle", "step"] if i.startswith(text)]
