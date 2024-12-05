import asyncio
import asyncio.locks
import asyncio.queues
import modal._asgi
import modal.client
import modal.running_app
import modal_proto.api_pb2
import synchronicity.combined_types
import typing
import typing_extensions

class UserException(Exception): ...
class Sentinel: ...

class FinalizedFunction:
    callable: typing.Callable[..., typing.Any]
    is_async: bool
    is_generator: bool
    data_format: int
    lifespan_manager: typing.Optional[modal._asgi.LifespanManager]

    def __init__(
        self,
        callable: typing.Callable[..., typing.Any],
        is_async: bool,
        is_generator: bool,
        data_format: int,
        lifespan_manager: typing.Optional[modal._asgi.LifespanManager] = None,
    ) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...

class IOContext:
    input_ids: typing.List[str]
    function_call_ids: typing.List[str]
    finalized_function: FinalizedFunction
    _cancel_issued: bool
    _cancel_callback: typing.Optional[typing.Callable[[], None]]

    def __init__(
        self,
        input_ids: typing.List[str],
        function_call_ids: typing.List[str],
        finalized_function: FinalizedFunction,
        function_inputs: typing.List[modal_proto.api_pb2.FunctionInput],
        is_batched: bool,
        client: modal.client._Client,
    ): ...
    @classmethod
    async def create(
        cls,
        client: modal.client._Client,
        finalized_functions: typing.Dict[str, FinalizedFunction],
        inputs: typing.List[typing.Tuple[str, str, modal_proto.api_pb2.FunctionInput]],
        is_batched: bool,
    ) -> IOContext: ...
    def set_cancel_callback(self, cb: typing.Callable[[], None]): ...
    def cancel(self): ...
    def _args_and_kwargs(
        self,
    ) -> typing.Tuple[typing.Tuple[typing.Any, ...], typing.Dict[str, typing.List[typing.Any]]]: ...
    def call_finalized_function(self) -> typing.Any: ...
    def validate_output_data(self, data: typing.Any) -> typing.List[typing.Any]: ...

class InputSlots:
    active: int
    value: int
    waiter: typing.Optional[asyncio.Future]
    closed: bool

    def __init__(self, value: int) -> None: ...
    async def acquire(self) -> None: ...
    def _wake_waiter(self) -> None: ...
    def release(self) -> None: ...
    def set_value(self, value: int) -> None: ...
    async def close(self) -> None: ...

