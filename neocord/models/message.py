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
from neocord.models.channels.base import GuildChannel
from typing import TYPE_CHECKING, Optional, Any

from neocord.models.base import DiscordModel
from neocord.dataclasses.embeds import Embed

from neocord.internal import helpers


if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.models.user import User
    from neocord.models.guild import Guild
    from neocord.typings.message import Message as MessagePayload
    from neocord.typings.member import Member as MemberPayload

class MessageInteraction(DiscordModel):
    """
    Represents the interaction's information attached to an interaction response's message.

    Attributes
    ----------
    id: :class:`int`
        The ID of interaction.
    name: :class:`str`
        The name of application command, If applicable.
    user: :class:`User`
        The user that invoked this interaction.
    application_id: :class:`int`
        The application's ID this interaction belongs to.
    """
    __slots__ = ('id', 'name', 'user', 'type', 'application_id')

    if TYPE_CHECKING:
        name: str
        user: User
        application_id: int
        type: int

    def __init__(self, data: Any, application_id: int) -> None:
        self.id = helpers.get_snowflake(data, 'id') # type: ignore
        self.name = data.get('name')

        if data.get('user'):
            user = data['user']
            self.user = self.state.get_user(int(user['id'])) or self.state.add_user(user)

        self.type = int(data.get('type', 1))
        self.application_id = application_id

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
    interaction: :class:`MessageInteraction`
        The interaction information if this message is an interaction response.
    embeds: List[:class:`Embed`]
        The list of embeds on this message.
    application_id: :class:`int`
        If message is an interaction, The application ID of the interaction.
    role_mentions: List[:class:`Role`]
        The list of roles that are mentioned in message.
    raw_role_mentions: List[:class:`int`]
        The list of role IDs that are mentioned in message.
    mentions: [:class:`User`, :class:`GuildMember`]
        The mentions that are done in the message.
    """
    __slots__ = (
        'id', 'channel_id', 'guild_id', 'content', 'created_at', '_edited_timestamp',
        'tts', 'mention_everyone', 'pinned', 'type', 'webhook_id', 'author', '_state',
        'mentions', 'role_mentions', 'raw_role_mentions', 'embeds', 'interaction', 'application_id'
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
        self.application_id = helpers.get_snowflake(data, 'application_id')
        author = data.get('author')

        if self.webhook_id is None:
            if self.guild:
                # since the member is most likely to be partial here, we try to
                # obtain member from our cache (which is complete) and in case we fail, we will
                # resolve it to user.
                self.author = self.guild.get_member(int(author['id']))

            else:
                self.author = self._state.get_user(int(author['id'])) or self._state.add_user(author)

        self.interaction = None
        inter = data.get('interaction')
        if inter:
            self.interaction = MessageInteraction(data['interaction'], application_id=self.application_id) # type: ignore

        self._update(data)

    def _update(self, data: MessagePayload):
        # this only has the fields that are subject to change after
        # initial create.
        self.content = data.get('content')

        self._edited_timestamp = data.get('edited_timestamp')
        self.pinned = data.get('pinned', False)
        self.mention_everyone = data.get('mention_everyone', False)

        self.mentions = []
        mentions = data.get('mentions', [])

        for mention in mentions:
            if 'member' in mention:
                try:
                    member_data: MemberPayload = {**mention['member'], 'user': mention} # type: ignore
                    member = self.guild.get_member(int(mention['id'])) or self.guild._add_member(member_data)
                except:
                    member = None
                else:
                    self.mentions.append(member)
            else:
                user = self.state.get_user(int(mention['id'])) or self.state.add_user(mention)
                self.mentions.append(user)

        self.role_mentions = []
        self.raw_role_mentions = []

        for role in data.get('mention_roles', []):
            # guild should not be None here
            role = self.guild.get_role(int(role)) # type: ignore
            if role:
                self.role_mentions.append(role)

            self.raw_role_mentions.append(int(role)) # type: ignore


        self.embeds = [Embed.from_dict(e) for e in data.get('embeds', [])]

    @property
    def guild(self) -> Optional[Guild]:
        """
        :class:`Guild`: Returns the guild in which message was sent. Could be None
        if message was sent in a DM channel.
        """
        return self._state.get_guild(self.guild_id) # type: ignore

    @property
    def channel(self) -> Optional[GuildChannel]:
        """
        :class:`GuildChannel`: Returns the channel in which message was sent.
        """
        if self.guild:
            return self.guild.get_channel(self.channel_id) # type: ignore

    def is_interaction_response(self):
        """
        Returns a boolean showing whether this message is an interaction i.e application
        command or message component's response.
        """
        return (self.application_id is not None)

    # TODO: Add API methods when guild channels are implemented.