from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Sequence, Literal
    from ._typing import _Area, _Areas

from aclib.cv import Image, FontLib, DotsetLib
from aclib.cv._typing import HexColorRange
from aclib.winlib import winapi

from ._functool import findfunc
from ._target import Target
from .window import Window


class CvWindow(Window):

    def _init_(self, hwnd: int):
        super()._init_(hwnd)
        self.__cvready = True
        self.__cvfontlib: FontLib = None
        self.__cvdotsetlib: DotsetLib = None

    @property
    def _cvready(self) -> bool:
        return self.__cvready

    def cvset(self, fontlib: str|None='', dotsetlib: str|None='', flibscale=1.0, dlibscale=1.0) -> Self:
        if fontlib:
            self.__cvfontlib = FontLib.fromfile(fontlib).scale(flibscale)
        if dotsetlib:
            self.__cvdotsetlib = DotsetLib.fromfile(dotsetlib).scale(dlibscale)
        if fontlib is None:
            self.__cvfontlib = None
        if dotsetlib is None:
            self.__cvdotsetlib = None
        return self

    def cvcapture(self, area: _Area=None, savepath='') -> Image | None:
        size, buffer = winapi.CaptureWindow(self.handle, area)
        screenshot = Image.frombuffer(buffer, size)
        if savepath:
            screenshot.tofile(savepath)
        return screenshot

    @findfunc
    def cvfindcolor(self, rgbranges: HexColorRange, areas: _Area|_Areas=None, lpoutput: list=None) -> Target:
        for area in areas:
            screenshot = self.cvcapture(area)
            if not screenshot: continue
            target = screenshot.findcolor(rgbranges)
            if not target: continue
            return target.offset(*area[:2])
        return Target.none

    @findfunc
    def cvfindcolors(self, rgbranges: HexColorRange, areas: _Area|_Areas=None, lpoutput: list=None) -> list[Target]:
        found = []
        for area in areas:
            screenshot = self.cvcapture(area)
            if not screenshot: continue
            targets = screenshot.findcolors(rgbranges)
            found.extend(target.offset(*area[:2]) for target in targets)
        return found

    @findfunc
    def cvfinddotset(self,
        dotsets: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        scale = 1.0,
        lpoutput: list=None
    ) -> Target:
        if self.__cvdotsetlib is None:
            return Target.none
        for area in areas:
            screenshot = self.cvcapture(area)
            if not screenshot: continue
            target = screenshot.finddotset(
                self.__cvdotsetlib, dotsets, matchcolor, similarity, scale)
            if target: return target.offset(*area[:2])
        return Target.none

    @findfunc
    def cvfinddotsets(self,
        dotsets: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        scale = 1.0,
        ignore_overlaps = False,
        lpoutput: list=None
    ) -> list[Target]:
        found = []
        if self.__cvdotsetlib is None:
            return found
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            targets = screenshot.finddotsets(
                self.__cvdotsetlib, dotsets, matchcolor, similarity, scale, ignore_overlaps)
            found.extend(target.offset(*area[:2]) for target in targets)
        return found

    @findfunc
    def cvfindtext(self,
        texts: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        txtdir: Literal[0,1]=0,
        txtwrap = True,
        charscale = 1.0,
        charset: str|Literal['']=None,
        lpoutput: list=None
    ) -> Target:
        if self.__cvfontlib is None:
            return Target.none
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            target = screenshot.findtext(
                self.__cvfontlib, texts, matchcolor, similarity, txtdir, txtwrap, charscale, charset)
            if target: return target.offset(*area[:2])
        return Target.none

    @findfunc
    def cvfindtexts(self,
        texts: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        txtdir: Literal[0,1]=0,
        txtwrap = True,
        charscale = 1.0,
        charset: str|Literal['']=None,
        ignore_overlaps = False,
        lpoutput: list=None
    ) -> list[Target]:
        found = []
        if self.__cvfontlib is None:
            return found
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            targets = screenshot.findtexts(
                self.__cvfontlib, texts, matchcolor, similarity, txtdir, txtwrap, charscale, charset, ignore_overlaps)
            found.extend(target.offset(*area[:2]) for target in targets)
        return found

    @findfunc
    def cvocr(self,
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        txtdir: Literal[0,1]=0,
        txtwrap = True,
        charscale = 1.0,
        charset: str|Literal['']=None,
        lpoutput: list=None
    ) -> list[str]:
        texts = []
        if self.__cvfontlib is None:
            return texts
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            ocrgroups = screenshot.ocr(
                self.__cvfontlib, matchcolor, similarity, txtdir, txtwrap, charscale, charset)
            texts.extend(ocrgroup.join().name for ocrgroup in ocrgroups)
        return texts
