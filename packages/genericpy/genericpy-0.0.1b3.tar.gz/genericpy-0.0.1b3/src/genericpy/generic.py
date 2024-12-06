from typing import Optional, Union, Tuple, Any
from types import MethodType, FunctionType
import sys
from io import StringIO
import weakref
import inspect
from pyreflex.pybase import deepcopy_class


# class SpecializedTypes(dict):
#     def get(self, key):
#         if not isinstance(key, tuple):
#             key = (key,)
#         item = super().get(key)
#         if item is not None:
#             item = item[0]
#         return item
    
#     def __getitem__(self, key):
#         if not isinstance(key, tuple):
#             key = (key,)
#         return super().__getitem__(key)[0]
    
#     def __setitem__(self, key, value):
#         if isinstance(key, tuple):
#             def finalize():
#                 _, finalizers = self.pop(key)
#                 (finalizer.detach() for finalizer in finalizers)
#             finalizers = [weakref.finalize(subkey, finalize) for subkey in key]
#             return super().__setitem__(key, (value, finalizers))
#         else:
#             tuple_key = (key,)
#             def finalize():
#                 self.pop(tuple_key)
#             weakref.finalize(key, finalize)
#             return super().__setitem__(tuple_key, (value, None))


def _class_typing(cls) -> Union[type, Tuple[type, ...], Any, None]:
    try:
        return cls.__type__
    except AttributeError:
        try:
            return cls.__types__
        except AttributeError: ...


class specialization(dict):
    def __getitem__(self, key):
        if isinstance(key, tuple):
            weakkey = tuple(weakref.ref(each) for each in key)
        else:
            weakkey = weakref.ref(key)
        return super().__getitem__(weakkey)[0]
    
    def __setitem__(self, key, value):
        try:
            from pyreflex.pybase import decref, incref
            def remove_key(weakkey, selfref=weakref.ref(self)):
                self = selfref()
                if self is not None:
                    try:
                        self.pop(weakkey)
                    except KeyError: ...
            if isinstance(key, tuple):
                weakkey = tuple((weakref.ref(each), decref(each))[0] for each in key)
                def finalize_key(selfref=weakref.ref(self)):
                    self = selfref()
                    if self is not None:
                        try:
                            _, finalizers = self.pop(weakkey)
                            (finalizer.detach() for finalizer in finalizers)
                        except KeyError: ...
                finalizers = [weakref.finalize(subkey, finalize_key) for subkey in key]
                def finalize_value():
                    for type in weakkey:
                        type = type()
                        if type is not None:
                            incref(type)
                    remove_key(weakkey)
            else:
                decref(key)
                weakkey = weakref.ref(key)
                weakref.finalize(key, lambda: remove_key(weakkey))
                finalizers = None
                def finalize_value():
                    type = weakkey()
                    if type is not None:
                        incref(type)
                    remove_key(weakkey)
            weakref.finalize(value, finalize_value)
            return super().__setitem__(weakkey, (value, finalizers))
        except TypeError:
            ...
    
    def get(self, key):
        try:
            if isinstance(key, tuple):
                weakkey = tuple(weakref.ref(each) for each in key)
            else:
                weakkey = weakref.ref(key)
            item = super().get(weakkey)
            if item is not None:
                item = item[0]
        except TypeError:
            item = None
        return item


class blocker:
    __slots__ = ('name')
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        owner = type(owner.__name__, tuple(), {})
        if instance is None:
            return getattr(owner, self.name)
        else:
            return getattr(owner(), self.name)


class generic: ...
_blank_generic = generic
class generic(_blank_generic):
    @staticmethod
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super(object).__init_subclass__()
        setattr(cls, f'__specialized_types', specialization())
_subclass_generic = generic
_subclass_generic.__type__ = blocker('__type__')
_subclass_generic.__types__ = blocker('__types__')
_subclass_generic.receive = blocker('receive')
class generic(_blank_generic):
    @staticmethod
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super(object).__init_subclass__()
    @classmethod
    def __class_getitem__(cls, *args): ...
_typed_generic = generic
_typed_generic.__type__ = blocker('__type__')
_typed_generic.__types__ = blocker('__types__')
_typed_generic.receive = blocker('receive')


def _qualname(obj):
    try:
        return obj.__qualname__
    except AttributeError:
        return repr(obj)


class generic:
    __type__: Optional[type]
    __types__: Optional[tuple[type, ...]]
    
    @staticmethod
    def receive(obj: Union[type, Any, None] = None) -> Union[type, Tuple[type, ...], Any, None]:
        if obj is None:
            return sys._getframe(1).f_globals.get(_blank_generic)
        else:
            if not isinstance(obj, type):
                obj = type(obj)
            return _class_typing(obj)
    
    @staticmethod
    def __new__(cls, *args, **kwargs):
        if cls is generic and len(args) == 1:
            maybe_func = args[0]
            if callable(maybe_func) or isinstance(maybe_func, classmethod):
                return dispatcher(maybe_func)
        return super().__new__(cls)
    
    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        setattr(cls, f'__specialized_types', specialization())
        bases = tuple(_subclass_generic if base is generic else base for base in cls.__bases__)
        cls.__bases__ = bases
    
    @classmethod
    def __class_getitem__(cls, typelike) -> type:
        specialized_types: dict[type, type] = getattr(cls, '__specialized_types')
        result = specialized_types.get(typelike)
        if result is None:
            if isinstance(typelike, tuple):
                inner_name = StringIO()
                length = len(typelike)
                for i, each_type in enumerate(typelike):
                    inner_name.write(_qualname(each_type))
                    if i != length - 1:
                        inner_name.write(', ')
                inner_name = inner_name.getvalue()
                is_multiple = True
            else:
                inner_name = _qualname(typelike)
                is_multiple = False
            typed_generic = deepcopy_class(_typed_generic)
            typed_generic.__bases__ = (cls,)
            class TypedGeneric(typed_generic): ...
            TypedGeneric.__name__ = f'{cls.__name__}[{inner_name}]'
            TypedGeneric.__qualname__ = f'{cls.__qualname__}[{inner_name}]'
            TypedGeneric.__module__ = cls.__module__
            if is_multiple:
                TypedGeneric.__types__ = typelike
            else:
                TypedGeneric.__type__ = typelike
            result = TypedGeneric
            specialized_types[typelike] = result
        return result