class _ContainerIOManager:
    task_id: str
    function_id: str
    app_id: str
    function_def: modal_proto.api_pb2.Function
    checkpoint_id: typing.Optional[str]
    calls_completed: int
    total_user_time: float
    current_input_id: typing.Optional[str]
    current_inputs: typing.Dict[str, IOContext]
    current_input_started_at: typing.Optional[float]
    _target_concurrency: int
    _max_concurrency: int
    _concurrency_loop: typing.Optional[asyncio.Task]
    _input_slots: InputSlots
    _environment_name: str
    _heartbeat_loop: typing.Optional[asyncio.Task]
    _heartbeat_condition: typing.Optional[asyncio.locks.Condition]
    _waiting_for_memory_snapshot: bool
    _is_interactivity_enabled: bool
    _fetching_inputs: bool
    _client: modal.client._Client
    _GENERATOR_STOP_SENTINEL: typing.ClassVar[Sentinel]
    _singleton: typing.ClassVar[typing.Optional[_ContainerIOManager]]

    def _init(self, container_args: modal_proto.api_pb2.ContainerArguments, client: modal.client._Client): ...
    @property
    def heartbeat_condition(self) -> asyncio.locks.Condition: ...
    @staticmethod
    def __new__(
        cls, container_args: modal_proto.api_pb2.ContainerArguments, client: modal.client._Client
    ) -> _ContainerIOManager: ...
    @classmethod
    def _reset_singleton(cls): ...
    async def _run_heartbeat_loop(self): ...
    async def _heartbeat_handle_cancellations(self) -> bool: ...
    def heartbeats(self, wait_for_mem_snap: bool) -> typing.AsyncContextManager[None]: ...
    def stop_heartbeat(self): ...
    def dynamic_concurrency_manager(self) -> typing.AsyncContextManager[None]: ...
    async def _dynamic_concurrency_loop(self): ...
    async def get_app_objects(self) -> modal.running_app.RunningApp: ...
    async def get_serialized_function(
        self,
    ) -> typing.Tuple[typing.Optional[typing.Any], typing.Optional[typing.Callable[..., typing.Any]]]: ...
    def serialize(self, obj: typing.Any) -> bytes: ...
    def deserialize(self, data: bytes) -> typing.Any: ...
    def serialize_data_format(self, obj: typing.Any, data_format: int) -> bytes: ...
    async def format_blob_data(self, data: bytes) -> typing.Dict[str, typing.Any]: ...
    def get_data_in(self, function_call_id: str) -> typing.AsyncIterator[typing.Any]: ...
    async def put_data_out(
        self, function_call_id: str, start_index: int, data_format: int, messages_bytes: typing.List[typing.Any]
    ) -> None: ...
    async def generator_output_task(
        self, function_call_id: str, data_format: int, message_rx: asyncio.queues.Queue
    ) -> None: ...
    async def _queue_create(self, size: int) -> asyncio.queues.Queue: ...
    async def _queue_put(self, queue: asyncio.queues.Queue, value: typing.Any) -> None: ...
    def get_average_call_time(self) -> float: ...
    def get_max_inputs_to_fetch(self): ...
    def _generate_inputs(
        self, batch_max_size: int, batch_wait_ms: int
    ) -> typing.AsyncIterator[typing.List[typing.Tuple[str, str, modal_proto.api_pb2.FunctionInput]]]: ...
    def run_inputs_outputs(
        self, finalized_functions: typing.Dict[str, FinalizedFunction], batch_max_size: int = 0, batch_wait_ms: int = 0
    ) -> typing.AsyncIterator[IOContext]: ...
    async def _push_outputs(
        self,
        io_context: IOContext,
        started_at: float,
        data_format: int,
        results: typing.List[modal_proto.api_pb2.GenericResult],
    ) -> None: ...
    def serialize_exception(self, exc: BaseException) -> bytes: ...
    def serialize_traceback(
        self, exc: BaseException
    ) -> typing.Tuple[typing.Optional[bytes], typing.Optional[bytes]]: ...
    def handle_user_exception(self) -> typing.AsyncContextManager[None]: ...
    def handle_input_exception(self, io_context: IOContext, started_at: float) -> typing.AsyncContextManager[None]: ...
    def exit_context(self, started_at, input_ids: typing.List[str]): ...
    async def push_outputs(
        self, io_context: IOContext, started_at: float, data: typing.Any, data_format: int
    ) -> None: ...
    async def memory_restore(self) -> None: ...
    async def memory_snapshot(self) -> None: ...
    async def volume_commit(self, volume_ids: typing.List[str]) -> None: ...
    async def interact(self, from_breakpoint: bool = False): ...
    @property
    def target_concurrency(self) -> int: ...
    @property
    def max_concurrency(self) -> int: ...
    @classmethod
    def get_input_concurrency(cls) -> int: ...
    @classmethod
    def set_input_concurrency(cls, concurrency: int): ...
    @classmethod
    def stop_fetching_inputs(cls): ...

