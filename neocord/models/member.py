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
import asyncio
from neocord.models.asset import CDNAsset
from typing import Optional, List, Any, TYPE_CHECKING

from neocord.models.base import DiscordModel
from neocord.models.user import User
from neocord.models.role import Role
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.typings.member import Member as MemberPayload
    from neocord.typings.role import Role as RolePayload
    from neocord.models.guild import Guild
    from neocord.dataclasses.flags.user import UserFlags
    from neocord.dataclasses.color import Color
    from datetime import datetime

class GuildMember(DiscordModel):
    """
    Represents a guild member entity. A member is just a user inside a guild.

    Attributes
    ----------
    name: :class:`str`
        The username of user as shown in Discord. This is not the guild avatar, to get
        the guild nickname, use :attr:`.nickname`
    id: :class:`int`
        The user's unique snowflake ID.
    discriminator: :class:`str`
        The 4 digits discriminator of user.
    bot: :class:`bool`
        A boolean representing if the user is a bot or not, In case of this class
        this is usually ``True``
    joined_at: :class:`datetime.datetime`
        The time when member joined the guild.
    deaf: :class:`bool`
        Whether the member is deaf in voice channel.
    mute: :class:`bool`
        Whether the member is mute in voice channel.
    pending: :class:`bool`
        Whether the member has passed membership screening or not.
    """
    __slots__ = (
        'guild', '_state', '_roles', 'joined_at', 'deaf', 'mute', 'pending',
        '_user', '_nickname', '_premium_since', '_permissions', '_avatar', 'id',
        'name', 'bot', 'discriminator'
        )

    def __init__(self, data: MemberPayload, guild: Guild):
        self.guild = guild
        self._state = self.guild._state
        self._roles = {}
        self._update(data)


    def _update(self, data: MemberPayload):
        self.joined_at = helpers.iso_to_datetime(data.get('joined_at'))
        self.deaf = data.get('deaf', False)
        self.mute = data.get('mute', False)
        self.pending = data.get('pending', False)

        self._user = User(data.get('user'), state=self._state) # type: ignore
        self._nickname = data.get('nick')
        self._premium_since = data.get('premium_since')
        self._permissions = data.get('permissions')
        self._avatar = data.get('avatar')

        self.id = self._user.id
        self.name = self._user.name
        self.bot = self._user.bot
        self.discriminator = self._user.discriminator

        for role in data.get('roles', []):
            self._add_role(role)

    def _add_role(self, id: int):
        role = self.guild.get_role(int(id))
        # role shouldn't be None here
        self._roles[role.id] = role
        return role

    @property
    def premium_since(self) -> Optional[datetime]:
        """
        Returns :class:`datetime.datetime` of time when member started boosting the server.

        This is None if member is not boosting.
        """
        if self._premium_since:
            return helpers.iso_to_datetime(self._premium_since)

    @property
    def guild_avatar(self) -> Optional[CDNAsset]:
        """
        Returns the guild avatar of the user. If user has no avatar in the guild then
        :attr:`.avatar` (default avatar) is returned instead.
        """
        if self._avatar is None:
            return self.avatar

        return CDNAsset(
            key=self._avatar,
            state=self._state,
            path=f'guilds/{self.guild.id}/users/{self.id}/avatars'
        )

    @property
    def nickname(self) -> str:
        """
        Returns the guild nickname of the user. If user has specific nickname in the guild
        then :attr:`.name` (default username) is returned instead.
        """
        if self._nickname is None:
            return self.name

        return self._nickname

    # Below are shorthands from user object.

    @property
    def public_flags(self) -> UserFlags:
        """:class:`UserFlags: Returns the public flags of a user."""
        return self._user.public_flags

    @property
    def avatar(self) -> Optional[CDNAsset]:
        """
        :class:`CDNAsset`: Returns the CDN asset for user avatar.

        This returns user's actual avatar. To get the guild avatar,
        Use :attr:`.guild_avatar`
        """
        return self._user.avatar

    @property
    def banner(self) -> Optional[CDNAsset]:
        """:class:`CDNAsset`: Returns the CDN asset for user banner."""
        return self._user.banner

    @property
    def accent_color(self) -> Color:
        """:class:`Color`: Returns the color representation of the user's banner color."""
        return self._user.accent_color

    # alias
    accent_colour = accent_color

    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string used to mention the user in Discord."""
        return self._user.mention


    @property
    def roles(self) -> List[Role]:
        """
        Returns the list of roles that are attached on this member.
        """
        return list(self._roles.values())


    def get_role(self, id: int, /) -> Optional[Role]:
        """
        Gets a role from the member. This method returns None is the role with ID
        is not found.

        Parameters
        ----------
        id: :class:`int`
            The ID of the role.

        Returns
        -------
        :class:`Role`
            The requested role.
        """
        return self._roles.get(id)

    async def edit(self, **kwargs: Any):
        """
        Edits the member.

        Parameters
        ----------
        nick: :class:`str`
            The new nickname of member.
        roles: List[:class:`DiscordModel`]
            List of roles (or :class:`ModelMimic`) that should be assigned to member.
        mute: :class:`bool`
            Whether to mute the member in voice channel. Requires member to be in voice
            channel.
        deaf: :class:`bool`
            Whether to deafen the member in voice channel. Requires member to be in voice
            channel.
        voice_channel: :class:`DiscordModel`
            The voice channel to move the member to. Requires member to be in voice
            channel.
        reason: :class:`str`
            The reason for this action that shows up on audit log.

        """
        await self.guild.edit_member(self, **kwargs)

    async def kick(self, **kwargs: Any):
        """
        Kicks the member.

        Parameters
        ----------
        reason: :class:`str`
            The reason for this action that shows up on audit log.
        """
        await self.guild.kick_member(self, **kwargs)

    def __repr__(self):
        return (
            f'<GuildMember id={self.id} name={self.name}' \
            f'discriminator={self.discriminator} bot={self.bot}>'
        )

    def __str__(self):
        return f'{self.name}#{self.discriminator}'