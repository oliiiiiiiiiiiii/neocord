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
from neocord.api.routes import guild
from typing import TYPE_CHECKING, Optional

from neocord.models.base import DiscordModel
from neocord.models.member import GuildMember
from neocord.models.user import User
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.models.guild import Guild
    from neocord.typings.message import Message as MessagePayload

class Message(DiscordModel):
    """Represents a discord message entity.

    Attributes
    ----------
    id: :class:`int`
        The snowflake ID of this message.
    channel_id: :class:`int`
        The ID of channel in which the message was sent.
    guild_id: :class:`int`
        The ID of guild in which message was sent.
    content: :class:`str`
        The content of message, this may be None if message has no content.
    created_at: :class:`datetime.datetime`
        The datetime representation of the time when message was sent.
    tts: :class:`bool`
        Whether message is a "text-to-speech" message.
    mention_everyone: :class:`bool`
        Whether this message involves the @everyone or @here mention.
    pinned: :class:`bool`
        Whether the message is pinned in the parent channel.
    type: :class:`MessageType`
        The type of message.
    webhook_id: :class:`int`
        If a webhook has sent this message, then this is the ID of that webhook.
    author: Union[:class:`GuildMember`, :class:`User`]
        The user that sent this message, this could be None. If the message was sent
        in a DM, Then it is :class:`User`, otherwise, it's a :class:`GuildMember`
    """
    __slots__ = (
        'id', 'channel_id', 'guild_id', 'content', 'created_at', '_edited_timestamp',
        'tts', 'mention_everyone', 'pinned', 'type', 'webhook_id', 'author', '_state'
    )

    def __init__(self, data: MessagePayload, state: State) -> None:
        self._state = state
        self.channel_id = helpers.get_snowflake(data, 'channel_id')
        self.webhook_id = helpers.get_snowflake(data, 'webhook_id')
        self.id = int(data['id'])
        self.guild_id = helpers.get_snowflake(data, 'guild_id')
        self.created_at = helpers.iso_to_datetime(data.get('timestamp'))
        self.tts = data.get('tts', False)
        self.type = data.get('type')
        self.author = None # type: ignore

        author = data.get('author')

        if self.webhook_id is None:
            if self.guild:
                # since the member is most likely to be partial here, we try to
                # obtain member from our cache and in case we fail, we will
                # resolve it to user.
                self.author = self.guild.get_member(int(author['id']))

            if self.author is None:
                self.author = User(author, state=self.state)

        self._update(data)

    def _update(self, data: MessagePayload):
        # this only has the fields that are subject to change after
        # initial create.
        self.content = data.get('content')

        self._edited_timestamp = data.get('edited_timestamp')
        self.pinned = data.get('pinned', False)
        self.mention_everyone = data.get('mention_everyone', False)

    @property
    def guild(self) -> Optional[Guild]:
        """
        :class:`Guild`: Returns the guild in which message was sent. Could be None
        if message was sent in a DM channel.
        """
        return self._state.get_guild(self.guild_id) # type: ignore