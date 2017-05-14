from ..util.decorators import attr_check, type_check


class Component:
        @type_check
        def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
                for key, value in json_item.items():
                    if key == 'type':
                        continue
                    if hasattr(self, key):
                        type_ = type(getattr(self, key))
                        type_name = type_.__name__

                        # Appendage type (dependency)
                        if type_name in class_dict:
                            object_ = type_(value, class_dict, device_dict)
                            setattr(self, key, object_)
                            if type_name not in device_dict:
                                device_dict[type_name] = []
                            device_dict[type_name].append(object_)

                        # Default type
                        else:
                            setattr(self, key, type_(value))
                    else:
                        raise Exception("Json value {0:s} not in Struct {1:s}".format(key, self.__class__.__name__))
