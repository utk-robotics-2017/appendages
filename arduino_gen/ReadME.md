# ArduinoGen Appendages


## Description
These appendages are the template system that are used to write Arduino Code that interfaces with RIP.


## Appendage Creation

### Struct

#### filename
The file should be in all lower case with underscores in between each word.

Example: encoder.py


### Class
The main class is a list of the individual appendages of this type.

Example:
```python
from .component import Component
from ..util.decorators import attr_check, type_check

@attr_check
class Example(Component):
    TIER = 1

    label = str
    val1 = int
    val2 = float
    val3 = str

    @type_check
    def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
        self.label = ""
        self.val1 = -1
        self.val2 = -1.0
        self.val3 = ""
        Component.__init__(self, json_item, class_dict, device_dict)
```

#### Inheiritance
Each struct should be a child class of Component

#### TIER
TIER is a static variable that must be in each list class. An appendage that does not depend on any
other appendage is tier 1. If an appendage depends on a tier 1 appendage then it is of tier 2. If it depends on a tier 2 appendage then it is of tier 3 and so on.


### Template

#### Sections


##### include
Required: False
List the include without the "#include"

```
include{{{
    <example>
    "example.h"
}}}
```

##### pins
Required: False
The pins for each appendage will be added (usually using a loop subsection)

Example:
```
pins{{{
    loop{{{
        const char <<<label>>_pin = <<<pin>>>;
    }}}
}}}
```

##### constructors
Required: False
This function has no parameters and returns a string that is all the contructors for the Arduino objects needed for this appendage.

Example:
```
constructors{{{
    Example examples[%%%length%%%] = {
        loop_separated_by(',') {{{
            Example(<<<val1>>>, <<<val2>>>, <<<val3>>>)
        }}}
    }
}}}
```

##### setup
Required: False

Example:
```
setup{{{
    loop{{{
        pinMode(<<<label>>>_pin, INPUT);
    }}}
}}}
```

##### commands
Required: True

Example:
```
commands{{{
    kExampleCommand,
    kExampleCommand2,
    kExampleCommand2Result,
    kExampleCommand3,
}}}
```

##### command_attaches
Required: True

Example:
```
command_attaches{{{
    cmdMessenger.attach(kExampleCommand, exampleCommand);
    cmdMessenger.attach(kExampleCommand2, exampleCommand2);
    cmdMessenger.attach(kExampleCommand3, exampleCommand3);
}}}
```

##### get_command_functions
Required: True

Example:
```
command_functions{{{
    void exampleCommand(){
        int indexNum = cmdMessenger.readBinArg<int>();
        if(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > %%%length%%%) {
            cmdMessenger.sendBinCmd(kError, kExampleCommand);
            return;
        }

        ...Do something...

        cmdMessenger.sendBinCmd(kAcknowledge, kExampleCommand);
    }

    void exampleCommand2(){
        int indexNum = cmdMessenger.readBinArg<int>();
        if(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > %%%length%%%) {
            cmdMessenger.sendBinCmd(kError, kExampleCommand2);
            return;
        }

        ...Do something...

        cmdMessenger.sendBinCmd(kAcknowledge, kExampleCommand2);
        cmdMessenger.sendBinCmd(kExampleCommand2Result, value);
    }

    void exampleCommand3(){
        int indexNum = cmdMessenger.readBinArg<int>();
        if(!cmdMessenger.isArgOk() || indexNum < 0 || indexNum > %%%length%%%) {
            cmdMessenger.sendBinCmd(kError, kExampleCommand3);
            return;
        }

        int value = cmdMessenger.readBinArg<int>();
        if(!cmdMessenger.isArgOk()){
            cmdMessenger.sendBinCmd(kError, kExampleCommand3);
            return;
        }

        ...Do something...

        cmdMessenger.sendBinCmd(kAcknowledge, kExampleCommand3);
    }
}}}
```

##### loop_functions
Required: False

```
loop_functions{{{
    ...something...
}}}
```


##### extra_functions
Required: False
```
extra_functions{{{
    ...something...
}}}
```

##### core_values
Required: True
Note: loop is not required for this

```
core_values{{{
    val1 = <<<val1>>>
    val2 = <<<val2>>>
    val3 = <<<val3>>>
}}}
```

#### subsections

##### loop
Loops through the list of appendages of that type. 

```
loop{{{
    ...something...
}}}
```

##### loop_separated_by
Loops through the list of appendages of that type. Each line is separated by the character or characters specified.

```
loop_separated_by(','){{{
    ...something...
}}}
```

##### if, else if, else

```
if(...condition...){{{
    ...something...
}}}
else if(...condition...){{{
    ...something else...
}}}
else (...condition...){{{
    ...another something...
}}}
```

#### local variables
Local variables are surrounded by '<<<' and '>>>'. 

#### global variables
Global variables are surrounded by '%%%'. The current only global variable is '%%%length%%%' which gets the length of the list of appendages of that type.