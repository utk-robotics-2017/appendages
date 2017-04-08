# ArduinoGen Appendages


## Description
These appendages are the template system that are used to write Arduino Code that interfaces with RIP.


## Appendage Creation

### filename
The file should be in all lower case with underscores in between each word. 'list' should be the last word.

Example: Encoder -> encoder_list.py

### Main Class
The main class is a list of the individual appendages of this type. It should follow the pascal case and end in 'List'.

Example: Encoder -> class EncoderList

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


#### add
Required: True
##### Parameters
json_item (`dict`): dictionary containing the information from the config (usually created through the web interface)
device_dict (`dict): dictionary containing the appendage lists for the previously generated appendage types
device_type (`dict): dictionary containing the classes (not the objects) of all the appendages

This function should fill out an appendage struct with the information gathered from the web interface and add it to the list. It should also return the struct.

Example: Encoder ->

```python
def add(self, json_item, device_dict, device_type):
        encoder = Encoder(json_item['label'], json_item['pin_a'], json_item['pin_b'], json_item['ticks_per_rev'])
        self.list_.append(encoder)
        return encoder
```

#### get_includes
Required: False


#### get_pins
Required: False

#### get_constructors
Required: False

#### get_setup
Required: False

#### get_commands
Required: True

#### get_command_attaches
Required: True

#### get_command_functions
Required: True

#### get_loop_functions
Required: False

#### get_extra_functions
Required: False

#### get_core_values

Required: True