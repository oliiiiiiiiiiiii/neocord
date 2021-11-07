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
from neocord.typings.guild import Guild
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from neocord.models.user import ClientUser
from neocord.internal.logger import logger

import asyncio
import copy

if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.typings.user import User as UserPayload
    from neocord.typings.guild import Guild as GuildPayload

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
    def dispatch(self) -> Callable[..., Any]:
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

        self.state.client._ready.set()
        self.dispatch('ready')


    def parse_ready(self, event: EventPayload):
        self.dispatch('connect')
        guilds = event['guilds']
        self.state.user = ClientUser(event['user'], state=self.state)
        self.state.add_user(event['user'])

        asyncio.create_task(self._schedule_ready(guilds))

    def parse_user_update(self, event: UserPayload):
        user = self.state.get_user(int(event['id']))

        if user is None:
            logger.debug(f'USER_UPDATE was sent with an unknown user {event["id"]}, Discarding.')
            return

        before = copy.copy(user)
        user._update(event)

        # user: after
        self.dispatch('user_update', before, user)

    def parse_guild_create(self, event: GuildPayload):
        guild = self.state.add_guild(event)
        if self.state.client.is_ready():
            # we assume that guild is joined since client is ready.
            self.dispatch('guild_join', guild)

        self.dispatch('guild_create', guild)

    def parse_guild_update(self, event: GuildPayload):
        guild = self.state.get_guild(int(event['id']))
        if guild is None:
            logger.debug(f'GUILD_UPDATE was sent with an unknown guild {event["id"]}, Discarding.')
            return


        before = copy.copy(guild)
        guild._update(event)

        # guild: after
        self.dispatch('guild_update', before, guild)

    def parse_guild_delete(self, event: GuildPayload):
        guild = self.state.get_guild(int(event['id']))
        if guild is None:
            logger.debug(f'GUILD_UPDATE was sent with an unknown guild {event["id"]}, Discarding.')
            return

        if not 'available' in event:
            # the user was removed from guild.
            self.dispatch('guild_leave', guild)
        else:
            self.dispatch('guild_available', guild)

        self.state.pop_guild(guild.id)
        self.dispatch('guild_delete', guild)
