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
from typing import Any, Dict

class HTTPError(Exception):
    """
    Base exception class for all the HTTPs related errors.

    Attributes
    ----------
    raw_response: :class:`dict`
        The raw response JSON.
    """
    def __init__(self, raw_response: Dict[str, Any]) -> None:
        self.raw_response = raw_response

        super().__init__(raw_response.get('message', 'An error occured.'))

class NotFound(HTTPError):
    """
    An error representing the 404 HTTP error or in other words an error that is
    raised when an entity is requested from Discord API that doesn't exist.

    This class inherits :exc:`HTTPException`.
    """
    pass

class Forbidden(HTTPError):
    """
    An error representing the 403 or 401 HTTP error or in other words an error that is
    raised when client is not allowed do a specific operation.

    This class inherits :exc:`HTTPException`.
    """
    pass

