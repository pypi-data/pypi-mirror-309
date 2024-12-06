__all__ = [
    "exec_task",
    "exec_ui",
    "StatusType",

    "RUNNABLE_APP",
    "RUNNABLE_KERNEL",
    "RUNNABLE_NON_SELECTED",
    "RUNNABLE_SCRIPT",
]

from enum import IntEnum

from .exec import exec_task
from .exec import exec_ui
from .exec import StatusType

# from utypes import Directory
# from utypes import FilePath
# from utypes import FileNmae
# from utypes import CallBack
# from utypes import FixedList
# from utypes import ListList

RUNNABLE_NON_SELECTED = 0
RUNNABLE_KERNEL = 1
RUNNABLE_APP = 2
RUNNABLE_SCRIPT = 3


class TaskKind(IntEnum):
    BUTTON = 0b00000001
    """Identifies a function to be called after a clicked event on a button in the UI."""
    RECURRING = 0b00000010
    """Identifies a function to be called recurrently with a timer from the UI."""
