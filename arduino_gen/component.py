from ..utils.decorators import attr_check, type_check


@attr_check
class Component:
	@type_check
	def __init__(self, json_item: dict, class_dict: dict, device_dict: dict):
		for key, value in json_item.items():
			if key in self.__dict__:
				type_ = self.__dict__[key].get_type()
				type_name = type_.__name__

				# Appendage type (dependency)
				if type_name in self.class_dict:
					object_ = type_(value, class_dict, device_dict)
					self.__dict__[key] = object_
					if type_name not in device_dict:
						device_dict[type_name] = []
					device_dict[type_name].append(object_)

				# Default type
				else:
					self.__dict__[key] = type_(value)
			else:
				raise Exception("Json value not in Struct {0:s}",format(self.__class__))