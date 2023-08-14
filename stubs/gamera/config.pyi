from .backport.config import *
from _typeshed import Incomplete

class GameraConfigOptionParser(ConfigOptionParser):
    extra_files: Incomplete
    def add_file(self, file) -> None: ...
    def get_config_files(self): ...

config: Incomplete
