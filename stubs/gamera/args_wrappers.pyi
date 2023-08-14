from .enums import *
from . import util as util
from _typeshed import Incomplete
from gamera import args as args

class Arg:
    arg_format: str
    convert_from_PyObject: bool
    multiple: bool
    delete_cpp: bool
    uid: int
    def __getitem__(self, attr): ...
    def __iter__(self): ...
    symbol: Incomplete
    pysymbol: Incomplete
    name: Incomplete
    def declare(self): ...
    def from_python(self): ...
    def call(self, function, args, output_args, limit_choices: Incomplete | None = ...): ...
    def delete(self): ...

class Int(Arg):
    arg_format: str
    c_type: str
    def to_python(self): ...
Choice = Int
Check = Int

class Float(Arg):
    arg_format: str
    c_type: str
    def to_python(self): ...

class Complex(Arg):
    arg_format: str
    c_type: str
    def to_python(self): ...
    def from_python(self): ...

class String(Arg):
    arg_format: str
    c_type: str
    return_type: str
    def to_python(self): ...
FileOpen = String
FileSave = String
Directory = String
ChoiceString = String

class ImageType(Arg):
    c_type: str
    convert_from_PyObject: bool
    multiple: bool
    def from_python(self): ...
    def to_python(self): ...
    def call(self, function, args, output_args, limit_choices: Incomplete | None = ...): ...

class Rect(Arg):
    c_type: str
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class Region(Arg):
    c_type: str
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class RegionMap(Arg):
    c_type: str
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class ImageList(Arg):
    c_type: str
    return_type: str
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class Class(Arg):
    arg_format: str
    c_type: str
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class IntVector(Arg):
    arg_format: str
    convert_from_PyObject: bool
    c_type: str
    delete_cpp: bool
    def from_python(self): ...
    def to_python(self): ...

class FloatVector(Arg):
    arg_format: str
    convert_from_PyObject: bool
    c_type: str
    delete_cpp: bool
    def from_python(self): ...
    def to_python(self): ...

class ComplexVector(Arg):
    arg_format: str
    convert_from_PyObject: bool
    c_type: str
    delete_cpp: bool
    def from_python(self): ...
    def to_python(self): ...

class Pixel(Arg):
    def from_python(self): ...
    def call(self, function, args, output_args, limit_choices: Incomplete | None = ...): ...

class Point(Arg):
    c_type: str
    delete_cpp: bool
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class FloatPoint(Arg):
    c_type: str
    delete_cpp: bool
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class Dim(Arg):
    c_type: str
    convert_from_PyObject: bool
    def from_python(self): ...
    def to_python(self): ...

class PointVector(Arg):
    arg_format: str
    convert_from_PyObject: bool
    c_type: str
    delete_cpp: bool
    def from_python(self): ...
    def to_python(self): ...

class ImageInfo(Arg):
    arg_format: str
    c_type: str
    convert_from_PyObject: bool
    def to_python(self): ...
