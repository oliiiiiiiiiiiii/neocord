# MIT License

# Copyright (c) 2021 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations
from typing import Any, ClassVar, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp import ClientResponse

class HTTPError(Exception):
    """
    Base exception class for all the HTTPs related errors.

    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The HTTP request response.
    data: :class:`dict`
        The raw data. May be None in some cases.
    status: :class:`int`
        The HTTP error status code.
    """
    DEFAULT_ERROR_MESSAGE: ClassVar[str] = 'An HTTP error occured.'

    def __init__(self, response: ClientResponse, data:  Dict[str, Any]) -> None:
        self.response = response
        self.data = data

        super().__init__(data.get('message', self.DEFAULT_ERROR_MESSAGE))

class NotFound(HTTPError):
    """
    An error representing the 404 HTTP error or in other words an error that is
    raised when an entity is requested from Discord API that doesn't exist.

    This class inherits :exc:`HTTPException`.
    """
    DEFAULT_ERROR_MESSAGE = 'Requested resource could not be found.'


class Forbidden(HTTPError):
    """
    An error representing the 403 or 401 HTTP error or in other words an error that is
    raised when client is not allowed do a specific operation.

    This class inherits :exc:`HTTPException`.
    """
    DEFAULT_ERROR_MESSAGE = 'Requested resource cannot be accessed.'

class HTTPRequestFailed(HTTPError):
    """
    Raised when an HTTP request fails i.e returns with 500s status code.

    This class inherits :exc:`HTTPException`.
    """
    def __init__(self, response: ClientResponse) -> None:
        # a fake kind of response data
        super().__init__(response, {'message': 'HTTP request failed, Returned with status {}'.format(response.status)})