_subclass_generic.__bases__ = (generic,)
setattr(generic, f'__specialized_types', specialization())


class dispatcher:
    __slots__ = ('_dispatcher__specialized_types', '_dispatcher__function', '_dispatcher__function_type', '_dispatcher__instance', '_dispatcher__type')
    
    def __init__(self, function):
        self.__specialized_types = specialization()
        self.__instance = None
        self.__type = None

        function_type = type(function)
        self.__function_type = function_type
        if issubclass(function_type, staticmethod):
            function = function.__wrapped__
        elif issubclass(function_type, classmethod):
            function = function.__wrapped__
        else:
            function = function
        self.__function = function
    
    def __get__(self, instance, owner):
        self.__instance = instance
        self.__type = owner
        return self
    
    def __getitem__(self, typelike):
        result = self.__specialized_types.get(typelike)
        if result is None:
            function = self.__function
            typed_function_globals = {_blank_generic : typelike}
            typed_function_globals.update(function.__globals__)
            code = function.__code__
            typed_function = FunctionType(
                code,
                typed_function_globals,
                code.co_name,
                function.__defaults__,
                function.__closure__
            )
            if isinstance(typelike, tuple):
                type_output = StringIO()
                final_index = len(typelike) - 1
                for i, each in enumerate(typelike):
                    type_output.write(_qualname(each))
                    if i != final_index:
                        type_output.write(', ')
                type_output = type_output.getvalue()
            else:
                type_output = _qualname(typelike)
            typed_function.__name__ = function.__name__
            typed_function.__qualname__ = f'{function.__qualname__}[{type_output}]'
            typed_function.__module__ = function.__module__
            typed_function.__doc__ = function.__doc__
            result = typed_function
            self.__specialized_types[typelike] = result
        function = result
        if self.__type is None or issubclass(self.__function_type, staticmethod):
            return function
        elif issubclass(self.__function_type, classmethod):
            return MethodType(function, self.__type)
        elif self.__instance is None:
            return function
        else:
            return MethodType(function, self.__instance)
    
    def __call__(self, *args, **kwargs):
        function = self.__function
        if self.__type is None or issubclass(self.__function_type, staticmethod):
            return function(*args, **kwargs)
        elif issubclass(self.__function_type, classmethod):
            return function(self.__type, *args, **kwargs)
        elif self.__instance is None:
            return function(*args, **kwargs)
        else:
            return function(self.__instance, *args, **kwargs)
    
    def __getattribute__(self, name):
        if name == '__name__':
            return self.__function.__name__
        elif name == '__qualname__':
            return self.__function.__qualname__
        elif name == '__module__':
            return self.__function.__module__
        # elif name == '__class__':
        #     if self.__instance is None or issubclass(self.__function_type, staticmethod) or issubclass(self.__function_type, classmethod):
        #         return Callable
        #     else:
        #         return MethodType
        return super().__getattribute__(name)
    
    def __getattr__(self, name):
        function = self.__function
        return getattr(function, name)
    
    def __repr__(self):
        function = self.__function
        qualname = function.__qualname__
        if self.__type is None or issubclass(self.__function_type, staticmethod):
            ...
        else:
            while True:
                if issubclass(self.__function_type, classmethod):
                    anchor = repr(self.__type)
                elif self.__instance is None:
                    break
                else:
                    anchor = f'<{self.__type.__module__}.{self.__type.__name__} object at {hex(id(self.__instance))}>'
                return f"<bound generic template method {qualname} of {anchor}>"
        return f"<generic template function {function.__module__}.{qualname}[...]{inspect.signature(function)}>"
    
    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    def __subclasscheck__(self, cls):
        return issubclass(cls, self.__class__)
    
    def __reduce_ex__(self, protocol):
        function_type = self.__function_type
        if issubclass(function_type, classmethod) or issubclass(function_type, staticmethod):
            function = function_type(self.__function)
        else:
            function = self.__function
        return (type(self), (function,))
    
    # def __getstate__(self):
    #     state = {}
    #     for name in self.__slots__:
    #         state[name] = _get_attribute(self, name)
    #     return state
    
    # def __setstate__(self, state):
    #     for name in self.__slots__:
    #         _set_attribute(self, name, state[name])


# def _get_attribute(obj, name: str):
#     if name.startswith('__'):
#         return obj.__getattribute__(f'_{type(obj).__name__}{name}')
#     else:
#         return obj.__getattribute__(name)


# def _set_attribute(obj, name: str, value):
#     if name.startswith('__'):
#         return obj.__setattr__(f'_{type(obj).__name__}{name}', value)
#     else:
#         return obj.__setattr__(name, value)


class receiver:
    def __get__(self, instance, owner) -> Union[type, Tuple[type, ...], Any, None]:
        return sys._getframe(1).f_globals.get(_blank_generic)

generic.__types__ = generic.__type__ = receiver()


receive = generic.receive