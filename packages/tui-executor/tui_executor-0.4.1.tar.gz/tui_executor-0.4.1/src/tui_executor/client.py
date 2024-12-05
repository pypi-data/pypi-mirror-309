import logging
import queue
from typing import Callable
from typing import List
from typing import TYPE_CHECKING
from typing import Tuple

from jupyter_client import BlockingKernelClient
from rich.text import Text

if TYPE_CHECKING:
    from tui_executor.kernel import MyKernel

from tui_executor.utils import decode_traceback

LOGGER = logging.getLogger("tui-executor.client")

DEBUG = True
"""Enable/disable all debugging log messages in this module."""


class MyClient:
    def __init__(self, kernel: "MyKernel", startup_timeout: float = 60.0, timeout: float = 1.0):
        self._timeout = timeout
        """The timeout used when communicating with the kernel."""

        self._startup_timeout = startup_timeout
        """The timeout used when starting up channels to the server."""

        self._error = None

        self._client: BlockingKernelClient = kernel.get_kernel_manager().client()

    def connect(self):
        DEBUG and LOGGER.debug(f"{id(self)}: Opening channels for client [{self}]...")
        self.start_channels()

    def disconnect(self):
        DEBUG and LOGGER.debug(f"{id(self)}: Closing channels for client [{self}]...")
        self.stop_channels()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def start_channels(self):
        self._client.start_channels()
        try:
            self._client.wait_for_ready(timeout=self._startup_timeout)
        except RuntimeError:
            self._client.stop_channels()
            raise
        except AttributeError as exc:
            LOGGER.error(
                f"The client that was created doesn't have the expected method 'wait_for_ready()'. "
                f"The client should be a BlockingKernelClient or an AsyncKernelClient, but it is {type(self._client)}."
            )
            raise

    def stop_channels(self):
        self._client.stop_channels()

    def get_kernel_info(self) -> dict:
        """Returns a dictionary with information about the Jupyter kernel."""
        msg_id = self._client.kernel_info()
        DEBUG and LOGGER.debug(f"{id(self)}: {msg_id = }")

        shell_msg = self._client.get_shell_msg()
        DEBUG and LOGGER.debug(f"{id(self)}: {shell_msg = }")

        return shell_msg['content']

    # Channel proxy methods ------------------------------

    async def get_shell_msg(self, *args, **kwargs):
        """Get a message from the shell channel"""
        return await self._client.get_shell_msg(*args, **kwargs)

    def get_iopub_msg(self, *args, **kwargs):
        """Get a message from the iopub channel"""
        return self._client.get_iopub_msg(*args, **kwargs)

    def get_stdin_msg(self, *args, **kwargs):
        """Get a message from the stdin channel"""
        return self._client.get_stdin_msg(*args, **kwargs)

    def get_control_msg(self, *args, **kwargs):
        """Get a message from the control channel"""
        return self._client.get_control_msg(*args, **kwargs)

    def get_error(self):
        return self._error

    def clear_error(self):
        self._error = None

    def input(self, input_string: str):
        """
        Send a string of raw input to the kernel.

        This should only be called in response to the kernel sending an `input_request` message on the stdin channel.
        """

        self._client.input(input_string)

    def execute(self, snippet: str, allow_stdin: bool = True) -> str:
        return self._client.execute(f"{snippet}\n", allow_stdin=allow_stdin)

    def run_snippet(
            self,
            snippet: str,
            allow_stdin: bool = True,
            notify: Callable = lambda x, y: ...
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Execute the code snippet in the kernel. The snippet can be a multiline command.

        Returns:
            A tuple with three lists:

            - the command that was given, i.e. the code snippet
            - the output of the code that was executed
            - the error message or traceback if there was an error

            The lists may be empty.
        """
        msg_id = self._client.execute(f"{snippet}\n", allow_stdin=allow_stdin)

        DEBUG and LOGGER.debug(f"{id(self)}: {msg_id = }")

        # fetch the output

        cmd: List[str] = []
        std_out: List[str] = []
        std_err: List[str] = []

        while True:
            try:
                io_msg = self._client.get_iopub_msg(timeout=self._timeout)
                io_msg_type = io_msg['msg_type']
                io_msg_content = io_msg['content']

                DEBUG and LOGGER.debug(f"{id(self)}: io_msg = {io_msg}")
                DEBUG and LOGGER.debug(f"{id(self)}: io_msg_type = {io_msg_type}")
                DEBUG and LOGGER.debug(f"{id(self)}: io_msg_content = {io_msg_content}")

                if io_msg_type == 'status':
                    if io_msg_content['execution_state'] == 'idle':
                        # self.signals.data.emit("Execution State is Idle, terminating...")
                        DEBUG and LOGGER.debug(f"{id(self)}: Execution State is Idle, terminating...")
                        break
                elif io_msg_type == 'stream':
                    if 'text' in io_msg_content:
                        text = io_msg_content['text'].rstrip()
                        # std_out.extend(text.split('\n'))
                        notify(Text.from_ansi(text), level=logging.NOTSET)
                elif io_msg_type == 'display_data':
                    if 'data' in io_msg_content:
                        if 'text/plain' in io_msg_content['data']:
                            text = io_msg_content['data']['text/plain'].rstrip()
                            # std_out.extend(text.split('\n'))
                            notify(Text.from_ansi(text), level=logging.NOTSET)
                elif io_msg_type == 'execute_input':
                    if 'code' in io_msg_content:
                        text = io_msg_content['code'].rstrip()
                        cmd.extend(text.split('\n'))
                elif io_msg_type == 'error':
                    if 'traceback' in io_msg_content:
                        text = io_msg_content['traceback']
                        std_err.extend(decode_traceback(text).split('\n'))
                elif io_msg_type == 'execute_result':
                    ...  # ignore this message type
                else:
                    raise RuntimeError(f"Unknown io_msg_type: {io_msg_type}")
            except queue.Empty:
                ...

        DEBUG and LOGGER.debug(f"{id(self)}: {cmd     = }")
        DEBUG and LOGGER.debug(f"{id(self)}: {std_out = }")
        DEBUG and LOGGER.debug(f"{id(self)}: {std_err = }")

        # fetch the reply message

        reply = self._client.get_shell_msg(timeout=1.0)

        DEBUG and LOGGER.debug(f"{id(self)}: {type(reply) = }")
        DEBUG and LOGGER.debug(f"{id(self)}: {reply = }")
        DEBUG and LOGGER.debug(f"{id(self)}: {reply['content'] = }")

        if reply["content"]["status"] == "error":
            try:
                self._error = decode_traceback(reply["content"]["traceback"])
            except KeyError:
                self._error = "An error occurred, no traceback was provided."
        else:
            self._error = None

        return cmd, std_out, std_err

    def __del__(self):
        if self._client:
            self._client.stop_channels()
