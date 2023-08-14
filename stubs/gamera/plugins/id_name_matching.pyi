from gamera.plugin import *
from _typeshed import Incomplete

def build_id_regex(s): ...

regex_cache: Incomplete
dummy_regex: Incomplete
type_dummy_regex: Incomplete

class match_id_name(PluginFunction):
    args: Incomplete
    def __call__(self, regex): ...
    __call__: Incomplete

def id_name_to_identifier(symbol): ...

class IdNameMatchingModule(PluginModule):
    category: str
    functions: Incomplete
    author: str
    url: str
    pure_python: int

module: Incomplete
