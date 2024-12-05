import asyncio.events
import asyncio.locks
import google.protobuf.message
import grpclib.client
import modal._utils.async_utils
import modal_proto.api_grpc
import modal_proto.modal_api_grpc
import synchronicity.combined_types
import typing
import typing_extensions

def _get_metadata(
    client_type: int, credentials: typing.Optional[typing.Tuple[str, str]], version: str
) -> typing.Dict[str, str]: ...

ReturnType = typing.TypeVar("ReturnType")

RequestType = typing.TypeVar("RequestType", bound="google.protobuf.message.Message")

ResponseType = typing.TypeVar("ResponseType", bound="google.protobuf.message.Message")

class _Client:
    _client_from_env: typing.ClassVar[typing.Optional[_Client]]
    _client_from_env_lock: typing.ClassVar[typing.Optional[asyncio.locks.Lock]]
    _cancellation_context: modal._utils.async_utils.TaskContext
    _cancellation_context_event_loop: asyncio.events.AbstractEventLoop
    _stub: typing.Optional[modal_proto.api_grpc.ModalClientStub]

    def __init__(
        self,
        server_url: str,
        client_type: int,
        credentials: typing.Optional[typing.Tuple[str, str]],
        version: str = "0.66.4",
    ): ...
    def is_closed(self) -> bool: ...
    @property
    def stub(self) -> modal_proto.modal_api_grpc.ModalClientModal: ...
    async def _open(self): ...
    async def _close(self, prep_for_restore: bool = False): ...
    async def hello(self): ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc, tb): ...
    @classmethod
    def anonymous(cls, server_url: str) -> typing.AsyncContextManager[_Client]: ...
    @classmethod
    async def from_env(cls, _override_config=None) -> _Client: ...
    @classmethod
    async def from_credentials(cls, token_id: str, token_secret: str) -> _Client: ...
    @classmethod
    async def verify(cls, server_url: str, credentials: typing.Tuple[str, str]) -> None: ...
    @classmethod
    def set_env_client(cls, client: typing.Optional[_Client]): ...
    async def _call_safely(self, coro, readable_method: str): ...
    async def _reset_on_pid_change(self): ...
    async def _get_grpclib_method(self, method_name: str) -> typing.Any: ...
    async def _call_unary(
        self,
        method_name: str,
        request: typing.Any,
        *,
        timeout: typing.Optional[float] = None,
        metadata: typing.Union[
            typing.Mapping[str, typing.Union[str, bytes]],
            typing.Collection[typing.Tuple[str, typing.Union[str, bytes]]],
            None,
        ] = None,
    ) -> typing.Any: ...
    def _call_stream(
        self,
        method_name: str,
        request: typing.Any,
        *,
        metadata: typing.Union[
            typing.Mapping[str, typing.Union[str, bytes]],
            typing.Collection[typing.Tuple[str, typing.Union[str, bytes]]],
            None,
        ],
    ) -> typing.AsyncGenerator[typing.Any, None]: ...

class Client:
    _client_from_env: typing.ClassVar[typing.Optional[Client]]
    _client_from_env_lock: typing.ClassVar[typing.Optional[asyncio.locks.Lock]]
    _cancellation_context: modal._utils.async_utils.TaskContext
    _cancellation_context_event_loop: asyncio.events.AbstractEventLoop
    _stub: typing.Optional[modal_proto.api_grpc.ModalClientStub]

    def __init__(
        self,
        server_url: str,
        client_type: int,
        credentials: typing.Optional[typing.Tuple[str, str]],
        version: str = "0.66.4",
    ): ...
    def is_closed(self) -> bool: ...
    @property
    def stub(self) -> modal_proto.modal_api_grpc.ModalClientModal: ...

    class ___open_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    _open: ___open_spec

    class ___close_spec(typing_extensions.Protocol):
        def __call__(self, prep_for_restore: bool = False): ...
        async def aio(self, prep_for_restore: bool = False): ...

    _close: ___close_spec

    class __hello_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    hello: __hello_spec

    def __enter__(self): ...
    async def __aenter__(self): ...
    def __exit__(self, exc_type, exc, tb): ...
    async def __aexit__(self, exc_type, exc, tb): ...
    @classmethod
    def anonymous(cls, server_url: str) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Client]: ...
    @classmethod
    def from_env(cls, _override_config=None) -> Client: ...
    @classmethod
    def from_credentials(cls, token_id: str, token_secret: str) -> Client: ...
    @classmethod
    def verify(cls, server_url: str, credentials: typing.Tuple[str, str]) -> None: ...
    @classmethod
    def set_env_client(cls, client: typing.Optional[Client]): ...

    class ___call_safely_spec(typing_extensions.Protocol):
        def __call__(self, coro, readable_method: str): ...
        async def aio(self, coro, readable_method: str): ...

    _call_safely: ___call_safely_spec

    class ___reset_on_pid_change_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    _reset_on_pid_change: ___reset_on_pid_change_spec

    class ___get_grpclib_method_spec(typing_extensions.Protocol):
        def __call__(self, method_name: str) -> typing.Any: ...
        async def aio(self, method_name: str) -> typing.Any: ...

    _get_grpclib_method: ___get_grpclib_method_spec

    async def _call_unary(
        self,
        method_name: str,
        request: typing.Any,
        *,
        timeout: typing.Optional[float] = None,
        metadata: typing.Union[
            typing.Mapping[str, typing.Union[str, bytes]],
            typing.Collection[typing.Tuple[str, typing.Union[str, bytes]]],
            None,
        ] = None,
    ) -> typing.Any: ...
    def _call_stream(
        self,
        method_name: str,
        request: typing.Any,
        *,
        metadata: typing.Union[
            typing.Mapping[str, typing.Union[str, bytes]],
            typing.Collection[typing.Tuple[str, typing.Union[str, bytes]]],
            None,
        ],
    ) -> typing.AsyncGenerator[typing.Any, None]: ...

class UnaryUnaryWrapper(typing.Generic[RequestType, ResponseType]):
    wrapped_method: grpclib.client.UnaryUnaryMethod[RequestType, ResponseType]
    client: _Client

    def __init__(self, wrapped_method: grpclib.client.UnaryUnaryMethod[RequestType, ResponseType], client: _Client): ...
    @property
    def name(self) -> str: ...
    async def __call__(
        self,
        req: RequestType,
        *,
        timeout: typing.Optional[float] = None,
        metadata: typing.Union[
            typing.Mapping[str, typing.Union[str, bytes]],
            typing.Collection[typing.Tuple[str, typing.Union[str, bytes]]],
            None,
        ] = None,
    ) -> ResponseType: ...

class UnaryStreamWrapper(typing.Generic[RequestType, ResponseType]):
    wrapped_method: grpclib.client.UnaryStreamMethod[RequestType, ResponseType]

    def __init__(
        self, wrapped_method: grpclib.client.UnaryStreamMethod[RequestType, ResponseType], client: _Client
    ): ...
    @property
    def name(self) -> str: ...
    def unary_stream(self, request, metadata: typing.Optional[typing.Any] = None): ...

HEARTBEAT_INTERVAL: float

HEARTBEAT_TIMEOUT: float

CLIENT_CREATE_ATTEMPT_TIMEOUT: float

CLIENT_CREATE_TOTAL_TIMEOUT: float
