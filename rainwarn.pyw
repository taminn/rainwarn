import os,sys
import threading

sys.path.append(sys.path[0]+'\\modules')

import Weatherwarn
import Eventwarn

threading.Thread(target=Weatherwarn.Warn).start()
threading.Thread(target=Eventwarn.Warn).start()