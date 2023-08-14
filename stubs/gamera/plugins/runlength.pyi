from gamera.plugin import *
from _typeshed import Incomplete

class most_frequent_run(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class most_frequent_runs(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    def __call__(image, n: int = ..., color: str = ..., direction: str = ...): ...
    __call__: Incomplete
    doc_examples: Incomplete

class run_histogram(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class FilterRuns(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    doc_examples: Incomplete

class filter_narrow_runs(FilterRuns):
    def __call__(image, length, color: str = ...): ...
    __call__: Incomplete

class filter_wide_runs(FilterRuns):
    def __call__(image, length, color: str = ...): ...
    __call__: Incomplete

class filter_tall_runs(FilterRuns):
    def __call__(image, length, color: str = ...): ...
    __call__: Incomplete

class filter_short_runs(FilterRuns):
    def __call__(image, length, color: str = ...): ...
    __call__: Incomplete

class to_rle(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    doc_examples: Incomplete

class from_rle(PluginFunction):
    self_type: Incomplete
    args: Incomplete

class iterate_runs(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete

class runlength_from_point(PluginFunction):
    category: str
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str

class FrequentRun(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    category: str
    pure_python: bool

class FrequentRuns(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    return_type: Incomplete
    author: str
    category: str
    pure_python: bool

class RunHistogram(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    author: str
    category: str
    pure_python: bool

class FilterRunsDep(PluginFunction):
    self_type: Incomplete
    args: Incomplete
    category: str
    pure_python: bool

class RunIterator(PluginFunction):
    self_type: Incomplete
    return_type: Incomplete
    category: str
    pure_python: bool

class RunLengthModule(PluginModule):
    category: str
    cpp_headers: Incomplete
    functions: Incomplete
    author: str
    url: str

module: Incomplete
