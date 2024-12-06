import datetime
from importlib.metadata import version

name = "miner3"
GIT_SHA = '$Id: 70651e1e2273f1f26f89ba03928674b7115c2ae3 $'

try:
    __version__ = version(name)
except:
    __version__ = 'development'

