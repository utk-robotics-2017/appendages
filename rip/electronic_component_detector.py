class ElectronicComponentDetector:
    DECODE = "kDecode"
    DECODE_RESULT = "kDecodeResult"

    def __init__(self, spine, devname, config, commands, sim):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.sim = sim

        if sim:
            pass
        else:
            self.decodeIndex = commands[self.DECODE]
            self.decodeResultIndex = commands[self.DECODE_RESULT]

    def get_command_parameters(self):
        yield self.decodeIndex, [self.DECODE, "c"]
        yield self.decodeResultIndex, [self.DECODE_RESULT, "i"]

    def decode(self, pad='9'):
        response = self.spine.send(self.devname, True, self.DECODE, pad)[0]
        code = []
        for i in range(5):
            code.append(response >> (i * 3) & 7)
        return code

    ### RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "decode":
            pad = -1
            if len(args) == 0:
                help(name)
                return
            if len(args) == 1:
                pad = 9
            if len(args) == 2:
                try:
                    pad = int(args[1])
                except ValueError:
                    help(name)
                    return

                if pad not in [0, 1, 2, 3, 4, 9]:
                    help(name)
                    return
            else:
                help(name)
                return

            val = self.s.get_appendage(name).decode(pad=str(pad))
            print("{}: {}".format(name, val))

        else:
            help(name)

    def help(self):
        print("usage: <ECD:str> decode")
        print("usage: <ECD:str> decode <pad:int>")
        print("")
        print("pad: [0, 1, 2, 3, 4, 9]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["decode"] if i.startswith(text)]
