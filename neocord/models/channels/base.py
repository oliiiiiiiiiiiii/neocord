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
from typing import TYPE_CHECKING, Any, Optional

from neocord.internal import helpers
from neocord.models.base import DiscordModel
from neocord.models.role import Role
from neocord.models.member import GuildMember
from neocord.models.user import User
from neocord.dataclasses.permissions import PermissionOverwrite

if TYPE_CHECKING:
    from neocord.models.guild import Guild
    from neocord.models.channels.category import CategoryChannel

class ChannelType:
    TEXT = 0
    DM = 1
    VOICE = 2
    GROUP = 3
    CATEGORY = 4
    NEWS = 5
    STORE = 6
    NEWS_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    STAGE = 13

class ChannelOverwriteType:
    ROLE = 0
    MEMBER = 1

class GuildChannel(DiscordModel):
    """
    Base class that implements basic operations for all channels types in a guild.

    Currently, the classes that inherit this are:

    - :class:`TextChannel`
    - :class:`VoiceChannel`
    - :class:`StageChannel`
    - :class:`CategoryChannel`
    - :class:`StoreChannel`

    Private channels like :class:`DMChannel` do not inherit this class.

    Attributes
    ----------
    id: :class:`int`
        The snowflake ID of the channel.
    guild: :class:`Guild`
        The guild that this channel belongs to.
    category_id: :class:`int`
        The ID of parent category that this channel exists in.
    type: :class:`int`
        The :class:`ChannelType` of channel
    position: :class:`int`
        The position of channel on the channels list.
    name: :class:`str`
        The name of channel.
    """
    __slots__ = (
        'guild', '_state', 'id', 'guild_id', 'category_id', 'type',
        'position', 'name', '_permission_overwrites', 'permissions'
        )
    # TODO: Add GuildChannelPayload
    def __init__(self, data: Any, guild: Guild):
        self.guild = guild
        self._state = self.guild._state
        self._update(data)

    def _update(self, data: Any):
        self.id = helpers.get_snowflake(data, 'id') # type: ignore
        self.guild_id = helpers.get_snowflake(data, 'guild_id') or self.guild.id
        self.category_id = helpers.get_snowflake(data, 'parent_id')

        self.type = int(data['type'])
        self.position = int(data.get('position', 0))
        self.name = data.get('name')

        # { (ENTITY_ID, ENTITY_TYPE): OVERWRITE }
        self._permission_overwrites: Dict[Tuple[int, int], Permission] = {}
        self.permissions = helpers.get_permissions(data)
        self._unroll_overwrites(data)

    def _unroll_overwrites(self, data):
        overwrites = data.get('permission_overwrites', [])

        for overwrite in overwrites:
            entity_id = int(overwrite['id'])
            allow = helpers.get_permissions(overwrite, key='allow')
            deny = helpers.get_permissions(overwrite, key='deny')

            self._permission_overwrites[(entity_id, overwrite['type'])] = PermissionOverwrite.from_pair(allow, deny)

    @property
    def category(self) -> Optional[CategoryChannel]:
        """
        Optional[:class:`CategoryChannel`]: Returns the category of this channel. None if
        channel has no parent category.
        """
        return self.guild.get_channel(self.category_id) # type: ignore


    def get_permission_overwrite_for(self, entity: Union[Role, GuildMember]) -> Optional[PermissionOverwrite]:
        """Returns a permission overwrite for requested entity.

        The entity can either be a :class:`Role` or a :class:`GuildMember`. If no
        overwrite is found for provided entity, None is returned.

        Parameters
        ----------
        entity: Union[:class:`Role`, :class:`GuildMember`]
            The entity to get overwrite for. Either a role or member.

        Returns
        -------
        Optional[:class:`PermissionOverwrite`]
            The permission overwrite for relevant entity.
        """
        if isinstance(entity, Role):
            entity_type = ChannelOverwriteType.ROLE
        elif isinstance(entity, (GuildMember, User)):
            entity_type = ChannelOverwriteType.MEMBER

        try:
            return self._permission_overwrites[(entity.id, entity_type)]
        except KeyError:
            return None

    async def edit(self, **kw: Any) -> None:
        raise NotImplementedError

    async def delete(self, *, reason: Optional[str] = None):
        """
        Deletes the channel.

        Parameters
        ----------
        reason: :class:`str`
            The reason for this action.

        Raises
        ------
        Forbidden
            You are not allowed to delete this channel.
        HTTPError
            The deletion failed somehow.
        """
        await self._state.http.delete_channel(channel_id=self.id, reason=reason)
