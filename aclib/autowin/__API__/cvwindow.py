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
        self.__cvfontlib = FontLib()
        self.__cvdotsetlib = DotsetLib()

    @property
    def _cvready(self) -> bool:
        return self.__cvready

    FontLib = FontLib
    DotsetLib = DotsetLib

    def cvset(self, fontlib: FontLib|None=..., dotsetlib: DotsetLib|None=...) -> Self:
        """传入None删除已设置的库，不传(或传入...)则不修改"""
        if isinstance(fontlib, FontLib):
            self.__cvfontlib = fontlib
        if isinstance(dotsetlib, DotsetLib):
            self.__cvdotsetlib = dotsetlib
        if fontlib is None:
            self.__cvfontlib = FontLib()
        if dotsetlib is None:
            self.__cvdotsetlib = DotsetLib()
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
        capscale = 1.0,
        lpoutput: list=None
    ) -> Target:
        if len(self.__cvdotsetlib) == 0:
            return Target.none
        for area in areas:
            screenshot = self.cvcapture(area)
            if not screenshot: continue
            if capscale != 1:
                screenshot = screenshot.scale(capscale)
            target = screenshot.finddotset(
                self.__cvdotsetlib, dotsets, matchcolor, similarity)
            if target: return target.scale(1/capscale).offset(*area[:2])
        return Target.none

    @findfunc
    def cvfinddotsets(self,
        dotsets: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        capscale = 1.0,
        ignore_overlaps = False,
        lpoutput: list=None
    ) -> list[Target]:
        found = []
        if len(self.__cvdotsetlib) == 0:
            return found
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            if capscale != 1:
                screenshot = screenshot.scale(capscale)
            targets = screenshot.finddotsets(
                self.__cvdotsetlib, dotsets, matchcolor, similarity, 1, ignore_overlaps)
            found.extend(target.scale(1/capscale).offset(*area[:2]) for target in targets)
        return found

    @findfunc
    def cvfindtext(self,
        texts: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        txtdir: Literal[0,1]=0,
        txtwrap = True,
        capscale = 1.0,
        charset: str|Literal['']=None,
        lpoutput: list=None
    ) -> Target:
        if len(self.__cvfontlib) == 0:
            return Target.none
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            if capscale != 1:
                screenshot = screenshot.scale(capscale)
            target = screenshot.findtext(
                self.__cvfontlib, texts, matchcolor, similarity, txtdir, txtwrap, 1, charset)
            if target: return target.scale(1/capscale).offset(*area[:2])
        return Target.none

    @findfunc
    def cvfindtexts(self,
        texts: str|Sequence[str],
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        txtdir: Literal[0,1]=0,
        txtwrap = True,
        capscale = 1.0,
        charset: str|Literal['']=None,
        ignore_overlaps = False,
        lpoutput: list=None
    ) -> list[Target]:
        found = []
        if len(self.__cvfontlib) == 0:
            return found
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            if capscale != 1:
                screenshot = screenshot.scale(capscale)
            targets = screenshot.findtexts(
                self.__cvfontlib, texts, matchcolor, similarity, txtdir, txtwrap, 1, charset, ignore_overlaps)
            found.extend(target.scale(1/capscale).offset(*area[:2]) for target in targets)
        return found

    @findfunc
    def cvocr(self,
        areas: _Area|_Areas=None,
        matchcolor: Literal[0,1]|HexColorRange=None,
        similarity = 0.9,
        txtdir: Literal[0,1]=0,
        txtwrap = True,
        capscale = 1.0,
        charset: str|Literal['']=None,
        lpoutput: list=None
    ) -> list[Target]:
        texts = []
        if self.__cvfontlib is None:
            return texts
        for area in areas:
            screenshot = self.cvcapture(area)
            if screenshot is None: continue
            if capscale != 1:
                screenshot = screenshot.scale(capscale)
            ocrgroups = screenshot.ocr(
                self.__cvfontlib, matchcolor, similarity, txtdir, txtwrap, 1, charset)
            texts.extend(ocrgroup.join().scale(1/capscale).offset(*area[:2]) for ocrgroup in ocrgroups)
        return texts
