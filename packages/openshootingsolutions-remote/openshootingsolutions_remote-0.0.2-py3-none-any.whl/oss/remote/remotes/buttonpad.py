"""A Buttonpad BaseRemote implementation"""

from enum import Enum
from typing import Callable

from oss.core.log import Log
from oss.core.models.base.remote import BaseHook, BaseRemote
from oss.core.models.base.timer import TimerControl

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


class ButtonpadAction(Enum):
    """A mapping between keystrokes and timer actions to send via the message broker"""

    GPIO1: TimerControl = TimerControl.TOGGLE_PHASE
    GPIO2: TimerControl = TimerControl.RESET_PHASE
    GPIO3: TimerControl = TimerControl.NEXT_STAGE
    GPIO4: TimerControl = TimerControl.PREVIOUS_STAGE


class ButtonpadHook(BaseHook):
    """A GPIO hook for capturing a buttonpress.

    The hook captures the buttonpress and executes the callback function that has been passed on initialization.
    """

    _unhook_callable: Callable[[], None]

    def register(self) -> None:
        """Registers a hook for a keypress

        Returns:
            None
        """
        # Need to write this implementation
        pass

    def remove(self):
        # Need to write this implementation
        pass


class ButtonpadRemote(BaseRemote):
    """A Buttonpad remote for controlling OSS components

    This is a buttonpad implementation of a BaseRemote.
    A keypad is a collection of GPIO inputs that sends HIGH/LOW signals on GPIO pins
    """

    _hook_type: type[ButtonpadHook] = ButtonpadHook  # The type of hook that is needed for this remote
    _action_schema: type[ButtonpadAction] = ButtonpadAction  # The actions that are mapped for this remote
