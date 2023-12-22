from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self
    from ._typing import _Pos, _Size, _Area

import time, getpass
from aclib.winlib import winapi, wincon, wintype


__all__ = [
    'BaseWindow'
]


class BaseWindow(object):

    def __new__(cls):
        raise TypeError(
            f'to create a "{cls.__name__}" object, please use other methods of this class')

    @classmethod
    def _new_(cls, hwnd: int):
        wnd = object.__new__(cls)
        wnd._init_(hwnd)
        return wnd

    def _init_(self, hwnd: int):
        self.__handle = hwnd

    @classmethod
    def _newwnd_(cls, hwnd: int) -> Self | None:
        return cls._new_(hwnd) if winapi.IsWindowExistent(hwnd) else None

    def _sethandle_(self, hwnd: int):
        self.__handle = hwnd

    def __repr__(self):
        if self.handle == winapi.GetDesktopWindow(): summary = 'DESKTOP'
        elif self.handle == winapi.GetDesktopView(): summary = 'desktop'
        elif self.handle == winapi.GetTaskbarWindow(): summary = 'taskbar'
        else: summary = self.title.replace('\n', '\\n') or self.classname
        return f'<{self.__class__.__name__}-{self.handle} {summary}>'


    @property
    def handle(self) -> int:
        return self.__handle

    @property
    def classname(self) -> str:
        return winapi.GetWindowClassName(self.handle)

    @property
    def title(self) -> str:
        return winapi.GetWindowTitle(self.handle)

    def settitle(self, title: str) -> bool:
        return winapi.SetWindowTitle(self.handle, title)


    @property
    def threadid(self) -> int:
        return winapi.GetWindowThreadProcessId(self.handle)[0]

    @property
    def processid(self) -> int:
        return winapi.GetWindowThreadProcessId(self.handle)[1]

    @property
    def threadprocessid(self) -> tuple[int, int]:
        return winapi.GetWindowThreadProcessId(self.handle)

    @property
    def creationtime(self) -> int:
        hthread = winapi.OpenThreadHandle(self.threadid)
        ctime = winapi.GetThreadTimes(hthread)[0]
        winapi.CloseHandle(hthread)
        return ctime

    @property
    def exittime(self) -> int:
        hthread = winapi.OpenThreadHandle(self.threadid)
        etime = winapi.GetThreadTimes(hthread)[1]
        winapi.CloseHandle(hthread)
        return etime


    def tolayeredwindow(self):
        winapi.LayerWindow(self.handle)

    def tounlayeredwindow(self):
        winapi.UnlayerWindow(self.handle)


    @property
    def isexistent(self) -> bool:
        return winapi.IsWindowExistent(self.handle)

    @property
    def isenabled(self) -> bool:
        return winapi.IsWindowEnabled(self.handle)

    @property
    def isvisible(self) -> bool:
        return winapi.IsWindowVisible(self.handle)

    @property
    def isviewable(self) -> bool:
        (l, t, r, b), (sw, sh) = self.rect.values(), winapi.GetScreenSize()
        return l < sw and t < sh and r > 0 and b > 0

    @property
    def ismaximized(self) -> bool:
        return winapi.IsWindowMaximized(self.handle)

    @property
    def isminimized(self) -> bool:
        return winapi.IsWindowMinimized(self.handle)

    @property
    def isnormalized(self) -> bool:
        return winapi.IsWindowNormalized(self.handle)

    @property
    def isforeground(self) -> bool:
        return self.handle == winapi.GetForegroundWindow()


    def close(self):
        winapi.CloseWindow(self.handle)

    def destroy(self):
        winapi.DestroyWindow(self.handle)

    def enable(self):
        winapi.EnableWindow(self.handle)

    def disable(self):
        winapi.DisableWindow(self.handle)

    def show(self):
        winapi.ShowWindow(self.handle)

    def hide(self):
        winapi.HideWindow(self.handle)

    def maximize(self):
        winapi.MaximizeWindow(self.handle)

    def minimize(self):
        winapi.MinimizeWindow(self.handle)

    def normalieze(self):
        winapi.NormalizeWindow(self.handle)


    @property
    def rect(self) -> wintype.RECT:
        return winapi.GetWindowRect(self.handle)

    @property
    def rectR(self) -> wintype.RECT:
        return winapi.GetWindowRectR(self.handle)

    @property
    def pos(self) -> _Pos:
        return self.rect.start

    @property
    def posR(self) -> _Pos:
        return self.rectR.start

    @property
    def size(self) -> _Size:
        return self.rect.size

    def setpossize(self, newpos: _Pos, newsize: _Size):
        winapi.SetWindowPosSize(self.handle, newpos, newsize)

    def setpossizeR(self, newposR: _Pos, newsize: _Size):
        winapi.SetWindowPosSizeR(self.handle, newposR, newsize)

    def setpos(self, newpos: _Pos):
        winapi.SetWindowPosSize(self.handle, newpos)

    def setposR(self, newposR: _Pos):
        winapi.SetWindowPosSizeR(self.handle, newposR)

    def setsize(self, newsize: _Size):
        winapi.SetWindowPosSize(self.handle, None, newsize)


    @property
    def clientrect(self) -> wintype.RECT:
        return winapi.GetClientRect(self.handle)

    @property
    def clientrectR(self) -> wintype.RECT:
        return winapi.GetClientRectR(self.handle)

    @property
    def clientpos(self) -> _Pos:
        return self.clientrect.start

    @property
    def clientposR(self) -> _Pos:
        return self.clientrectR.start

    @property
    def clientsize(self) -> _Size:
        return self.clientrect.size

    def setclientpossize(self, newclientpos: _Pos, newclientsize: _Size):
        winapi.SetClientPosSize(self.handle, newclientpos, newclientsize)

    def setclientpossizeR(self, newclientposR: _Pos, newclientsize: _Size):
        winapi.SetClientPosSizeR(self.handle, newclientposR, newclientsize)

    def setclientpos(self, newclientpos: _Pos):
        winapi.SetClientPosSize(self.handle, newclientpos)

    def setclientposR(self, newclientposR: _Pos):
        winapi.SetClientPosSizeR(self.handle, newclientposR)

    def setclientsize(self, newclientsize: _Size):
        winapi.SetClientPosSize(self.handle, None, newclientsize)


    @property
    def transparency(self) -> float:
        return winapi.GetWindowTransparency(self.handle)

    def settransparency(self, transparency: float):
        winapi.SetWindowTransparency(self.handle, transparency)


    def getcolor(self, pos: _Pos) -> int:
        """get decimal bgr color at given pos"""
        return winapi.GetPixel(self.handle, pos)

    def capture(self, area: _Area) -> tuple[_Size, bytearray]:
        return winapi.CaptureWindow(self.handle, area)


    def movemouse(self, topos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_MOUSEMOVE, 0, winapi.MakeLong(*topos))


    def leftdown(self, pos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_LBUTTONDOWN, wincon.MK_LBUTTON, winapi.MakeLong(*pos))

    def leftup(self, pos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_LBUTTONUP, wincon.MK_LBUTTON, winapi.MakeLong(*pos))

    def leftclick(self, pos: _Pos):
        self.leftdown(pos)
        self.leftup(pos)

    def leftdbclick(self, pos: _Pos):
        self.leftclick(pos)
        self.leftclick(pos)

    def leftdrag(self, pos: _Pos, topos: _Pos):
        self.leftdown(pos)
        self.movemouse(topos)
        self.leftup(topos)

    def leftdragR(self, pos: _Pos, dpos: _Pos):
        self.leftdrag(pos, (pos[0] + dpos[0], pos[1] + dpos[1]))


    def rightdown(self, pos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_RBUTTONDOWN, wincon.MK_RBUTTON, winapi.MakeLong(*pos))

    def rightup(self, pos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_RBUTTONUP, wincon.MK_RBUTTON, winapi.MakeLong(*pos))

    def rightclick(self, pos: _Pos):
        self.rightdown(pos)
        self.rightup(pos)

    def rightdbclick(self, pos: _Pos):
        self.rightclick(pos)
        self.rightclick(pos)

    def rightdrag(self, pos: _Pos, topos: _Pos):
        self.rightdown(pos)
        self.movemouse(topos)
        self.rightup(topos)

    def rightdragR(self, pos: _Pos, dpos: _Pos):
        self.rightdrag(pos, (pos[0] + dpos[0], pos[1] + dpos[1]))


    def middown(self, pos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_MBUTTONDOWN, wincon.MK_MBUTTON, winapi.MakeLong(*pos))

    def midup(self, pos: _Pos):
        winapi.PostMessage(self.handle, wincon.WM_MBUTTONUP, wincon.MK_MBUTTON, winapi.MakeLong(*pos))

    def midclick(self, pos: _Pos):
        self.middown(pos)
        self.midup(pos)

    def middrag(self, pos: _Pos, topos: _Pos):
        self.middown(pos)
        self.movemouse(topos)
        self.midup(topos)

    def middragR(self, pos: _Pos, dpos: _Pos):
        self.middrag(pos, (pos[0] + dpos[0], pos[1] + dpos[1]))

    def wheelup(self, pos, times=1):
        self.movemouse(pos)
        lParam = winapi.MakeLong(*winapi.ClientToScreen(self.handle, pos))
        for i in range(times):
            winapi.PostMessage(self.handle, wincon.WM_MOUSEWHEEL, wincon.WHEEL_DELTA, lParam)

    def wheeldown(self, pos, times=1):
        self.movemouse(pos)
        lParam = winapi.MakeLong(*winapi.ClientToScreen(self.handle, pos))
        for i in range(times):
            winapi.PostMessage(self.handle, wincon.WM_MOUSEWHEEL, -wincon.WHEEL_DELTA, lParam)


    def keydown(self, key: int | str):
        winapi.PostMessage(self.handle, wincon.WM_IME_KEYDOWN, *winapi.MakeKeyMessageParam(key)[0])

    def keyup(self, key:int|str):
        winapi.PostMessage(self.handle, wincon.WM_IME_KEYUP, *winapi.MakeKeyMessageParam(key)[1])

    def keypress(self, key: int | str):
        self.keydown(key)
        self.keyup(key)

    def waitkey(self, *keys: int | str, msg='', cmdmode=False) -> int | str:
        vkmap = {}
        for key in keys:
            vkcode = winapi.MakeKeyCode(key)
            if not vkcode:
                raise ValueError(f'invalid key <- {key} ->')
            vkmap[vkcode] =  key
        vkmap = vkmap or wincon.VK_MAP_KEYBOARD
        print(msg)
        while True:
            for vkcode in vkmap:
                if winapi.GetAsyncKeyState(vkcode):
                    if cmdmode:
                        if vkcode != 13: self.keypress('enter')
                        getpass.getpass('')
                    return vkmap[vkcode]
            time.sleep(.001)
