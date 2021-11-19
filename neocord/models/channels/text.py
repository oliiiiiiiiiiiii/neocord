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
from typing import Optional, TYPE_CHECKING, Any

from neocord.models.base import DiscordModel
from neocord.models.channels.base import ChannelType, GuildChannel
from neocord.models.message import Message
from neocord.internal import helpers
from neocord.internal.missing import MISSING
from neocord.abc import Messageable

if TYPE_CHECKING:
    from neocord.models.guild import Guild

class TextChannel(GuildChannel, Messageable):
    """
    Represents a text channel in a guild.

    Like all guild channels, This also inherits :class:`GuildChannel` so all operations
    valid there are valid here too.

    Attributes
    ----------
    last_message_id: :class:`int`
        The ID of last message.
    last_pin_timestamp: Optional[:class:`datetime.datetime`]
        The timestamp when last message pin was created.
    rate_limit_per_user: :class:`int`
        The ratelimit aka the slowmode in text channel. 0 means no ratelimit.
    topic: Optional[:class:`str`]
        The topic of channel.
    nsfw: :class:`bool`
        Whether this channel is marked as not safe for work (NSFW)
    """
    if TYPE_CHECKING:

        def __init__(self, data: Any, guild: Guild) -> None:
            ...

    def _update(self, data: Any):
        # super()._update will call GuildChannel._update()
        super()._update(data)

        # adding text channel specific attributes
        self.last_message_id = helpers.get_snowflake(data, 'last_message_id')
        self.last_pin_timestamp = helpers.iso_to_datetime(data.get('last_pin_timestamp'))

        self.rate_limit_per_user = int(data.get('rate_limit_per_user', 0))
        self.topic = data.get('topic')
        self.nsfw = data.get('nsfw', False)

    def is_news(self) -> bool:
        """
        Returns a boolean that indicates if the channel is a news aka announcement
        channel.
        """
        return self.type is ChannelType.NEWS

    async def fetch_message(self, id: int, /) -> Message:
        """
        Fetches a message from this channel.

        Parameters
        ----------
        id: :class:`int`
            The ID of the message.

        Returns
        -------
        :class:`Message`
            The requested message.

        Raises
        ------
        NotFound:
            Message was not found. i.e ID is incorrect.
        Forbidden:
            You are not allowed to fetch this message.
        HTTPError:
            The fetching failed somehow.
        """
        data = await self._state.http.get_message(channel_id=self.id, message_id=id)
        return Message(data, state=self._state)

    async def _get_messageable_channel(self) -> TextChannel:
        return self

    async def edit(self, *,
        name: Optional[str] = None,
        nsfw: Optional[bool] = None,
        position: Optional[int] = None,
        topic: Optional[str] = MISSING,
        rate_limit_per_user: Optional[int] = MISSING,
        default_auto_archive_duration: Optional[int] = MISSING,
        category: Optional[DiscordModel] = MISSING,
        reason: Optional[str] = None,
    ) -> None:
        """
        Edits the text channel.

        Parameters
        ----------
        name: :class:`str`
            The new name of channel.
        topic: :class:`str`
            The new topic of channel.
        nsfw: :class:`bool`
            Whether the channel should be NSFW or not.
        position: :class:`int`
            The new position of channel.
        rate_limit_per_user: :class:`int`
            The ratelimit per user aka channel message cooldown for a user.
        default_auto_archive_duration: :class:`int`
            The default thread auto-archiving durations of this channel.
        category: :class:`CategoryChannel`
            The ID of category that this channel should be put in.
        reason: :class:`str`
            The reason for this edit that appears on Audit log.

        Raises
        ------
        Forbidden:
            You are not allowed to edit this channel.
        HTTPError:
            The editing of text channel failed somehow.
        """
        payload = {}

        if name is not None:
            payload['name'] = name
        if topic is not MISSING:
            payload['topic'] = topic
        if nsfw is not None:
            payload['nsfw'] = nsfw
        if position is not None:
            payload['position'] = position
        if rate_limit_per_user is not MISSING:
            payload['rate_limit_per_user'] = rate_limit_per_user
        if default_auto_archive_duration is not MISSING:
            payload['default_auto_archive_duration'] = default_auto_archive_duration
        if category is not MISSING:
            payload['parent_id'] = category and category.id


        await self._state.http.edit_channel(
            channel_id=self.id,
            payload=payload,
            reason=reason,
        )
