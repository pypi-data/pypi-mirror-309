import modal.secret
import modal_proto.api_pb2
import typing

class _CloudBucketMount:
    bucket_name: str
    bucket_endpoint_url: typing.Optional[str]
    key_prefix: typing.Optional[str]
    secret: typing.Optional[modal.secret._Secret]
    read_only: bool
    requester_pays: bool

    def __init__(
        self,
        bucket_name: str,
        bucket_endpoint_url: typing.Optional[str] = None,
        key_prefix: typing.Optional[str] = None,
        secret: typing.Optional[modal.secret._Secret] = None,
        read_only: bool = False,
        requester_pays: bool = False,
    ) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...

def cloud_bucket_mounts_to_proto(
    mounts: typing.List[typing.Tuple[str, _CloudBucketMount]],
) -> typing.List[modal_proto.api_pb2.CloudBucketMount]: ...

class CloudBucketMount:
    bucket_name: str
    bucket_endpoint_url: typing.Optional[str]
    key_prefix: typing.Optional[str]
    secret: typing.Optional[modal.secret.Secret]
    read_only: bool
    requester_pays: bool

    def __init__(
        self,
        bucket_name: str,
        bucket_endpoint_url: typing.Optional[str] = None,
        key_prefix: typing.Optional[str] = None,
        secret: typing.Optional[modal.secret.Secret] = None,
        read_only: bool = False,
        requester_pays: bool = False,
    ) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...
