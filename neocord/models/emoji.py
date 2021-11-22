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
from typing import Any, TYPE_CHECKING, Optional, List

from neocord.models.base import DiscordModel
from neocord.models.asset import CDNAsset
from neocord.internal import helpers
from neocord.internal.missing import MISSING

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
        return  f'{CDNAsset.BASE_CDN_URL}/emojis/{self.id}.{"gif" if self.animated else "png"}'

    @property
    def mention(self) -> str:
        """
        :class:`str`: Returns a string representation that is used to use an emoji in Discord.
        """
        return f'<{"a" if self.animated else ""}:{self.name}:{self.id}>'

    async def edit(self,
        *,
        name: Optional[str] = None,
        roles: Optional[List[DiscordModel]] = MISSING,
        reason: Optional[str] = None,
        ):
        """
        Edits the custom guild emoji.

        You must have :attr:`~Permissions.manage_emojis` to perform this
        action in the guild.

        Parameters
        ----------
        name: :class:`str`
            The new name of emoji.
        roles: List[:class:`Role`]
            The list of roles that can use this emoji. None to disable the explicit
            restriction.
        reason: :class:`str`
            Reason for editing this emoji that shows up on guild's audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to edit an emoji.
        HTTPError
            Editing of emoji failed.
        """
        payload = {}

        if name is not None:
            payload['name'] = name
        if roles is not MISSING:
            if roles is None:
                payload['roles'] = []
            else:
                payload['roles'] = [r.id for r in roles]

        data = await self._state.http.edit_guild_emoji(
            guild_id=self.id,
            emoji_id=self.id,
            payload=payload,
            reason=reason,
            )
        if data:
            self._update(data)

    async def delete(self, *, reason: Optional[str] = None):
        """
        Deletes the custom emoji from the guild.

        Parameters
        ----------
        reason: :class:`str`
            The reason to delete that shows up on audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to delete this emoji.
        NotFound:
            Emoji not found.
        HTTPError
            Deleting of emoji failed.
        """
        await self._state.http.delete_guild_emoji(
            guild_id=self.guild.id,
            emoji_id=self.id,
            reason=reason
        )