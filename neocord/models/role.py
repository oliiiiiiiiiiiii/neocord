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

from neocord.models.base import DiscordModel
from neocord.models.asset import CDNAsset
from neocord.dataclasses.color import Color
from neocord.internal.missing import MISSING
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.typings.role import (
        Role as RolePayload,
        RoleTags as RoleTagsPayload
    )
    from neocord.models.guild import Guild
    from neocord.models.member import GuildMember


class RoleTags:
    """Represents the tags that are present on a role.

    Role tags contain information about the role's owner for example if a role is
    owned by an integration or if the role is a booster role.

    Attributes
    ----------
    bot_id: Optional[:class:`int`]
        The ID of the bot that owns this role. Could be None
    integration_id: Optional[:class:`int`]
        The ID of the integration that owns this role. Could be None
    """
    __slots__ = ('bot_id', 'integration_id', '_premium_subscriber')

    def __init__(self, data: RoleTagsPayload):
        self.bot_id = helpers.get_snowflake(data, 'bot_id')
        self.integration_id = helpers.get_snowflake(data, 'integration_id')

        # Discord API sends premium_subscriber field as null (None). If it is present
        # then it is True, if this is missing then it's False so we would
        # MISSING.
        # God bless Discord API.

        self._premium_subscriber = data.get('premium_subscriber', MISSING)

    @property
    def premium_subscriber(self) -> bool:
        """
        :class:`bool`: Whether this role is for premium subscribers aka server boosters.
        Premium subscriber roles cannot be assigned or removed manually nor can it be
        deleted or created manually.
        """
        if self._premium_subscriber is MISSING:
            return False

        return True

class Role(DiscordModel):
    """
    Represents a guild's role entity.

    A role can be used to modify a guild member's permissions, appearence
    and other characters or organize members.

    Attributes
    ----------
    id: :class:`int`
        The unique snowflake ID of the role.
    name: :class:`str`
        The name of the role.
    hoist: :class:`bool`
        Whether the role is shown seperate from online members and other roles.
    position: :class:`int`
        An integer representing the position of the role in role heirarchy.
    managed: :class:`bool`
        Whether the role is managed by an integration.
    mentionable: :class:`bool`
        Whether the role is mentioned by members.
    unicode_emoji: Optional[:class:`str`]
        The string representation of the unicode emoji as role icon if any. This would
        be None if there is no unicode emoji on role icon.
    color: :class:`Colour`
        The color of the role.
    tags: :class:`RoleTags`
        The tags present on the role.
    """
    __slots__ = (
        '_guild', '_state', 'id', 'name', 'hoist', 'position',
        'managed', 'mentionable', 'unicode_emoji', 'color', 'tags',
        '_icon'
    )

    def __init__(self, data: RolePayload, guild: Guild):
        self._guild = guild
        self._state = self._guild._state
        self._update(data)

    def _update(self, data: RolePayload):
        self.id = int(data['id'])
        self.name = data['name']
        self.hoist = data.get('hoist', False)
        self.position = int(data['position'])
        self.managed = data.get('managed', False)
        self.mentionable = data.get('mentionable', False)
        self.unicode_emoji = data.get('unicode_emoji')
        self.color = Color(data.get('color', 0))
        self.tags = RoleTags(data.get('tags', {})) # type: ignore

        self._icon = data.get('icon')

    @property
    def icon(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the asset that represents the icon of this role.
        Could be None if role has no icon set.
        """
        if self._icon:
            return CDNAsset(
                state=self._state,
                key=self._icon,
                path=f'/role-icons/{self.id}'
                )

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string used to mention the role in Discord."""
        return '<@&{0}>'.format(self.id)

    @property
    def members(self) -> List[GuildMember]:
        """
        List[:class:`GuildMember`]: Returns the list of members that have this role assigned.
        """
        return [member for member in self._guild.members if self in member.roles]


    async def edit(self, *,
        name: Optional[str] = None,
        hoist: Optional[bool] = None,
        position: Optional[int] = None,
        mentionable: Optional[bool] = None,
        unicode_emoji: Optional[str] = MISSING,
        color: Optional[Color] = MISSING,
        colour: Optional[Color] = MISSING,
        icon: Optional[bytes] = MISSING,
        reason: str = None,
    ):
        """Edits the role.

        You need :attr:`Permissions.manage_roles` in role's guild to edit the role.

        Parameters
        ----------
        name: :class:`str`
            The name of the role.
        hoist: :class:`bool`
            Whether the role is shown seperate from online members and other roles.
        position: :class:`int`
            An integer representing the position of the role in role heirarchy.
        managed: :class:`bool`
            Whether the role is managed by an integration.
        mentionable: :class:`bool`
            Whether the role is mentioned by members.
        unicode_emoji: Optional[:class:`str`]
            The string representation of the unicode emoji as role icon if any. This could
            be None to remove the icon.
        color: :class:`Colour`
            The color of the role.
        icon: :class:`bytes`
            The bytes-like object representing the new icon, None can be passed to
            remove the icon.
        reason: :class:`str`
            The reason for editing the role, Shows up on the audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to edit the role.
        HTTPError
            The editing of role failed somehow.
        """
        payload = {}
        if name is not None:
            payload['name'] = name
        if hoist is not None:
            payload['hoist'] = hoist
        if mentionable is not None:
            payload['mentionable'] = mentionable
        if unicode_emoji is not MISSING:
            payload['unicode_emoji'] = unicode_emoji
        if icon is not MISSING:
            if icon is None:
                payload['icon'] = icon
            else:
                payload['icon'] = helpers.get_image_data(icon)


        if color is not MISSING or colour is not MISSING:
            payload['color'] = helpers.get_either_or(color, colour, equ=MISSING).value

        if payload:
            data = await self._state.http.edit_role(
                guild_id=self._guild.id,
                role_id=self.id,
                reason=reason,
                payload=payload,
                )

        if position is not None:
            payload = {'position': position, 'id': self.id}
            roles = await self._state.http.edit_role_position(
                guild_id=self._guild.id,
                payload=payload,
                reason=reason,
                )

    async def delete(self, *, reason: Optional[str] = None):
        """Deletes the role.

        Parameters
        ----------
        reason: :class:`str`
            The reason for deleting the role; Shows up on audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to delete the role.
        HTTPError
            The deletion of role failed somehow.
        """
        await self._state.http.delete_role(
            guild_id=self._guild.id,
            role_id=self.id,
            reason=reason,
        )