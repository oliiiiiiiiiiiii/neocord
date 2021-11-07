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
import asyncio
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from neocord.api.state import State

    EventPayload = Dict[str, Any]

class Parsers:
    """
    Parsers for gateway events.
    """
    if TYPE_CHECKING:
        state: State

    def __init__(self, state: State) -> None:
        self.state = state

    @property
    def dispatch(self) -> Callable[[str], Any]:
        return self.state.client.dispatch

    def get_parser(self, event: str) -> Optional[Callable[[Dict[str, Any]], Any]]:
        try:
            parser = getattr(self, f'parse_{event.lower()}')
        except AttributeError:
            return
        else:
            return parser

    async def _schedule_ready(self, pending: List[Dict[str, Any]]):
        while pending:
            await asyncio.sleep(0.05)
            pending.pop(0)

        self.dispatch('ready')


    def parse_ready(self, event: EventPayload):
        self.dispatch('connect')
        guilds = event['guilds']

        asyncio.create_task(self._schedule_ready(guilds))