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

from neocord.models.base import DiscordModel
from neocord.api.state import State
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.typings.message import Message as MessagePayload

class Message(DiscordModel):
    """Represents a discord message entity.

    Attributes
    ----------
    id: :class:`int`
        The snowflake ID of this message.
    """
    def __init__(self, data: MessagePayload, state: State) -> None:
        self._update(data)

    def _update(self, data: MessagePayload):
        self.id = int(data['id'])
        self.channel_id = helpers.get_snowflake(data, 'channel_id')
        self.guild_id = helpers.get_snowflake(data, 'guild_id')
        self.content = data.get('content')

        self.timestamp = helpers.iso_to_datetime(data.get('timestamp'))
        self._edited_timestamp = data.get('edited_timestamp')

        self.tts = data.get('tts', False)
        self.mention_everyone = data.get('mention_everyone', False)
        self.pinned = data.get('pinned', False)

        self.type = data.get('type')