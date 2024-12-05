from ...core import rpc_client
from ...common.utils.process_arg import map_arg

import inspect
from functools import wraps

# def method_wrapper(method):
#     @wraps(method)
#     def wrapped(self, *args, **kwargs): # No methods are present in Pluto Script
#         # Access instance attributes like self.token
#         # print(f"Method called: {method.__name__} with self.token: {self.token}")
#         # Modify behavior as needed
#         # For example, redirect the call
#         # return self.try_get(function_name=method.__name__)
#         return
#     return wrapped

def property_wrapper(prop):
    # Wrap the getter
    if prop.fget:
        @wraps(prop.fget)
        def getter(self):
            print(f"Getting property: {prop.fget.__name__} with self.token: {self.token}")
            # Redirect or modify behavior here
            return self.try_get(function_name=prop.fget.__name__)
    else:
        getter = None

    # Wrap the setter
    if prop.fset:
        @wraps(prop.fset)
        def setter(self, value):
            print(f"Setting property: {prop.fset.__name__} to {value} with self.token: {self.token}")
            # Redirect or modify behavior here
            self.try_set(function_name=prop.fset.__name__, value=value)
    else:
        setter = None

    # Wrap the deleter
    if prop.fdel:
        @wraps(prop.fdel)
        def deleter(self):
            print(f"Deleting property: {prop.fdel.__name__}")
            # Redirect or modify behavior here
            prop.fdel(self)
    else:
        deleter = None

    return property(getter, setter, deleter)

class WrapperMeta(type):
    def __new__(cls, name, bases, dct):
        # Create the class object first
        cls_obj = super().__new__(cls, name, bases, dct)
        wrapped_methods = set()

        # Iterate over the MRO to include inherited methods and properties
        for base in cls_obj.__mro__:
            for attr_name, attr_value in base.__dict__.items():
                if attr_name in wrapped_methods or attr_name.startswith('__') and attr_name.endswith('__'):
                    continue

                # if callable(attr_value):
                #     # Wrap methods
                #     setattr(cls_obj, attr_name, method_wrapper(attr_value))
                #     wrapped_methods.add(attr_name)
                
                if isinstance(attr_value, property):
                    # Wrap properties
                    setattr(cls_obj, attr_name, property_wrapper(attr_value))
                    wrapped_methods.add(attr_name)

        return cls_obj