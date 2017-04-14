# ArduinoGen Appendages


## Description
These appendages are the template system that are used to write Arduino Code that interfaces with RIP.


## Appendage Creation

### filename
The file should be in all lower case with underscores in between each word. 'list' should be the last word.

Example: encoder_list.py

### Main Class
The main class is a list of the individual appendages of this type. It should follow the pascal case and end in 'List'.

Example: class EncoderList

#### Inheiritance
Each list class should be a child class of Component

Example: Encoder ->

```python
from .component_list import ComponentList


class EncoderList(ComponentList):
...
```

#### TIER
TIER is a static variable that must be in each list class. An appendage that does not depend on any
other appendage is tier 1. If an appendage depends on a tier 1 appendage then it is of tier 2. If it depends on a tier 2 appendage then it is of tier 3 and so on.


#### Constructor
The constructor should have no parameters (other than the obvious self) and should create the list that will hold all the individual appendages of that type.

```python
    def __init__(self):
        self.list_ = []
```

#### add
Required: True
##### Parameters
json_item (`dict`): dictionary containing the information from the config (usually created through the web interface)
device_dict (`dict`): dictionary containing the appendage lists for the previously generated appendage types
device_type (`dict`): dictionary containing the classes (not the objects) of all the appendages

This function should fill out an appendage struct with the information gathered from the web interface and add it to the list. It should also return the struct.

Example:

```python
def add(self, json_item, device_dict, device_type):
        encoder = Encoder(json_item['label'], json_item['pin_a'], json_item['pin_b'], json_item['ticks_per_rev'])
        self.list_.append(encoder)
        return encoder
```

#### get_includes
Required: False
This function has no parameters and returns a string that is the includes needed by Arduino.

```python
    def get_includes(self):
        return '#include "Encoder.h"\n'
```

#### get_pins
Required: False
It is easier to later read the Arduino Code (if we ever have to) if we store the various pins used in constants that use the appendage labels. This function returns a string that makes these constants. These constants will be below the includes and above setup as expected.

Example:
```python
    def get_pins(self):
        rv = ""
        for encoder in self.list_:
            rv += "const char {0:s}_pin_a = {1:d};\n".format(encoder.label, encoder.pin_a)
            rv += "const char {0:s}_pin_b = {1:d};\n".format(encoder.label, encoder.pin_b)
        rv += "\n"
        return rv
```

#### get_constructors
Required: False
This function has no parameters and returns a string that is all the contructors for the Arduino objects needed for this appendage.

Example:
```python
    def get_constructors(self):
        rv = "Encoder encoders[{0:d}] = {{\n".format(len(self.list_))
        for encoder in self.list_:
            rv += "\tEncoder({0:s}_pin_a, {0:s}_pin_b),\n".format(encoder.label)
        rv = rv[:-2] + "\n};\n"
        return rv
```

#### get_setup
Required: False
This function has no parameters and returns a string that is the functions for this appendage that need to run during the Arduino's setup function.

Example:
```python
    def get_setup(self):
        rv = ""
        for encoder in self.list_:
            rv += "\tpinMode({0:s}_pin_a, INPUT);\n".format(encoder.label)
            rv += "\tpinMode({0:s}_pin_b, INPUT);\n".format(encoder.label)
        return rv
```

#### get_commands
Required: True

Example:
```python
    def get_commands(self):
        return "\tkReadEncoder,\n\tkReadEncoderResult,\n\tkZeroEncoder,\n"
```

#### get_command_attaches
Required: True

Example:
```python
    def get_command_attaches(self):
        rv = "\tcmdMessenger.attach(kReadEncoder, readEncoder);\n"
        rv += "\tcmdMessenger.attach(kZeroEncoder, zeroEncoder);\n"
        return rv
```

#### get_command_functions
Required: True

Example:
```python
    def get_command_functions(self):
        rv = "void readEncoder() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kReadEncoder);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kReadEncoder);\n"
        rv += "\tcmdMessenger.sendBinCmd(kReadEncoderResult, encoders[indexNum].read());\n"
        rv += "}\n\n"

        rv += "void zeroEncoder() {\n"
        rv += "\tint indexNum = cmdMessenger.readBinArg<int>();\n"
        rv += "\tif(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > {0:d}) {{\n".format(len(self.list_))
        rv += "\t\tcmdMessenger.sendBinCmd(kError, kZeroEncoder);\n"
        rv += "\t\treturn;\n"
        rv += "\t}\n"
        rv += "\tencoders[indexNum].write(0);\n"
        rv += "\tcmdMessenger.sendBinCmd(kAcknowledge, kZeroEncoder);\n"
        rv += "}\n\n"
        return rv
```

#### get_loop_functions
Required: False

#### get_extra_functions
Required: False

#### get_core_values
Required: True

```python
    def get_core_values(self):
        for i, encoder in enumerate(self.list_):
            a = {}
            a['index'] = i
            a['label'] = encoder.label
            a['type'] = "Encoder"
            a['ticks_per_rev'] = encoder.ticks_per_rev
            yield a
```