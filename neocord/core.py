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
from typing import Any, TYPE_CHECKING

import asyncio

class Client:
    """
    Represents a client that interacts with the Discord API. This is the starter
    point of any bot and core class for creating discord bots.

    This class takes no required parameters in initalization however a number
    of parameters can be passed in the initalization to modify the behaviour of
    class as needed. All parameters are optional and keyword-only.

    Parameters
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The asyncio event loop to use. if not provided, it will be obtained by calling
        :func:`asyncio.get_event_loop` function.
    """
    if TYPE_CHECKING:
        loop: asyncio.AbstractEventLoop

    def __init__(self, **params: Any) -> None:
        self.loop = params.get('loop') or asyncio.get_event_loop()

        self._ready = asyncio.Event()

    def is_ready(self) -> bool:
        """
        Returns a boolean representation of whether the client is in ready state,
        as such client has connected to Discord and has successfully filled
        the internal cache.

        Returns
        -------
        :class:`bool`
            Whether the client is ready or not.
        """
        return self._ready.is_set()

    async def wait_until_ready(self) -> None:
        """
        A coroutine that waits until the client is in ready state. The client is
        considered in ready state when it has connected to Discord websocket and has
        successfully filled the internal cache.
        """
        await self._ready.wait()
