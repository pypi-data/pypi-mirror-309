# -*- coding: utf-8 -*-

from abc import abstractmethod
from http import HTTPMethod

from urllib3 import Retry
from urllib3.response import HTTPResponse


class Requester:
    """ Base class for all type of HTTP requesters """

    @classmethod
    @abstractmethod
    def make_request(
            cls, method: HTTPMethod, url: str, headers=None, fields=None, timeout: float = 10,
            retries: Retry = False, **kwargs) -> HTTPResponse:

        """ Makes the request and returns the response """
