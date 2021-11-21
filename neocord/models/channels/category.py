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
from typing import Optional, TYPE_CHECKING, Any, List

from neocord.models.channels.base import GuildChannel

if TYPE_CHECKING:
    from neocord.models.guild import Guild


class CategoryChannel(GuildChannel):
    """
    Represents a category channel.

    A category channel can be used to organize other channels in a guild as such
    other channels can inherit the permissions and options for a category.


    """
    if TYPE_CHECKING:
        def __init__(self, data: Any, guild: Guild):
            ...

    @property
    def channels(self) -> List[GuildChannel]:
        """
        Returns the channels within this organizational category.

        Returns
        -------
        List[:class:`GuildChannel`]
        """
        return [c for c in self.guild.channels if c.category_id == self.id]

    async def edit(self, *,
        name: Optional[str] = None,
        position: Optional[int] = None,
        nsfw: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> None:
        """
        Edits the category channel.

        Parameters
        ----------
        name: :class:`str`
            The new name of channel.
        nsfw: :class:`bool`
            Whether the channel should be NSFW or not.
        position: :class:`int`
            The new position of channel.
        reason: :class:`str`
            The reason for this edit that appears on Audit log.

        Raises
        ------
        Forbidden
            You are not allowed to edit this channel.
        HTTPError
            The editing of category channel failed somehow.
        """
        payload = {}

        if name is not None:
            payload['name'] = name
        if position is not None:
            payload['position'] = position
        if nsfw is not None:
            payload['nsfw'] = nsfw

        await self._state.http.edit_channel(channel_id=self.id, payload=payload, reason=reason)