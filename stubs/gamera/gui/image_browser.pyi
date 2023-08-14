import wx
from _typeshed import Incomplete
from gamera import core as core
from gamera.gui import compat_wx as compat_wx, gamera_display as gamera_display, gamera_icons as gamera_icons, gui_util as gui_util

class FileList(wx.GenericDirCtrl):
    image_display: Incomplete
    def __init__(self, parent, ID, image_display) -> None: ...
    def OnItemSelected(self, e) -> None: ...

class ImageBrowserFrame(wx.Frame):
    splitter: Incomplete
    image: Incomplete
    file: Incomplete
    def __init__(self) -> None: ...
