from urllib.request import urlopen, Request

from componenter.component import Component
from dev.examples.http_client.types import PostRequesterT, RequestT, ResponseT


class HttpClient(Component, components=[]):
    pass


class PostRequester(PostRequesterT[Request]):
    def post(self, request: RequestT) -> ResponseT:
        urlopen(request)
