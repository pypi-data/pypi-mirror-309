from io import BytesIO

from ..api.tool_identity import ToolIdentity
from ..rpc import RPCClient


class ContainerError(Exception):
    """Error caused by incorrect use of the ContainerTool"""


class Job:
    def __init__(self, tool_id: ToolIdentity, rpc: RPCClient) -> None:
        self._tool_id = tool_id
        self._rpc = rpc
        self._stdout: BytesIO | None = None

    @property
    def is_running(self) -> bool:
        """Whether the container is running"""

        return self._rpc.tools_container_get_state(self._tool_id).running

    def kill(self) -> None:
        """Send SIGKILL to the container"""

        self._signal("kill")

    def terminate(self) -> None:
        """Send SIGTERM to the container"""

        self._signal("term")

    def _signal(self, signal: str) -> None:
        """Send a signal to the container"""

        self._rpc.tools_container_signal(self._tool_id, signal)

    @property
    def stdout(self) -> BytesIO:
        """Get stdout from the container"""
        if self._stdout is None:
            self._stdout = BytesIO(self._rpc.tools_container_get_stdout(self._tool_id))
        return self._stdout

    @property
    def return_code(self) -> int:
        """The return code of the job"""
        state = self._rpc.tools_container_get_state(self._tool_id)
        if state.return_code is None:
            raise ContainerError("Can't get the return code of a running container")
        return state.return_code


class ContainerTool:
    """A Container Tool"""

    def __init__(self, rpc: RPCClient, tool_id: str):
        self._tool_id = ToolIdentity(tool_id=tool_id)
        self._rpc = rpc

    def run(
        self,
        container: str,
        command: list[str],
        username: str | None = None,
        password: str | None = None,
    ) -> Job:
        """Run the command in the container"""

        self._rpc.tools_container_run(
            self._tool_id, container, command, username, password
        )
        return Job(self._tool_id, self._rpc)

    def reset(self) -> None:
        """Reset the tool"""

        self._rpc.rig_tools_reset(self._tool_id)
