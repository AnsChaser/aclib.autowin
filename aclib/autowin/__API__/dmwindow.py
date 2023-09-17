from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Literal
    from ._typing import _Area, _Areas

import os, itertools
from aclib.dm import DM, DmDotsetLib

from ._functool import findfunc
from ._target import Target
from .window import Window


class DmWindow(Window):

    def _init_(self, hwnd: int):
        super()._init_(hwnd)
        self.__dmready = False
        self.__dmwordlock = False
        self.__dmdotsetlib: DmDotsetLib = None

    @property
    def __dm(self) -> DM:
        del DmWindow.__dm
        self.__dm = DM()
        self.__dm.SetShowErrorMsg(0)
        return self.__dm

    @property
    def _dmready(self) -> bool:
        return self.__dmready

    def dmset(self,
        displaymode: Literal['dx', 'dx2', 'dx3', 'gdi', 'gdi2'] | None = '',
        fontlib: str | None = '',
        dotsetlib: str | None = '',
        libscale: float = 1.0
    ) -> Self:
        """传入空字符串时对应参数不做更改，传入None时清除已设置的值"""
        if displaymode:
            self.__dm.UnBindWindow()
            self.__dm.BindWindow(self.handle, displaymode, 'windows', 'windows', 0)
            self.__dmready = True
        if fontlib:
            if not os.path.isfile(fontlib):
                raise FileNotFoundError(
                    f'No such file or directory: {fontlib}')
            self.__dm.SetDict(0, fontlib)
        if dotsetlib:
            self.__dmdotsetlib = DmDotsetLib.fromfile(dotsetlib).scale(libscale)
        if displaymode is None:
            self.__dm.UnBindWindow()
            self.__dmready = False
        if fontlib is None:
            self.__dm.ClearDict()
            self.__dmwordlock = False
        if dotsetlib is None:
            self.__dmdotsetlib = None
        return self

    def dmcapture(self, area: _Area=None, savepath: str=''):
        assert self.__dmready, 'dm not set'
        area = area or (0, 0, *self.clientsize)
        self.__dm.Capture(*area, savepath)

    @findfunc
    def dmfindcolor(self, color: str, areas: _Area|_Areas=None, lpoutput: list=None) -> Target:
        for area, color in itertools.product(areas, color.split('|')):
            x, y, success = self.__dm.FindColor(*area, color, 1, 0)
            if success:
                return Target(color, (x, y), (x, y), 1.0)
        return Target.none

    @findfunc
    def dmfindcolors(self, color: str, areas: _Area|_Areas=None, lpoutput: list=None) -> list[Target]:
        found = []
        for area, color in itertools.product(areas, color.split('|')):
            res = self.__dm.FindColorEx(*area, color, 1, 0)
            if not res: continue
            xs, ys = [[int(coor) for coor in coors.split(',')] for coors in res.split('|')]
            for i in range(min(len(xs), len(ys))):
                pos = xs[i], ys[i]
                found.append(Target(color, pos, pos, 1.0))
        return found

    @findfunc
    def dmfindcolorblock(self, colorBlock: str, areas: _Area|_Areas=None, similarity=1, scale=1, lpoutput: list=None) -> Target:
        """ colorBlock: '{w}x{h}x{color}|{w}x{h}x{color}' like '3x5xefefef-101010' """
        for area, colorBlock in itertools.product(areas, colorBlock.split('|')):
            w,h,color = [(round(int(w)*scale), round(int(h)*scale), color) for w,h,color in [(info for info in colorBlock.split('x'))]][0]
            dmColorBlock = ','.join([f'{i%w}|{i//w}|{color}' for i in range(w*h)])
            x, y, success = self.__dm.FindMultiColor(*area, color, dmColorBlock, similarity, 0)
            if success:
                colorBlock = f'{w}x{h}x{color}'
                start = x, y
                end = x+w, y+h
                return Target(colorBlock, start, end, similarity)
        return Target.none

    @findfunc
    def dmfindcolorblocks(self, colorBlock: str, areas: _Area|_Areas=None, similarity=1, scale=1, lpoutput: list=None) -> list[Target]:
        """ colorBlock: '{w}x{h}x{color}|{w}x{h}x{color}' like '3x5xefefef-101010' """
        found = []
        for area, colorBlock in itertools.product(areas, colorBlock.split('|')):
            w,h,color = [(round(int(w)*scale), round(int(h)*scale), color) for w,h,color in [(info for info in colorBlock.split('x'))]][0]
            dmColorBlock = ','.join([f'{i%w}|{i//w}|{color}' for i in range(w*h)])
            res = self.__dm.FindMultiColorEx(*area, color, dmColorBlock, similarity, 0)
            if not res: continue
            xs, ys = [[int(coor) for coor in coors.split(',')] for coors in res.split('|')]
            for i in range(min(len(xs), len(ys))):
                x, y = xs[i], ys[i]
                start = x, y
                end = x+w, y+h
                found.append(Target(colorBlock, start, end, similarity))
        return found

    @findfunc
    def dmfinddotset(self, dotsetname: str, areas: _Area|_Areas=None, color: str=None, similarity=1, scale=1, lpoutput: list=None) -> Target:
        if not self.__dmdotsetlib:
            return Target.none
        for area, dotsetname in itertools.product(areas, dotsetname.split('|')):
            for dotset in self.__dmdotsetlib.group(dotsetname):
                dotset = dotset.scale(scale).asmatchcolor(color)
                x, y, success = self.__dm.FindMultiColor(*area, dotset.matchcolor, dotset.tmpl, similarity, 0)
                if success:
                    start = dotset.getrealpos((x, y))
                    end = start[0] + dotset.width, start[1] + dotset.height
                    return Target(dotsetname, start, end, similarity)
        return Target.none

    @findfunc
    def dmfinddotsets(self, dotsetname: str, areas: _Area|_Areas=None, color: str=None, similarity=1, scale=1, lpoutput: list=None) -> list[Target]:
        found = []
        if not self.__dmdotsetlib:
            return found
        for area, dotsetname in itertools.product(areas, dotsetname.split('|')):
            for dotset in self.__dmdotsetlib.group(dotsetname):
                dotset = dotset.scale(scale).asmatchcolor(color)
                res = self.__dm.FindMultiColorEx(*area, dotset.matchcolor, dotset.tmpl, similarity, 0)
                if not res: continue
                xs, ys = [[int(coor) for coor in coors.split(',')] for coors in res.split('|')]
                for i in range(min(len(xs), len(ys))):
                    x, y = xs[i], ys[i]
                    start = dotset.getrealpos((x, y))
                    end = start[0] + dotset.width, start[1] + dotset.height
                    found.append(Target(dotsetname, start, end, similarity))
        return found

    @findfunc
    def dmfindword(self, texts: str, areas: _Area|_Areas, color: str, similarity=0.9, lpoutput: list=None) -> Target:
        while self.__dmwordlock: pass
        self.__dmwordlock = True
        found = Target.none
        for area in areas:
            x, y, index = self.__dm.FindStrFast(*area, texts, color, similarity)
            if index > -1:
                found = Target(texts.split('|')[index], (x,y), (x,y), similarity)
                break
        self.__dmwordlock = False
        return found

    @findfunc
    def dmfindwords(self, texts: str, areas: _Area|_Areas, color: str, similarity=0.9, lpoutput: list=None) -> list[Target]:
        while self.__dmwordlock: pass
        self.__dmwordlock = True
        found = []
        textList = texts.split('|')
        for area in areas:
            res = self.__dm.FindStrFastEx(*area, texts, color, similarity)
            if not res: continue
            for info in res.split('|'):
                index, x, y = info.split(',')
                word = textList[int(index)]
                pos = int(x), int(y)
                found.append(Target(word, pos, pos, similarity))
        self.__dmwordlock = False
        return found
