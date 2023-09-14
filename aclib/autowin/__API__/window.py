from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

from typing import overload
from aclib.winlib import winapi

from .basewindow import BaseWindow


__all__ = [
    'Window'
]


class Window(BaseWindow):


    @overload
    def __new__(cls, hwnd: int) -> Self: ...

    @overload
    def __new__(cls, title='', classname='', visible: bool=None) -> Self | None: ...

    def __new__(cls, target: int | str ='', classname='', visivle: bool=None) -> Self | None:
        if isinstance(target, int):
            return super()._new_(target)
        return super()._newwnd_(winapi.FilterWindow(winapi.IterDescendantWindows(0), target, classname, visivle))


    @classmethod
    def findwindows(cls, title='', classname='', visible: bool=None) -> list[Self]:
        return [cls._new_(h) for h in winapi.FilterWindows(winapi.IterDescendantWindows(0), title, classname, visible)]


    @classmethod
    def desktopwindow(cls) -> Self:
        """winapi中定义的DesktopWindow"""
        return cls._new_(winapi.GetDesktopWindow())

    @classmethod
    def desktop(cls) -> Self:
        """显示桌面图标的窗口"""
        return cls._new_(winapi.GetDesktopView())

    @classmethod
    def taskbar(cls) -> Self:
        return cls._new_(winapi.GetTaskbarWindow())


    @classmethod
    def pointwindow(cls, pos: tuple[int, int] = None) -> Self:
        return cls._new_(winapi.GetPointWindow(pos or winapi.GetCursorPos()))

    @classmethod
    def foregroundwindow(cls) -> Self:
        return cls._new_(winapi.GetForegroundWindow())


    def parent(self) -> Self:
        return self._new_(winapi.GetParentWindow(self.handle))

    def root(self) -> Self:
        return self._new_(winapi.GetRootWindow(self.handle))

    def rootowner(self) -> Self:
        return self._new_(winapi.GetRootOwnerWindow(self.handle))


    def prevbrother(self) -> Self | None:
        return self._newwnd_(winapi.GetPrevWindow(self.handle))

    def nextbrother(self) -> Self | None:
        return self._newwnd_(winapi.GetNextWindow(self.handle))

    def brother(self, title='', classname='', visible: bool=None) -> Self | None:
        return self._newwnd_(winapi.FilterWindow(winapi.IterBrotherWindows(self.handle), title, classname, visible))

    def brothers(self, title='', classname='', visible: bool=None) -> list[Self]:
        return [self._new_(h) for h in winapi.FilterWindows(winapi.IterBrotherWindows(self.handle), title, classname, visible)]


    def child(self, title='', classname='', visible: bool=None) -> Self | None:
        return self._newwnd_(winapi.FilterWindow(winapi.IterChildWindows(self.handle), title, classname, visible))

    def children(self, title='', classname='', visible: bool=None) -> list[Self]:
        return [self._new_(h) for h in winapi.FilterWindows(winapi.IterChildWindows(self.handle), title, classname, visible)]


    def descendant(self, title='', classname='', visible: bool=None) -> Self | None:
        return self._newwnd_(winapi.FilterWindow(winapi.IterDescendantWindows(self.handle), title, classname, visible))

    def descendants(self, title='', classname='', visible: bool=None) -> Self | None:
        return [self._new_(h) for h in winapi.FilterWindows(winapi.IterDescendantWindows(self.handle), title, classname, visible)]
