from _typeshed import Incomplete
from gamera.backport import dircache as dircache

def dummy() -> None: ...

lib: Incomplete
lib_gui: Incomplete
plugins: Incomplete
doc: Incomplete
plugins_src: str
toolkits: Incomplete
test: Incomplete
test_results: Incomplete

def get_toolkit_names(dir): ...
def import_directory(dir, gl, lo, verbose: int = ...): ...
