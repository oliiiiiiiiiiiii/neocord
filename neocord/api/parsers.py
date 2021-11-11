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
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from neocord.models.user import ClientUser
from neocord.internal.logger import logger

import asyncio
import copy

if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.typings.user import User as UserPayload
    from neocord.typings.guild import Guild as GuildPayload
    from neocord.typings.member import Member as MemberPayload
    from neocord.typings.role import Role as RolePayload
    from neocord.typings.message import Message as MessagePayload

    EventPayload = Dict[str, Any]

class Parsers:
    """
    Parsers for gateway events.
    """
    if TYPE_CHECKING:
        state: State

    def __init__(self, state: State) -> None:
        self.state = state
        self._awaiting_guild_create = None

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

    async def _schedule_ready(self):
        logger.info('Preparing to dispatch ready.')

        if self._awaiting_guild_create is None:
            # avoid RuntimeError of future being attached to a different loop
            # in asyncio.wait_for()
            self._awaiting_guild_create = asyncio.Event()

        while True:
            self._awaiting_guild_create.clear()
            try:
                await asyncio.wait_for(self._awaiting_guild_create.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                break

        self._awaiting_guild_create.set()
        self.state.client._ready.set()

        self.dispatch('ready')

    def parse_ready(self, event: EventPayload):
        self.dispatch('connect')
        guilds = event['guilds']
        self.state.user = ClientUser(event['user'], state=self.state)
        self.state.add_user(event['user'])
        asyncio.create_task(self._schedule_ready())

    def parse_user_update(self, event: UserPayload):
        user = self.state.get_user(int(event['id']))

        if user is None:
            logger.debug(f'USER_UPDATE was sent with an unknown user {event["id"]}, Adding to cache without dispatching.')
            self.state.add_user(event)
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

        if self._awaiting_guild_create is None:
            return

        if not self._awaiting_guild_create.is_set():
            self._awaiting_guild_create.set()


    def parse_guild_update(self, event: GuildPayload):
        guild = self.state.get_guild(int(event['id']))
        if guild is None:
            # the guild object is not complete (as compared to GUILD_CREATE) here so
            # we cannot add it to internal cache.
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

    def parse_guild_member_add(self, event: MemberPayload):
        # guild_id is an extra field here.
        guild = self.state.get_guild(int(event['guild_id'])) # type: ignore

        if guild is None:
            logger.debug(f'GUILD_MEMBER_ADD was sent with an unknown guild {event["guild_id"]}, Discarding.') # type: ignore
            return

        member = guild._add_member(event)
        self.dispatch('member_join', member)

    def parse_guild_member_remove(self, event: dict):
        guild = self.state.get_guild(int(event['guild_id']))

        if guild is None:
            logger.debug(f'GUILD_MEMBER_REMOVE was sent with an unknown guild {event["guild_id"]}, Discarding.') # type: ignore
            return

        user = event["user"]
        member = guild._remove_member(int(user["id"]))
        self.dispatch('member_leave', member)

    def parse_guild_member_update(self, event: MemberPayload):
        # guild_id is an extra field here.
        guild = self.state.get_guild(int(event['guild_id'])) # type: ignore

        if guild is None:
            logger.debug(f'GUILD_MEMBER_UPDATE was sent with an unknown guild {event["guild_id"]}, Discarding.') # type: ignore
            return

        # user is always present here.
        member = guild.get_member(int(event["user"]["id"])) # type: ignore
        if member is None:
            logger.debug(f'GUILD_MEMBER_UPDATE was sent with an unknown member {event["user"]["id"]}, Adding to cache without dispatching.') # type: ignore
            guild._add_member(event)
            return

        before = copy.copy(member)
        member._update(event)

        # after = member
        self.dispatch('member_update', before, member)


    def parse_guild_role_create(self, event: RolePayload):
        # guild_id is an extra field here.
        guild = self.state.get_guild(int(event['guild_id'])) # type: ignore

        if guild is None:
            logger.debug(f'GUILD_ROLE_CREATE was sent with an unknown guild {event["guild_id"]}, Discarding.') # type: ignore
            return

        role = guild._add_role(event)
        self.dispatch('role_create', role)

    def parse_guild_role_delete(self, event: dict):
        guild = self.state.get_guild(int(event['guild_id']))

        if guild is None:
            logger.debug(f'GUILD_ROLE_DELETE was sent with an unknown guild {event["guild_id"]}, Discarding.') # type: ignore
            return

        role = guild.get_role(int(event["role_id"]))
        self.dispatch('role_delete', role)

    def parse_guild_role_update(self, event: RolePayload):
        # guild_id is an extra field here.
        guild = self.state.get_guild(int(event['guild_id'])) # type: ignore

        if guild is None:
            logger.debug(f'GUILD_ROLE_UPDATE was sent with an unknown guild {event["guild_id"]}, Discarding.') # type: ignore
            return

        data = event["role"] # type: ignore

        role = guild.get_role(int(data["id"]))
        if role is None:
            logger.debug(f'GUILD_ROLE_UPDATE was sent with an unknown role {event["role"]["id"]}, Adding to cache without dispatching.') # type: ignore
            guild._add_role(data)
            return

        before = copy.copy(role)
        role._update(data)

        # after = role
        self.dispatch('role_update', before, role)

    def parse_message_create(self, event: MessagePayload):
        message = self.state.add_message(event)
        self.dispatch('message', message)