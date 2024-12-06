from oss.core.log import Log
from oss.core.models.base.app import BaseApp
from oss.core.models.base.remote import BaseRemote
from oss.remote.remotes.type import RemoteType

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


class RemoteApp(BaseApp):
    _remote: BaseRemote

    def __init__(self, remote: RemoteType) -> None:
        # If there are timers as a parameter, add them to the timer list.
        if remote:
            # Initialize the passed in remote and make it the remote of this remote app
            self._remote = remote.value()
            logger.info(self._identifier)
        else:
            # We have a major problem a remote app without a remote
            logger.critical("Cannot start app. No remote or invalid remote specified")
            self.terminate()

    def __del__(self):
        self.terminate()

    def run(self) -> None:
        while True:
            # don't have much to do right now :)
            pass

    def terminate(self) -> None:
        # Terminate old connections to the message broker
        pass
