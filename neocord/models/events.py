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

class ScheduledEventStatus:
    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELLED = 4

class EntityType:
    VOICE_CHANNEL = 1
    STAGE_INSTANCE = 2
    EXTERNAL = 3

class EventPrivacyLevel:
    GUILD_ONLY = 2

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

    async def edit(self, *,
        channel: Optional[DiscordModel] = MISSING,
        location: Optional[str] = MISSING,
        name: Optional[str] = MISSING,
        privacy_level: Optional[int] = MISSING,
        starts_at: Optional[datetime.datetime] = MISSING,
        ends_at: Optional[datetime.datetime] = MISSING,
        description: Optional[str] = MISSING,
        entity_type: Optional[int] = MISSING,
        status: Optional[int] = MISSING,
    ):
        """
        Edits the scheduled event.

        Requires you to have :attr:`Permissions.manage_events` in the event's guild.

        Parameters
        ----------
        name: :class:`str`
            The name of event.
        starts_at: :class:`datetime.datetime`
            The datetime representation of the time when the event will be scheduled
            to start.
        ends_at: :class:`datetime.datetime`
            The datetime representation of the time when the event will be scheduled
            to end. Ending time is required for external events but optional for non-external
            events.
        description: :class:`str`
            The description of event.
        channel: Union[:class:`VoiceChannel`, `StageChannel`]
            The channel where the event is being hosted. Cannot be mixed with ``location``.
        location: :class:`str`
            The external location name where event is being hosted. Cannot be mixed with
            ``channel``.
        privacy_level: :class:`EventPrivacyLevel`
            The privacy level of event. Defaults to :attr:`~EventPrivacyLevel.GUILD_ONLY`
        entity_type: :class:`EntityType`
            The type of entity where event is being hosted. You must provide this
            to edit the entity of event from channel to location and vice versa.
        status: :class:`EventStatus`
            The new status of the event. This parameter can be used to start, end or cancel
            the event.

            There are some considerations for this parameter. Some major ones
            are mentioned below:

            * You cannot start an already active event.
            * You cannot cancel an active event.
            * You cannot end a scheduled event. You can only cancel it.
            * You can only end an active event.

        Raises
        ------
        Forbidden
            You don't have permissions to edit an event.
        HTTPError
            Editing of event failed.
        """
        payload = {}

        if channel is not MISSING:
            if channel is None:
                payload['channel_id'] = None
            else:
                payload['channel_id'] = channel.id

        if location is not MISSING:
            payload['entity_metadata'] = {'location': location}

        if name is not MISSING:
            payload['name'] = name

        if privacy_level is not MISSING:
            payload['privacy_level'] = privacy_level

        if starts_at is not MISSING:
            payload['scheduled_start_time'] = starts_at.isoformat()

        if ends_at is not MISSING:
            payload['scheduled_end_time'] = ends_at.isoformat()

        if description is not MISSING:
            payload['description'] = description

        if entity_type is not MISSING:
            payload['entity_type'] = entity_type

        if status is not MISSING:
            payload['status'] = status

        if payload:
            data = await self._state.http.edit_guild_event(
                guild_id=self.guild.id,
                event_id=self.id,
                payload=payload,
            )
            self._update(data)

    async def delete(self):
        """
        Deletes the guild scheduled event.

        Returns
        -------
        :class:`ScheduledEvent`
            The deleted event.

        Raises
        ------
        Forbidden
            You don't have permissions to delete this event.
        NotFound
            Event not found.
        HTTPError
            Deleting of event failed.
        """
        await self._state.http.delete_guild_event(
            guild_id=self.guild.id,
            event_id=self.id,
        )

