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
from neocord.models.asset import CDNAsset
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.models.guild import Guild
    from neocord.typings.emoji import Emoji as EmojiPayload

class Emoji(DiscordModel):
    """Represents a custom emoji in a guild.

    Attributes
    ----------
    id: :class:`int`
        The ID of this role.
    name: :class:`str`
        The name of this emoji.
    roles: List[:class:`Role`]
        The list of roles that can manage this emoji.
    user: :class:`User`
        The user that created this emoji.
    require_colons: :class:`bool`
        Whether this emoji requires to be wrapped in ":" (colons) to be used.
    managed: :class:`bool`
        Whether this emoji is managed by an integration like Twitch etc.
    available: :class:`bool`
        Whether this emoji is available for use. Could be False if the emoji became
        unavailable due to server losing boosts.
    animated: :class:`bool`
        Whether the emoji is animated or not.
    guild: :class:`Guild`
        The guild that this emoji belongs to.
    """
    __slots__ = (
        'guild', '_state', 'id', 'name', 'roles', 'role_ids', 'user',
        'require_colons', 'available', 'managed', 'animated',
    )

    def __init__(self, data: EmojiPayload, guild: Guild):
        self.guild = guild
        self._state = guild._state
        self._update(data)

    def _update(self, data: EmojiPayload):
        self.id = helpers.get_snowflake(data, 'id') # type: ignore
        self.name = data.get('name')

        self.roles = []
        self.role_ids = []

        for role_id in data.get('roles', []):
            role_id = int(role_id)
            role = self.guild.get_role(role_id)

            if role:
                self.roles.append(role)

            self.role_ids.append(role_id)

        user = data.get('user')
        if user:
            self.user = self._state.add_user(user)
        else:
            self.user = None

        self.require_colons = data.get('require_colons', True)
        self.available = data.get('available', True)
        self.managed = data.get('managed', False)
        self.animated = data.get('animated', False)

    @property
    def url(self) -> str:
        """:class:`str`: Returns the URL of the emoji."""
        return CDNAsset.BASE_CDN_URL + f'/emojis/{self.id}.{"gif" if self.animated else "png"}'

