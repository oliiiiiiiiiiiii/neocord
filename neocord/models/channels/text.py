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
from typing import TYPE_CHECKING, Any

from neocord.models.channels.base import GuildChannel
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.models.guild import Guild

class TextChannel(GuildChannel):
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

        def __init__(self, data: Any, guild: Guild):
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