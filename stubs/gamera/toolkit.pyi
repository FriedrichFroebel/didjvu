from _typeshed import Incomplete
from gamera.gui import gui as gui, has_gui as has_gui, icon_display as icon_display

CustomMenu = gui.CustomMenu
CustomIcon = icon_display.CustomIcon

class NullClass:
    def __init__(self, *args, **kwargs) -> None: ...

class CustomMenu(NullClass): ...

class CustomIcon(NullClass):
    def register(cls, *args, **kwargs) -> None: ...
    register: Incomplete
