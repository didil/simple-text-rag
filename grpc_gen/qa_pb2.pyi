from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateCollectionRequest(_message.Message):
    __slots__ = ("name", "file_url")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    name: str
    file_url: str
    def __init__(self, name: _Optional[str] = ..., file_url: _Optional[str] = ...) -> None: ...

class CreateCollectionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAnswerRequest(_message.Message):
    __slots__ = ("collection_name", "question")
    COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    collection_name: str
    question: str
    def __init__(self, collection_name: _Optional[str] = ..., question: _Optional[str] = ...) -> None: ...

class Answer(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
