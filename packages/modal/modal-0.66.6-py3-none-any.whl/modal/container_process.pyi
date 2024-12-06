import modal.client
import modal.io_streams
import modal.stream_type
import typing
import typing_extensions

class _ContainerProcess:
    _process_id: typing.Optional[str]
    _stdout: modal.io_streams._StreamReader
    _stderr: modal.io_streams._StreamReader
    _stdin: modal.io_streams._StreamWriter
    _returncode: typing.Optional[int]

    def __init__(
        self,
        process_id: str,
        client: modal.client._Client,
        stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
    ) -> None: ...
    @property
    def stdout(self) -> modal.io_streams._StreamReader: ...
    @property
    def stderr(self) -> modal.io_streams._StreamReader: ...
    @property
    def stdin(self) -> modal.io_streams._StreamWriter: ...
    @property
    def returncode(self) -> modal.io_streams._StreamWriter: ...
    async def poll(self) -> typing.Optional[int]: ...
    async def wait(self) -> int: ...
    async def attach(self, *, pty: bool): ...

class ContainerProcess:
    _process_id: typing.Optional[str]
    _stdout: modal.io_streams.StreamReader
    _stderr: modal.io_streams.StreamReader
    _stdin: modal.io_streams.StreamWriter
    _returncode: typing.Optional[int]

    def __init__(
        self,
        process_id: str,
        client: modal.client.Client,
        stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
    ) -> None: ...
    @property
    def stdout(self) -> modal.io_streams.StreamReader: ...
    @property
    def stderr(self) -> modal.io_streams.StreamReader: ...
    @property
    def stdin(self) -> modal.io_streams.StreamWriter: ...
    @property
    def returncode(self) -> modal.io_streams.StreamWriter: ...

    class __poll_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Optional[int]: ...
        async def aio(self) -> typing.Optional[int]: ...

    poll: __poll_spec

    class __wait_spec(typing_extensions.Protocol):
        def __call__(self) -> int: ...
        async def aio(self) -> int: ...

    wait: __wait_spec

    class __attach_spec(typing_extensions.Protocol):
        def __call__(self, *, pty: bool): ...
        async def aio(self, *, pty: bool): ...

    attach: __attach_spec
