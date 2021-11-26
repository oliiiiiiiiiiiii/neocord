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
from typing import TYPE_CHECKING, Optional

from neocord.models.base import DiscordModel
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.typings.stage_instance import StageInstance as StageInstancePayload
    from neocord.models.guild import Guild
    from neocord.api.state import State

class StageInstance(DiscordModel):
    """Represents a stage instance.

    A stage instance is an event in stage channel that users can discover
    using stage discovery and join the stage channel.

    Attributes
    ----------
    id: :class:`int`
        The snowflake ID of this instance.
    guild_id: :class:`int`
        The guild ID that this instance belongs to.
    channel_id: :class:`int`
        The snowflake ID of the stage channel that this instance is associated to.
    topic: Optional[:class:`str`]
        The topic of stage instance.
    privacy_level: :class:`StagePrivacyLevel`
        The privacy level of this instance.
    discoverable_disabled: :class:`bool`
        Whether this instance is disabled to be publicly discoverable.
    """
    __slots__ = (
        'id', 'channel_id', 'topic', 'privacy_level', 'discoverable_disabled',
        'guild', '_state', 'guild_id',
    )
    def __init__(self, data: StageInstancePayload, state: State):
        self._state = state
        self._update(data)

    @property
    def guild(self) -> Optional[Guild]:
        """
        Optional[:class:`Guild`]: Returns the guild that belongs to this stage instance.

        Requires :attr:`GatewayIntents.guilds` to be enabled.
        """
        return self._state.get_guild(self.guild_id) # type: ignore

    def _update(self, data: StageInstancePayload):
        self.guild_id = int(data['guild_id'])
        self.id = int(data['id'])
        self.channel_id = int(data['channel_id'])
        self.topic = data.get('topic')
        self.privacy_level = helpers.int_or_none(data, 'privacy_level') or 2
        self.discoverable_disabled = data.get('discoverable_disabled', False)

    async def delete(self, *, reason: Optional[str] = None):
        """Deletes the stage instance or in other words end the live stage.

        The user has to be stage moderator to perform this action i.e has following
        permissions:

        * :attr:`Permissions.manage_channels`
        * :attr:`Permissions.mute_members`
        * :attr:`Permissions.move_members`

        Parameters
        ----------
        reason: :class:`str`
            The reason for deleting the stage instance. Shows up on audit log.

        Raises
        ------
        Forbidden
            You are not allowed to delete this instance.
        HTTPError
            An error occured while performing this action.
        """
        await self._state.http.delete_stage_instance(
            instance_id=self.id,
            reason=reason,
        )