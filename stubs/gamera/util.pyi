from types import *
from gamera.enums import *
from _typeshed import Incomplete
from collections.abc import Generator
from gamera.config import config as config
from gamera.gui import has_gui as has_gui

def is_sequence(obj): ...
def make_sequence(obj): ...
def is_image_list(l): ...
def is_string_or_unicode(s): ...
def is_homogeneous_image_list(l): ...
def is_homogenous_list(l, t): ...
def is_string_or_unicode_list(l): ...
def replace_prefix(s, a, b): ...
def fast_cmp(x, y): ...
def rangeeq(a, b, range, mod: int = ...): ...
def constains_instance(gl, klass): ...
def sublists(list) -> Generator[Incomplete, None, None]: ...
def string2identifier(str): ...
def sign(i): ...

class Set(list):
    def __init__(self, list=...) -> None: ...
    def append(self, item) -> None: ...
    def insert(self, i, item) -> None: ...
    def extend(self, other) -> None: ...

class SetDictionary(dict):
    def __getitem__(self, key): ...

def pretty_print_byte_size(bytes): ...
def enumerate(collection) -> Generator[Incomplete, None, None]: ...

enumerate: Incomplete

def get_pixel_type_name(type_): ...
def group_list(list, group_size): ...
def permute_list(alist, level: int = ...) -> Generator[Incomplete, None, None]: ...
def combinations(seed) -> Generator[Incomplete, None, None]: ...
def word_wrap(stream, l, indent: int = ..., width: int = ...) -> None: ...
def encode_binary(s): ...
def decode_binary(s): ...

class ProgressNothing:
    def __init__(self, message, length: int = ...) -> None: ...
    def ___(*args) -> None: ...
    update = ___
    kill = ___
    step = ___
    add_length = ___
    set_length = ___

class ProgressText:
    width: int
    def __init__(self, message, length: int = ...) -> None: ...
    def add_length(self, l) -> None: ...
    def set_length(self, l) -> None: ...
    def step(self) -> None: ...
    def kill(self) -> None: ...
    def update(self, num, den) -> None: ...

def ProgressFactory(message, length: int = ..., numsteps: int = ...): ...
def dedent(s): ...

class CallbackObject:
    is_dirty: bool
    def __init__(self) -> None: ...
    def add_callback(self, alert, callback) -> None: ...
    def remove_callback(self, alert, callback) -> None: ...
    def trigger_callback(self, alert, *args) -> None: ...

class CallbackList(list, CallbackObject):
    def __init__(self, initlist=...) -> None: ...
    def add_callback(self, alert, callback) -> None: ...
    def clear(self) -> None: ...
    def __del__(self) -> None: ...
    def __setitem__(self, i, item) -> None: ...
    def __delitem__(self, i) -> None: ...
    def __setslice__(self, i, j, other) -> None: ...
    def __delslice__(self, i, j) -> None: ...
    def __iadd__(self, other) -> None: ...
    def append(self, item) -> None: ...
    def insert(self, i, item) -> None: ...
    def pop(self, i: int = ...) -> None: ...
    def remove(self, item) -> None: ...
    def extend(self, other) -> None: ...

class CallbackSet(set, CallbackObject):
    def __init__(self, initset=...) -> None: ...
    def __del__(self) -> None: ...
    def add_callback(self, alert, callback) -> None: ...
    def add(self, element) -> None: ...
    append = add
    def remove(self, element) -> None: ...
    def discard(self, element) -> None: ...
    def pop(self) -> None: ...
    def clear(self) -> None: ...
    def update(self, iterable) -> None: ...
    def difference_update(self, iterable) -> None: ...
    def symmetric_difference_update(self, iterable) -> None: ...
    def intersection_update(self, iterable) -> None: ...
    def union_update(self, other) -> None: ...
    extend = update

def get_file_extensions(mode): ...

class _ImageFileExtensionFinder:
    mode: Incomplete
    def __init__(self, mode) -> None: ...

load_image_file_extension_finder: Incomplete
save_image_file_extension_finder: Incomplete

def __warn_deprecated__(message, other_filename: Incomplete | None = ..., other_lineno: Incomplete | None = ..., from_cpp: bool = ...) -> None: ...
warn_deprecated = __warn_deprecated__
