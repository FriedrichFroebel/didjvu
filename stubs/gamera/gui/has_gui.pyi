from _typeshed import Incomplete

NO_GUI: Incomplete
WX_GUI: Incomplete
CURSES_GUI: Incomplete
has_gui = NO_GUI

class NullGui:
    class NullMethod:
        def __call__(*args, **kwargs) -> None: ...
    def __getattr__(self, attr): ...

gui: Incomplete
