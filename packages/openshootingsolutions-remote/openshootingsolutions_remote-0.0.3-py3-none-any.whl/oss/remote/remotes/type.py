from enum import Enum

from oss.remote.remotes.buttonpad import ButtonpadHook, ButtonpadRemote
from oss.remote.remotes.keypad import KeypadHook, KeypadRemote


class RemoteType(Enum):
    KEYPAD: type[KeypadRemote] = KeypadRemote
    BUTTONPAD: type[ButtonpadRemote] = ButtonpadRemote


class HookType(Enum):
    KEYPAD: type[KeypadHook] = KeypadHook
    BUTTONPAD: type[ButtonpadHook] = ButtonpadHook
