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
from typing import Optional, List, TYPE_CHECKING

from neocord.internal.missing import MISSING
from neocord.internal import helpers
from neocord.models.message import Message
from neocord.models.base import DiscordModel

if TYPE_CHECKING:
    from neocord.dataclasses.embeds import Embed
    from neocord.api.state import State

class Messageable:
    if TYPE_CHECKING:
        _state: State

    async def _get_messageable_channel(self) -> DiscordModel:
        raise NotImplementedError

    async def send(self,
        content: Optional[str] = None,
        *,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
    ) -> Message:
        """
        Sends a message to the destination.

        Parameters
        ----------
        content: :class:`str`
            The content of message.
        embed: :class:`Embed`
            The embed shown in message. This parameter cannot be mixed with ``embeds``
        embeds: List[:class:`Embed`]
            The list of embeds shown in message. This parameter cannot be mixed with ``embed``

        Returns
        -------
        :class:`Message`
            The message that was sent.

        Raises
        ------
        Forbidden:
            You are not allowed to send message at this destination.
        HTTPError:
            The message sending failed somehow.
        """
        channel = await self._get_messageable_channel()
        payload = helpers.parse_message_create_payload(
            content=content,
            embed=embed,
            embeds=embeds,
        )
        data = await self._state.http.create_message(
            channel_id=channel.id,
            payload=payload,
            )
        return Message(data, state=self._state)