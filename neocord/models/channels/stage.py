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
from typing import TYPE_CHECKING

from neocord.models.channels.base import GuildChannel
from neocord.internal.missing import MISSING

if TYPE_CHECKING:
    from neocord.models.base import DiscordModel

class StageChannel(GuildChannel):
    """
    Represents a guild stage channel.

    Attributes
    ----------
    bitrate: :class:`int`
        The bitrate of this stage channel.
    user_limit: :class:`int`
        The number of users that can connect to this channel at a time, 0 means that there
        is no explicit limit set.
    rtc_region: :class:`str`
        The voice region of this channel.
    topic: :class:`str`
        The topic of this stage channel.
    nsfw: :class:`bool`
        Whether this stage channel is NSFW or not.
    """
    __slots__ = ('bitrate', 'user_limit', 'rtc_region', 'topic', 'nsfw')

    if TYPE_CHECKING:
        def __init__(self, data: Any, guild: Guild):
            ...

    def _update(self, data: Any):
        super()._update(data)
        try:
            self.bitrate = int(data['bitrate'])
        except KeyError:
            self.bitrate = None

        self.user_limit = int(data.get('user_limit', 0))
        self.rtc_region = data.get('rtc_region')
        self.nsfw = data.get('nsfw', False)
        self.topic = data.get('topic')

    async def edit(self, *,
        name: Optional[str] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = MISSING,
        rtc_region: Optional[str] = None,
        nsfw: Optional[bool] = None,
        position: Optional[int] = None,
        category: Optional[DiscordModel] = MISSING,
        topic: Optional[str] = MISSING,
        reason: Optional[str] = None,
    ) -> None:
        """
        Edits the stage channel.

        Parameters
        ----------
        name: :class:`str`
            The new name of channel.
        bitrate: :class:`int`
            The new bitrate of channel.
        user_limit: :class:`int`
            New user limit of the channel or None to remove it.
        position: :class:`int`
            The new position of channel.
        rtc_region: :class:`str`
            The new voice region of channel.
        topic: :class:`str`
            The topic of the channel.
        category: :class:`CategoryChannel`
            The ID of category that this channel should be put in.
        nsfw: :class:`bool`
            Whether this channel is NSFW or not.
        reason: :class:`str`
            The reason for this edit that appears on Audit log.

        Raises
        ------
        Forbidden
            You are not allowed to edit this channel.
        HTTPError
            The editing of voice channel failed somehow.
        """
        payload = {}

        if name is not None:
            payload['name'] = name
        if nsfw is not None:
            payload['nsfw'] = nsfw
        if position is not None:
            payload['position'] = position
        if category is not MISSING:
            if category is None:
                payload['parent_id'] = None
            else:
                payload['parent_id'] = category.id

        if bitrate is not None:
            payload['bitrate'] = bitrate
        if user_limit is not MISSING:
            payload['user_limit'] = user_limit
        if rtc_region is not None:
            payload['rtc_region'] = rtc_region
        if topic is not MISSING:
            payload['topic'] = topic

        if payload:
            data = await self._state.http.edit_channel(
                channel_id=self.id,
                payload=payload,
                reason=reason,
            )
            self._update(data)

    @property
    def instance(self) -> Optional[StageInstance]:
        """
        Optional[:class:`StageInstance`]: Returns the live stage instance that is currently
        running in stage channel. Returns None if no instance is running.
        """
        for instance in self.guild.stage_instances:
            if instance.channel_id == self.id:
                return instance

    async def fetch_instance(self, id: int, /):
        """Fetches a stage instance that is associated with this stage channel.

        This is an API call. Consider using :attr:`instance` instead.

        Parameters
        ----------
        id: :class:`int`
            The ID of stage instance.

        Returns
        -------
        :class:`StageInstance`
            The fetched stage instance.

        Raises
        ------
        NotFound
            The stage instance was not found.
        HTTPError
            An error occured while fetching.
        """
        data = await self.http.get_stage_instance(channel_id=self.id)
        return StageInstance(data, state=self.state)