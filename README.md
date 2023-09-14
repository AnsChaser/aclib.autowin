# Installation

### General
    pip install aclib.autowin
### work with dm
    pip install aclib.autowin[dm]
### work with cv
    pip install aclib.autowin[cv]
### full installation
    pip install aclib.autowin[full]


# Usage

```python
from aclib.autowin._typing import *

from aclib.autowin import screen, Window, AppWindow
from aclib.autowin.cvwindow import CvWindow, Target     # [cv] requires
from aclib.autowin.dmwindow import DmWindow, Target     # [dm] requires

# full requires
# if all requires ready, you can get all api from this module
# the classs 'Window' in this module is inherit from 'CvWindow' & 'DmWindow'
from aclib.autowin.windows import screen, Window, AppWindow, Target
```
