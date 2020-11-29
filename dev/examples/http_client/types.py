import abc
from typing import Protocol, TypeVar, Generic

ParsedT = TypeVar("ParsedT")
RequestInputT = TypeVar("RequestInputT")
RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class ClientT:
    config: dict


class PostRequesterT(Generic[RequestT, ResponseT]):
    @abc.abstractmethod
    def post(self, request: RequestT) -> ResponseT:
        ...


class GetRequesterT(Generic[RequestT, ResponseT]):
    @abc.abstractmethod
    def get(self, request: RequestT) -> ResponseT:
        ...


class ResponseParserT(Generic[ResponseT, ParsedT]):
    @abc.abstractmethod
    def parse(self, response: ResponseT) -> ParsedT:
        ...


class RequestBuilder(Generic[RequestT, RequestInputT]):
    @abc.abstractmethod
    def create_request(self, request_input: RequestInputT) -> RequestT:
        ...
