from .__API__.screen import screen
from .__API__.appwindow import AppWindow
from .__API__.cvwindow import CvWindow
from .__API__.dmwindow import DmWindow
from .__API__._target import Target

class Window(CvWindow, DmWindow): ...
