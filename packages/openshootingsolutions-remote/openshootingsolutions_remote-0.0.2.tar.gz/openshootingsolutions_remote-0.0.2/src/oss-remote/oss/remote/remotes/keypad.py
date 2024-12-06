"""A Keypad BaseRemote implementation"""

from enum import Enum
from typing import Callable

import keyboard
from oss.core.log import Log
from oss.core.models.base.remote import BaseHook, BaseRemote
from oss.core.models.base.timer import TimerControl

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


class KeypadAction(Enum):
    """A mapping between keystrokes and timer actions to send via the message broker"""

    Q: TimerControl = TimerControl.TOGGLE_PHASE
    W: TimerControl = TimerControl.RESET_PHASE
    E: TimerControl = TimerControl.SET_TOGGLE_DELAY


class KeypadHook(BaseHook):
    """A keypad hook for capturing a keystroke.

    The hook captures the keystroke and executes the callback function that has been passed on initialization.
    """

    _unhook_callable: Callable[[], None]

    def register(self) -> None:
        """
        Registers a keyboard hotkey and associate it with a callback function. When the specified key (self.name)
        is pressed, the callback function (self.callback) is called with the provided arguments (self.action).
        This method uses the 'keyboard' library to add the hotkey and sets a removal function to clean up the hook
        when needed.

        Sets:
          self._unhook_callable: A function that removes the hotkey hook when called.
        """
        # The add_hotkey function configures a keyboard hook, but returns a remove function as a result.
        hook_remove_function: Callable[[], None] = keyboard.add_hotkey(
            hotkey=self.name,  # Name is a reference to the KEY of the action Enum. This is the keystroke to press.
            callback=self.callback,  # The function to be called on keypress. This is the hook handle function.
            args=[self.action],  # The arguments passed to the hook handle function. This is the action to be executed.
            timeout=0.1,  # The minimum amount of time that the key needs to be pressed.
        )

        # Set the hook remove function to this class. This function is needed to remove the ook.
        self._unhook_callable = hook_remove_function

    def remove(self):
        """
        Removes the hook by calling the unhook callable method.

        Unhooks any function or method that was previously hooked by invoking
        the internal `_unhook_callable` method of the instance.
        """
        self._unhook_callable()


class KeypadRemote(BaseRemote):
    """A keypad remote for controlling OSS components

    This is a keypad implementation of a BaseRemote.
    A keypad is a (small) keyboard that sends keystrokes like: Q,W,E,R,T,Y.
    """

    _hook_type: type[KeypadHook] = KeypadHook  # Hook type for this remote
    _action_schema: type[KeypadAction] = KeypadAction  # Mapped actions for this remote
