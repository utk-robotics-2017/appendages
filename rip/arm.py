from .component import Component


class Arm(Component):
    SET = "kSetArm"
    DETACH = "kDetachArm"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.base = config['base']
        self.shoulder = config['shoulder']
        self.elbow = config['elbow']
        self.wrist = config['wrist']
        self.wrist_rot = config['wrist_rot']

        self.sim = sim
        if sim:
            self.sim_base = 0
            self.sim_shoulder = 0
            self.sim_elbow = 0
            self.sim_wrist = 0
            self.sim_wrist_rotate = 0
            self.sim_attached = False
        else:
            self.setIndex = commands[self.SET]
            self.detachIndex = commands[self.DETACH]

    def get_command_parameters(self):
        yield self.setIndex, [self.SET, "iiiiii"]
        yield self.detachIndex, [self.DETACH, "i"]

    def set(self, rot):
        '''
        Move the arm to a position given in raw servo values.
        :warning:
            You probably do not want to call this method directly. Please see
            the documentation on the Arm class which can greatly simplify the
            process of programming for the arm. It can help with the translation
            between cartesian coordinates and servo values, and it can also
            handle the interpolation between arm positions.
        :param rot:
            A tuple of length 5 with values between 1 and 180 that specify the
            amount of rotation for each servo in the arm. The servo order is
            (base, shoulder, elbow, wrist, wristrotate).
        :type rot: ``tuple``
        '''
        if self.sim:
            self.sim_base = rot[0]
            self.sim_shoulder = rot[1]
            self.sim_elbow = rot[2]
            self.sim_wrist = rot[3]
            self.sim_wrist_rot = rot[4]
            self.sim_attached = True
            return

        assert len(rot) == 5
        for r in rot:
            assert 0 <= r <= 180
        self.spine.send(self.devname, False, self.SET, self.index, *rot)

    def detach(self):
        if self.sim:
            self.sim_attached = False
            return

        self.spine.send(self.devname, False, self.DETACH, self.index)

    def get_dependency_update(self):
        dependencies = {}
        dependencies[self.base]['sim_value'] = self.sim_base
        dependencies[self.shoulder]['sim_value'] = self.sim_shoulder
        dependencies[self.elbow]['sim_value'] = self.sim_elbow
        dependencies[self.wrist]['sim_value'] = self.sim_wrist
        dependencies[self.wrist_rot]['sim_value'] = self.sim_wrist_rot
        return dependencies

    def get_hal_data(self):
        hal_data = {}
        hal_data['base'] = self.sim_base
        hal_data['shoulder'] = self.sim_shoulder
        hal_data['elbow'] = self.sim_elbow
        hal_data['wrist'] = self.sim_wrist
        hal_data['wrist_rot'] = self.sim_wrist_rot
        hal_data['attached'] = self.sim_attached
        return hal_data

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set":
            if len(args) != 6:
                help(name)
                return

            rot = []
            try:
                for i in range(1, 6):
                    value = int(args[i])
                    if value < 0 or value > 180:
                        help(name)
                        return
                    rot.append(value)
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(rot)

        elif args[0] == "detach":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).detach()

        else:
            help(name)

    def help(self):
        print("usage: <arm:str> set <rot[0]> <rot[1]> <rot[2]> <rot[3]> <rot[4]>")
        print("       <arm:str> detach")
        print("")
        print("rot values: [0, 180]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set", "detach"] if i.startswith(text)]
