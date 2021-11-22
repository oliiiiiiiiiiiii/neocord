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
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.models.guild import Guild
    from neocord.typings.events import (
        GuildScheduledEvent as GuildScheduledEventPayload,
        EntityMetadata
    )

class ScheduledEvent(DiscordModel):
    """Represents a guild scheduled event.

    Attributes
    ----------
    ...
    """
    __slots__ = (
        'guild', '_state', 'id', 'guild_id', 'channel_id', 'creator_id', 'entity_id',
        'name', 'description', 'starts_at', 'ends_at', 'privacy_level', 'status',
        'entity_type', 'location', 'creator'
    )

    def __init__(self, data: GuildScheduledEventPayload, guild: Guild):
        self.guild = guild
        self._state = guild._state
        self._update(data)

    def _update(self, data: GuildScheduledEventPayload):
        self.id = helpers.get_snowflake(data, 'id') # type: ignore
        self.guild_id = helpers.get_snowflake(data, 'guild_id') or (self.guild and self.guild.id)
        self.channel_id = helpers.get_snowflake(data, 'channel_id')
        self.creator_id = helpers.get_snowflake(data, 'creator_id')
        self.entity_id = helpers.get_snowflake(data, 'entity_id')

        self.name = data.get('name')
        self.description = data.get('description')

        self.starts_at = helpers.iso_to_datetime(data.get('scheduled_start_time'))
        self.ends_at = helpers.iso_to_datetime(data.get('scheduled_end_time'))

        self.privacy_level = helpers.int_or_none(data, 'privacy_level') # type: ignore
        self.status = helpers.int_or_none(data, 'status') # type: ignore
        self.entity_type = helpers.int_or_none(data, 'entity_type') # type: ignore

        try:
            creator = data['creator']
        except KeyError:
            self.creator = None
        else:
            self.creator = self._state.add_user(creator)

        self._apply_metadata(data.get('entity_metadata')) # type: ignore

    def _apply_metadata(self, metadata: EntityMetadata):
        self.location = metadata.get('location')

    def __repr__(self) -> str:
        if self.status == 1:
            status = 'SCHEDULED'
        elif self.status == 2:
            status = 'ACTIVE'
        elif self.status == 3:
            status = 'COMPLETED'
        elif self.status == 4:
            status = 'CANCELLED'
        else:
            status = 'UNKNOWN STATUS'

        return f"<ScheduledEvent name={self.name} id={self.id} {status}>"

    async def delete(self):
        """
        Deletes the guild scheduled event.

        Returns
        -------
        :class:`ScheduledEvent`
            The deleted event.

        Raises
        ------
        Forbidden:
            You don't have permissions to delete this event.
        NotFound:
            Event not found.
        HTTPError
            Deleting of event failed.
        """
        await self._state.http.delete_guild_event(
            guild_id=self.guild.id,
            event_id=self.id,
        )

