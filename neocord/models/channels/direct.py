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

from neocord.models.base import DiscordModel
from neocord.abc import Messageable

if TYPE_CHECKING:
    from neocord.models.user import ClientUser

class DMChannel(Messageable, DiscordModel):
    """Represents a direct message channel with another user.

    Attributes
    ----------
    recipient: :class:`User`
        The user that this channel is with.
    me: :class:`ClientUser`
        The user representing the client.
    id: :class:`int`
        The ID of this channel.
    """
    __slots__ = ('_state', 'recipient', 'me', 'id')

    # TODO: DMChannelPayload
    def __init__(self, me: ClientUser, data: Any, state: State):
        self._state = state
        self.me = me
        self._update(data)

    async def _get_messageable_channel(self):
        return self

    def _update(self, data: Any):
        # recipients is always a list of single user.

        user = data['recipients'][0] # type: ignore

        self.recipient = self._state.add_user(user)
        self.id = int(data['id'])
