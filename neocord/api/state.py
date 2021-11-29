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
from typing import Any, Dict, Optional, TYPE_CHECKING

from neocord.internal.mixins import ClientPropertyMixin
from neocord.internal.logger import logger
from neocord.api.parsers import Parsers
from neocord.models.user import User
from neocord.models.guild import Guild
from neocord.models.message import Message
from neocord.models.channels.direct import DMChannel
import asyncio

if TYPE_CHECKING:
    from neocord.core import Client
    from neocord.models.user import ClientUser
    from neocord.typings.user import User as UserPayload
    from neocord.typings.guild import Guild as GuildPayload
    from neocord.typings.message import Message as MessagePayload

class State(ClientPropertyMixin):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.parsers = Parsers(state=self)
        self.user: Optional[ClientUser] = None

        self.clear()

    def clear(self):
        self.guilds: Dict[int, Guild] = {}
        self.users: Dict[int, User] = {}
        self.messages: Dict[int, Message] = {}
        self.dm_channels: Dict[int, DMChannel] = {}
        self.dm_channels_by_recipient: Dict[int, DMChannel] = {}

    def parse_event(self, event: str, data: Any):
        if self.client.debug_events:
            self.client.dispatch('socket_dispatch', event, data)

        parser = self.parsers.get_parser(event)
        if parser is None:
            logger.debug(f'Unknown event {event}, Discarding.')
            return

        return parser(data)

    def get_user(self, id: int, /):
        return self.users.get(id)

    def add_user(self, data: UserPayload):
        user = User(data, state=self)
        self.users[user.id] = user
        return user

    def pop_user(self, id: int, /):
        return self.users.pop(id, None)

    def create_guild(self, data: GuildPayload):
        return Guild(data, state=self)

    def get_guild(self, id: int, /):
        return self.guilds.get(id)

    def add_guild(self, data: GuildPayload):
        guild = Guild(data, state=self)
        self.guilds[guild.id] = guild
        return guild

    def pop_guild(self, id: int, /):
        return self.guilds.pop(id, None)

    def get_message(self, id: int, /):
        return self.messages.get(id)

    def add_message(self, data: MessagePayload, /):
        # clear our cache if the message limit has reached or gone
        # beyond the caching limits.
        if len(self.messages.keys()) >= self.client.message_cache_limit:
            self.messages = {}

        message = Message(data, state=self)
        self.messages[message.id] = message
        return message

    def pop_message(self, id: int, /):
        return self.messages.pop(id, None)

    def add_dm_channel(self, data):
        channel = DMChannel(me=self.user, data=data, state=self) # type: ignore
        self.dm_channels[channel.id] = channel
        try:
            self.dm_channels_by_recipient[channel.recipient.id] = channel
        except AttributeError:
            pass

        return channel

    def remove_dm_channel(self, channel: DMChannel):
        try:
            self.dm_channels_by_recipient.pop(channel.recipient.id, None)
        except (KeyError, AttributeError):
            pass

        return self.dm_channels.pop(channel.id, None)

    def get_dm_channel_by_recipient(self, id: int) -> Optional[DMChannel]:
        return self.dm_channels_by_recipient.get(id)

    def get_dm_channel(self, id: int) -> Optional[DMChannel]:
        return self.dm_channels.get(id)
