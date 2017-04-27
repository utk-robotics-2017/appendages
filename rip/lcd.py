from .component import Component

from ..util.ourlogging import Logger

logger = Logger()


class Lcd(Component):
    WRITE = "kPrintLCD"
    CLEAR = "kClearLCD"
    SETPOS = "kSetCursorLCD"

    def __init__(self, spine, devname, config, commands, sim, rows=2, cols=16):
        self.spine = spine
        self.devname = devname
        self.label = config['label']
        self.index = config['index']
        self.sim = sim
        self.rows = rows
        self.cols = cols
        # lines is an array for keeping track of what is on each line.
        # contains char lists for each line/row.
        self.lines = []
        # self.cursor: (row, col)
        # keeps track of where the cursor is.
        self.cursor = (0, 0)

        if self.sim:
            for i in range(0, self.rows):
                self.lines.append(list("Sim Line " + str(i)))
        else:
            self.writeLCD = commands[self.WRITE]
            self.clearLCD = commands[self.CLEAR]
            self.setposLCD = commands[self.SETPOS]
            # The display is initially empty.
            for i in range(0, self.rows):
                self.lines.append(list(" " * cols))

    def get_command_parameters(self):
        yield self.writeLCD, [self.WRITE, "is"]
        yield self.clearLCD, [self.CLEAR, "i"]
        yield self.setposLCD, [self.SETPOS, "iii"]

    def write(self, message):
        '''write(str message)
        Writes a message to the LCD display at the current position.
        :return: nothing
        '''

        logger.info("Trying to set LCD message: " + message)

        if not self.sim:
            self.spine.send(self.devname, False, self.WRITE, self.index, message)
            logger.info("Written: \"" + message + "\" to the LCD #" + str(self.index))
        else:
            logger.info("Written: \"" + message + "\" to the LCD #" + str(self.index))

        self.lines[self.cursor[0]] = list(message)

        return

    def clear(self):
        '''clear()
        Clears the LCD display of all text.
        :return: nothing
        '''

        if not self.sim:
            self.spine.send(self.devname, False, self.CLEAR, self.index)
        logger.info("Cleared LCD display #" + str(self.index))

        for row in range(0, self.rows):
            self.lines[row] = list(" " * self.cols)

        return

    def setpos(self, vertical, horizontal):
        '''setpos(int vertical, int horizontal)
        Sets the cursor position for the LCD display.
        :return: nothing
        '''

        self.cursor = (vertical, horizontal)

        if not self.sim:
            self.spine.send(self.devname, False, self.SETPOS, self.index, vertical, horizontal)

        logger.info("Set cursor position for LCD #" + str(self.index))

        return

    def get_message(self):
        '''get_message()
        Returns a representation of what the display was last set to.
        :return: multi-line string, newline at end of each line
        '''
        return_message = ""

        for linelist in self.lines:
            return_message += "".join(linelist)
            return_message += "\n"

        return return_message

    def get_hal_data(self):
        message = self.get_message()
        return message

    # NOTE RIP_COM
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "write":
            if len(args) < 2:
                help(name)
                return
            self.message = " ".join(args[1:])
            print("Writing message to LCD: " + self.message)
            self.s.get_appendage(name).write(self.message)

        elif args[0] == "clear":
            self.s.get_appendage(name).clear()

        elif args[0] == "writepos":
            if len(args) < 3:
                help(name)
                return
            try:
                pos1 = int(args[1])
                pos2 = int(args[2])
            except ValueError as err:
                help(name)
                return
            self.s.get_appendage(name).setpos(pos1, pos2)
            if len(args) > 3:
                self.message = " ".join(args[3:])
                self.s.get_appendage(name).write(self.message)

        elif args[0] == "writeln":
            if len(args) < 2:
                help(name)
                return
            try:
                line = int(args[1])
            except ValueError as err:
                help(name)
                return
            # setpos is vertical, horizontal
            self.s.get_appendage(name).setpos(line, 0)
            if len(args) > 2:
                self.message = " ".join(args[2:])
                self.s.get_appendage(name).write(self.message)

        elif args[0] == "read":
            if len(args) > 1:
                help(name)
            try:
                print(self.s.get_appendage(name).get_message())
            except Exception as err:
                print("lol ther waz exceptshun: " + str(err))

        else:
            help(name)

    def help(self):
        print("usage: <lcd:str> write <value:str>")
        print("       <lcd:str> clear")
        print("       <lcd:str> read")
        print("       <lcd:str> writeln <value:int> ?<value:str>")
        print("       <lcd:str> writepos <value:int> <value:int> ?<value:str>")
        print("Notes: ")
        print("    read is software-side only, not accurate to real life.")
        print("    write is the raw write, subject to cursor position")
        print("    writepos calls setpos then write, function in rip_com not rip")
        print("     -> pass no message to writepos for direct access to setpos")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["write", "clear", "writepos", "writeln", "read"] if i.startswith(text)]
