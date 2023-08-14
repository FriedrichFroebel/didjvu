from types import *
from . import paths as paths, util as util
from _typeshed import Incomplete
from typing import Any
from gamera.gui import has_gui as has_gui

DEFAULT_MAX_ARG_NUMBER: int

def method_wraper(f): ...

class NoGUIArgs:
    def setup(self, *args, **kwargs) -> None: ...
    def show(self, *args, **kwargs) -> None: ...

class Args(NoGUIArgs):
    list: Incomplete
    valid: int
    name: Incomplete
    function: Incomplete
    title: Incomplete
    def __init__(self, list: Incomplete | None = ..., name: str = ..., function: Incomplete | None = ..., title: Incomplete | None = ...) -> None: ...
    def __getitem__(self, i): ...
    index = __getitem__
    def __len__(self, i) -> int: ...

class CNoneDefault: ...

NoneDefault: Incomplete

class Arg:
    default: Any
    length: int
    name: Incomplete
    has_default: bool
    def __init__(self, name) -> None: ...
    def rest_repr(self, name: bool = ...): ...
    def register(self, plug, func) -> None: ...

class Int(Arg):
    rng: Incomplete
    has_default: bool
    default: int
    def __init__(self, name: Incomplete | None = ..., range=..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class Real(Arg):
    rng: Incomplete
    has_default: bool
    default: float
    def __init__(self, name: Incomplete | None = ..., range: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...
Float = Real

class Complex(Arg):
    has_default: bool
    default: complex
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class String(Arg):
    has_default: bool
    default: str
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class Class(Arg):
    klass: Incomplete
    list_of: Incomplete
    has_default: bool
    default: str
    def __init__(self, name: Incomplete | None = ..., klass: Incomplete | None = ..., list_of: bool = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class ImageType(Arg):
    klass: Incomplete
    pixel_types: Incomplete
    list_of: Incomplete
    has_default: bool
    default: Incomplete
    def __init__(self, pixel_types, name: Incomplete | None = ..., list_of: bool = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...
    def register(self, plug, func) -> None: ...

class Rect(Arg):
    klass: Incomplete
    list_of: Incomplete
    def __init__(self, name: Incomplete | None = ..., list_of: bool = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class Choice(Arg):
    choices: Incomplete
    has_default: bool
    default: int
    def __init__(self, name: Incomplete | None = ..., choices: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class ChoiceString(Arg):
    choices: Incomplete
    has_default: bool
    default: Incomplete
    strict: Incomplete
    def __init__(self, name: Incomplete | None = ..., choices: Incomplete | None = ..., default: Incomplete | None = ..., strict: bool = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class _Filename(Arg):
    default: Incomplete
    extension: Incomplete
    def __init__(self, name: Incomplete | None = ..., default: str = ..., extension: str = ...) -> None: ...

class FileOpen(_Filename): ...
class FileSave(_Filename): ...
class Directory(_Filename): ...

class Radio(Arg):
    radio_button: Incomplete
    def __init__(self, name: Incomplete | None = ..., radio_button: str = ...) -> None: ...

class Check(Arg):
    check_box: Incomplete
    has_default: bool
    default: bool
    enabled: Incomplete
    def __init__(self, name: Incomplete | None = ..., check_box: str = ..., default: Incomplete | None = ..., enabled: bool = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...
Bool = Check

class Region(Class):
    def __init__(self, name: Incomplete | None = ...) -> None: ...

class RegionMap(Class):
    def __init__(self, name: Incomplete | None = ...) -> None: ...

class ImageInfo(Class):
    def __init__(self, name: Incomplete | None = ...) -> None: ...

class Point(Arg):
    has_default: bool
    default: Incomplete
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...

class FloatPoint(Arg):
    has_default: bool
    default: Incomplete
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...

class Dim(Point): ...

class _Vector(Class):
    length: Incomplete
    default: Incomplete
    has_default: bool
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ..., length: int = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class FloatVector(_Vector):
    klass = float
    typecode: str

class IntVector(_Vector):
    klass = int
    typecode: str

class ComplexVector(_Vector):
    klass = complex
    typecode: Incomplete

class ImageList(Class):
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...

class Pixel(Class):
    has_default: bool
    default: Incomplete
    def __init__(self, name: Incomplete | None = ..., default: Incomplete | None = ...) -> None: ...
    def rest_repr(self, name: bool = ...): ...

class Info(Arg): ...

class PointVector(Class):
    def __init__(self, name: Incomplete | None = ...) -> None: ...

class Wizard:
    def show(self, dialog) -> None: ...

def mixin(module, name) -> None: ...