class ContainerIOManager:
    task_id: str
    function_id: str
    app_id: str
    function_def: modal_proto.api_pb2.Function
    checkpoint_id: typing.Optional[str]
    calls_completed: int
    total_user_time: float
    current_input_id: typing.Optional[str]
    current_inputs: typing.Dict[str, IOContext]
    current_input_started_at: typing.Optional[float]
    _target_concurrency: int
    _max_concurrency: int
    _concurrency_loop: typing.Optional[asyncio.Task]
    _input_slots: InputSlots
    _environment_name: str
    _heartbeat_loop: typing.Optional[asyncio.Task]
    _heartbeat_condition: typing.Optional[asyncio.locks.Condition]
    _waiting_for_memory_snapshot: bool
    _is_interactivity_enabled: bool
    _fetching_inputs: bool
    _client: modal.client.Client
    _GENERATOR_STOP_SENTINEL: typing.ClassVar[Sentinel]
    _singleton: typing.ClassVar[typing.Optional[ContainerIOManager]]

    def __init__(self, /, *args, **kwargs): ...
    def _init(self, container_args: modal_proto.api_pb2.ContainerArguments, client: modal.client.Client): ...
    @property
    def heartbeat_condition(self) -> asyncio.locks.Condition: ...
    @classmethod
    def _reset_singleton(cls): ...

    class ___run_heartbeat_loop_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    _run_heartbeat_loop: ___run_heartbeat_loop_spec

    class ___heartbeat_handle_cancellations_spec(typing_extensions.Protocol):
        def __call__(self) -> bool: ...
        async def aio(self) -> bool: ...

    _heartbeat_handle_cancellations: ___heartbeat_handle_cancellations_spec

    class __heartbeats_spec(typing_extensions.Protocol):
        def __call__(
            self, wait_for_mem_snap: bool
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(self, wait_for_mem_snap: bool) -> typing.AsyncContextManager[None]: ...

    heartbeats: __heartbeats_spec

    def stop_heartbeat(self): ...

    class __dynamic_concurrency_manager_spec(typing_extensions.Protocol):
        def __call__(self) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(self) -> typing.AsyncContextManager[None]: ...

    dynamic_concurrency_manager: __dynamic_concurrency_manager_spec

    class ___dynamic_concurrency_loop_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    _dynamic_concurrency_loop: ___dynamic_concurrency_loop_spec

    class __get_app_objects_spec(typing_extensions.Protocol):
        def __call__(self) -> modal.running_app.RunningApp: ...
        async def aio(self) -> modal.running_app.RunningApp: ...

    get_app_objects: __get_app_objects_spec

    class __get_serialized_function_spec(typing_extensions.Protocol):
        def __call__(
            self,
        ) -> typing.Tuple[typing.Optional[typing.Any], typing.Optional[typing.Callable[..., typing.Any]]]: ...
        async def aio(
            self,
        ) -> typing.Tuple[typing.Optional[typing.Any], typing.Optional[typing.Callable[..., typing.Any]]]: ...

    get_serialized_function: __get_serialized_function_spec

    def serialize(self, obj: typing.Any) -> bytes: ...
    def deserialize(self, data: bytes) -> typing.Any: ...
    def serialize_data_format(self, obj: typing.Any, data_format: int) -> bytes: ...

    class __format_blob_data_spec(typing_extensions.Protocol):
        def __call__(self, data: bytes) -> typing.Dict[str, typing.Any]: ...
        async def aio(self, data: bytes) -> typing.Dict[str, typing.Any]: ...

    format_blob_data: __format_blob_data_spec

    class __get_data_in_spec(typing_extensions.Protocol):
        def __call__(self, function_call_id: str) -> typing.Iterator[typing.Any]: ...
        def aio(self, function_call_id: str) -> typing.AsyncIterator[typing.Any]: ...

    get_data_in: __get_data_in_spec

    class __put_data_out_spec(typing_extensions.Protocol):
        def __call__(
            self, function_call_id: str, start_index: int, data_format: int, messages_bytes: typing.List[typing.Any]
        ) -> None: ...
        async def aio(
            self, function_call_id: str, start_index: int, data_format: int, messages_bytes: typing.List[typing.Any]
        ) -> None: ...

    put_data_out: __put_data_out_spec

    class __generator_output_task_spec(typing_extensions.Protocol):
        def __call__(self, function_call_id: str, data_format: int, message_rx: asyncio.queues.Queue) -> None: ...
        async def aio(self, function_call_id: str, data_format: int, message_rx: asyncio.queues.Queue) -> None: ...

    generator_output_task: __generator_output_task_spec

    class ___queue_create_spec(typing_extensions.Protocol):
        def __call__(self, size: int) -> asyncio.queues.Queue: ...
        async def aio(self, size: int) -> asyncio.queues.Queue: ...

    _queue_create: ___queue_create_spec

    class ___queue_put_spec(typing_extensions.Protocol):
        def __call__(self, queue: asyncio.queues.Queue, value: typing.Any) -> None: ...
        async def aio(self, queue: asyncio.queues.Queue, value: typing.Any) -> None: ...

    _queue_put: ___queue_put_spec

    def get_average_call_time(self) -> float: ...
    def get_max_inputs_to_fetch(self): ...

    class ___generate_inputs_spec(typing_extensions.Protocol):
        def __call__(
            self, batch_max_size: int, batch_wait_ms: int
        ) -> typing.Iterator[typing.List[typing.Tuple[str, str, modal_proto.api_pb2.FunctionInput]]]: ...
        def aio(
            self, batch_max_size: int, batch_wait_ms: int
        ) -> typing.AsyncIterator[typing.List[typing.Tuple[str, str, modal_proto.api_pb2.FunctionInput]]]: ...

    _generate_inputs: ___generate_inputs_spec

    class __run_inputs_outputs_spec(typing_extensions.Protocol):
        def __call__(
            self,
            finalized_functions: typing.Dict[str, FinalizedFunction],
            batch_max_size: int = 0,
            batch_wait_ms: int = 0,
        ) -> typing.Iterator[IOContext]: ...
        def aio(
            self,
            finalized_functions: typing.Dict[str, FinalizedFunction],
            batch_max_size: int = 0,
            batch_wait_ms: int = 0,
        ) -> typing.AsyncIterator[IOContext]: ...

    run_inputs_outputs: __run_inputs_outputs_spec

    class ___push_outputs_spec(typing_extensions.Protocol):
        def __call__(
            self,
            io_context: IOContext,
            started_at: float,
            data_format: int,
            results: typing.List[modal_proto.api_pb2.GenericResult],
        ) -> None: ...
        async def aio(
            self,
            io_context: IOContext,
            started_at: float,
            data_format: int,
            results: typing.List[modal_proto.api_pb2.GenericResult],
        ) -> None: ...

    _push_outputs: ___push_outputs_spec

    def serialize_exception(self, exc: BaseException) -> bytes: ...
    def serialize_traceback(
        self, exc: BaseException
    ) -> typing.Tuple[typing.Optional[bytes], typing.Optional[bytes]]: ...

    class __handle_user_exception_spec(typing_extensions.Protocol):
        def __call__(self) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(self) -> typing.AsyncContextManager[None]: ...

    handle_user_exception: __handle_user_exception_spec

    class __handle_input_exception_spec(typing_extensions.Protocol):
        def __call__(
            self, io_context: IOContext, started_at: float
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(self, io_context: IOContext, started_at: float) -> typing.AsyncContextManager[None]: ...

    handle_input_exception: __handle_input_exception_spec

    def exit_context(self, started_at, input_ids: typing.List[str]): ...

    class __push_outputs_spec(typing_extensions.Protocol):
        def __call__(self, io_context: IOContext, started_at: float, data: typing.Any, data_format: int) -> None: ...
        async def aio(self, io_context: IOContext, started_at: float, data: typing.Any, data_format: int) -> None: ...

    push_outputs: __push_outputs_spec

    class __memory_restore_spec(typing_extensions.Protocol):
        def __call__(self) -> None: ...
        async def aio(self) -> None: ...

    memory_restore: __memory_restore_spec

    class __memory_snapshot_spec(typing_extensions.Protocol):
        def __call__(self) -> None: ...
        async def aio(self) -> None: ...

    memory_snapshot: __memory_snapshot_spec

    class __volume_commit_spec(typing_extensions.Protocol):
        def __call__(self, volume_ids: typing.List[str]) -> None: ...
        async def aio(self, volume_ids: typing.List[str]) -> None: ...

    volume_commit: __volume_commit_spec

    class __interact_spec(typing_extensions.Protocol):
        def __call__(self, from_breakpoint: bool = False): ...
        async def aio(self, from_breakpoint: bool = False): ...

    interact: __interact_spec

    @property
    def target_concurrency(self) -> int: ...
    @property
    def max_concurrency(self) -> int: ...
    @classmethod
    def get_input_concurrency(cls) -> int: ...
    @classmethod
    def set_input_concurrency(cls, concurrency: int): ...
    @classmethod
    def stop_fetching_inputs(cls): ...

def check_fastapi_pydantic_compatibility(exc: ImportError) -> None: ...

MAX_OUTPUT_BATCH_SIZE: int

RTT_S: float
