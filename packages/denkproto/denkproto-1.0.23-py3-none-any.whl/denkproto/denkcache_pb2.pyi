from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectExistsRequest(_message.Message):
    __slots__ = ("container_name", "blob_name")
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    BLOB_NAME_FIELD_NUMBER: _ClassVar[int]
    container_name: str
    blob_name: str
    def __init__(self, container_name: _Optional[str] = ..., blob_name: _Optional[str] = ...) -> None: ...

class ObjectExistsResponse(_message.Message):
    __slots__ = ("exists",)
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    exists: bool
    def __init__(self, exists: bool = ...) -> None: ...

class GetObjectRequest(_message.Message):
    __slots__ = ("container_name", "blob_name")
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    BLOB_NAME_FIELD_NUMBER: _ClassVar[int]
    container_name: str
    blob_name: str
    def __init__(self, container_name: _Optional[str] = ..., blob_name: _Optional[str] = ...) -> None: ...

class GetObjectResponse(_message.Message):
    __slots__ = ("object",)
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    object: bytes
    def __init__(self, object: _Optional[bytes] = ...) -> None: ...

class GetCachedObjectRequest(_message.Message):
    __slots__ = ("container_name", "blob_name")
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    BLOB_NAME_FIELD_NUMBER: _ClassVar[int]
    container_name: str
    blob_name: str
    def __init__(self, container_name: _Optional[str] = ..., blob_name: _Optional[str] = ...) -> None: ...

class GetCachedObjectResponse(_message.Message):
    __slots__ = ("object",)
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    object: bytes
    def __init__(self, object: _Optional[bytes] = ...) -> None: ...

class HasObjectCachedRequest(_message.Message):
    __slots__ = ("container_name", "blob_name")
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    BLOB_NAME_FIELD_NUMBER: _ClassVar[int]
    container_name: str
    blob_name: str
    def __init__(self, container_name: _Optional[str] = ..., blob_name: _Optional[str] = ...) -> None: ...

class HasObjectCachedResponse(_message.Message):
    __slots__ = ("exists",)
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    exists: bool
    def __init__(self, exists: bool = ...) -> None: ...

class PingPongRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingPongResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
