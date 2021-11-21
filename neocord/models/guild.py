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
from typing import List, Optional, Any, TYPE_CHECKING

from neocord.models.base import DiscordModel
from neocord.models.asset import CDNAsset
from neocord.models.role import Role
from neocord.models.member import GuildMember
from neocord.models.emoji import Emoji
from neocord.models.events import ScheduledEvent
from neocord.internal.factories import channel_factory
from neocord.internal import helpers
from neocord.dataclasses.flags.system import SystemChannelFlags
from neocord.internal.missing import MISSING

if TYPE_CHECKING:
    from neocord.models.channels.base import GuildChannel
    from neocord.typings.guild import Guild as GuildPayload
    from neocord.typings.role import Role as RolePayload
    from neocord.typings.member import Member as MemberPayload
    from neocord.typings.emoji import Emoji as EmojiPayload
    from neocord.typings.events import GuildScheduledEvent as GuildScheduledEventPayload
    from neocord.api.state import State
    from datetime import datetime

class Guild(DiscordModel):
    """Represents a discord guild entity often referred as a "Server" in the UI.

    Attributes
    ----------
    id: :class:`int`
        The unique snowflake ID of the guild.
    name: :class:`str`
        The name of guild.
    afk_timeout: :class:`int`
        The number of seconds after which idle members would be moved
        to the AFK channel. ``0`` means there is no timeout.
    widget_enabled: :class:`bool`
        Whether the guild has enabled embed widget.
    verification_level: :class:`VerificiationLevel`
        The verification level for the users of this guild.
    default_message_notifications: :class:`NotificationLevel`
        The message notification level of this guild.
    explicit_content_filter: :class:`ContentFilter`
        The explicit content filter of this guild. i.e if the sent media is scanned
        or not.
    features: :class:`str`
        The :class:`list` of the features this guild has, Guild features represent
        the features this guild has access to like role icons, welcome screen etc.
    mfa_level: :class:`MFALevel`
        The MFA level of this guild.
    application_id: Optional[:class:`int`]
        The ID of application that created this guild if it is bot created, This is usually
        ``None``
    large: Optional[:class:`bool`]
        Whether this guild is marked as a large guild. This is not available if the guild
        if fetched manually instead of getting from client's internal cache.
    unavailable: Optional[:class:`bool`]
        Whether this guild is unavailable due to an outage. This is not available if the guild
        if fetched manually instead of getting from client's internal cache.
    member_count: Optional[:class:`int`]
        The member count of this guild. This is not available if the guild
        if fetched manually instead of getting from client's internal cache.
    vanity_url_code: Optional[:class:`str`]
        The vanity URL code of this guild if any, Otherwise None.
    description: Optional[:class:`str`]
        The description of the guild. Could be None
    premium_tier: :class:`PremiumTier`
        The premium tier of this guild "aka" the server boost level.
    premium_subscription_count: :class:`int`
        The premium subscription count of this guild "aka" the number of boosts
        this guild has.
    preferred_locale: :class:`str`
        the preferred locale of a Community guild; used in server discovery and notices
        from Discord; Usually "en-US"
    approximate_member_count: :class:`int`
        The approximate member count of the guild, This is only available when
        fetching the guild using :meth:`~Client.fetch_guild` with ``with_counts`` parameter
        to ``True``
    approximate_presence_count: :class:`int`
        The approximate presences count of the guild, This is only available when
        fetching the guild using :meth:`~Client.fetch_guild` with ``with_counts`` parameter
        to ``True``
    nsfw_level: :class:`NSFWLevel`
        The NSFW level of the guild.
    system_channel_flags: :class:`SystemChannelFlags`
        The system channel's attributes of the guild.
    """

    __slots__ = (
        '_state', '_voice_states', '_members', '_channels', '_threads', '_presences',
        '_stage_instances', '_stickers', '_emojis', 'name', 'afk_timeout', 'widget_enabled', 'large',
        'unavailable', 'member_count', 'premium_subscription_count', 'max_presences',
        'max_members', 'max_video_channel_users', 'vanity_url_code', 'description',
        'preferred_locale', 'approximate_member_count', 'approximate_presence_count',
        'id', 'owner_id', 'afk_channel_id', 'widget_channel_id', 'application_id',
        'system_channel_id', 'rules_channel_id', 'public_updates_channel_id', 'system_channel_flags',
        '_joined_at', 'verification_level', 'default_message_notifications', 'explicit_content_filter',
        'mfa_level', 'premium_tier', 'nsfw_level', '_icon', '_splash', '_banner', '_discovery_splash',
        'welcome_screen', 'features', '_roles', '_scheduled_events',
    )

    def __init__(self, data: GuildPayload, state: State):
        self._state = state

        self._voice_states = {}
        self._threads = {}
        self._presences = {}
        self._stage_instances = {}
        self._stickers = {}
        self._scheduled_events = {}

        self._members = {}
        self._channels = {}
        self._emojis = {}
        self._roles = {}

        self._update(data)

        for channel in data.get('channels', []):
            self._add_channel(channel)
        for role in data.get('roles', []):
            self._add_role(role)
        for member in data.get('members', []):
            self._add_member(member)
        for event in data.get('guild_scheduled_events', []):
            self._add_event(event)

        self._bulk_overwrite_emojis(data.get('emojis', []))

    def _update(self, data: GuildPayload):
        self.name = data.get('name')
        self.afk_timeout = data.get('afk_timeout', 0)
        self.widget_enabled = data.get('widget_enabled', False)
        self.large = data.get('large', False)
        self.unavailable = data.get('unavailable', False)
        self.member_count = data.get('member_count')
        self.premium_subscription_count = data.get('premium_subscription_count', 0)
        self.max_presences = data.get('max_presences')
        self.max_members = data.get('max_members')
        self.max_video_channel_users = data.get('max_video_channel_users')
        self.vanity_url_code = data.get('vanity_url_code')
        self.description = data.get('description')
        self.preferred_locale = data.get('preferred_locale', 'en-US')
        self.approximate_member_count = data.get('approximate_member_count')
        self.approximate_presence_count = data.get('approximate_presence_count')
        self.features = data.get('features', [])


        # snowflakes
        self.id = helpers.get_snowflake(data, 'id') # type: ignore
        self.owner_id = helpers.get_snowflake(data, 'owner_id')
        self.afk_channel_id = helpers.get_snowflake(data, 'afk_channel_id')
        self.widget_channel_id = helpers.get_snowflake(data, 'widget_channel_id')
        self.application_id = helpers.get_snowflake(data, 'application_id')
        self.system_channel_id = helpers.get_snowflake(data, 'system_channel_id')
        self.rules_channel_id = helpers.get_snowflake(data, 'rules_channel_id')
        self.public_updates_channel_id = helpers.get_snowflake(data, 'public_updates_channel_id')

        # flags
        self.system_channel_flags = SystemChannelFlags(data.get('system_channel_flags') or 0)

        # timestamps
        self._joined_at = data.get('joined_at')

        # enums
        self.verification_level = data.get('verification_level')
        self.default_message_notifications = data.get('default_message_notifications')
        self.explicit_content_filter = data.get('explicit_content_filter')
        self.mfa_level = data.get('mfa_level')
        self.premium_tier = data.get('premium_tier')
        self.nsfw_level = data.get('nsfw_level')


        # assets
        self._icon = data.get('icon')
        self._splash = data.get('splash')
        self._discovery_splash = data.get('discovery_splash')
        self._banner = data.get('banner')

        # objects
        self.welcome_screen = data.get('welcome_screen')


    # assets

    @property
    def icon(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the CDN asset for the icon of guild.

        This may be None if the guild has no icon set.
        """
        if self._icon:
            return CDNAsset(
                key=self._icon,
                path=f'/icons/{self.id}',
                state=self._state,
            )

    @property
    def splash(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the CDN asset for the splash of guild.

        This may be None if the guild has no splash set.
        """
        if self._splash:
            return CDNAsset(
                key=self._splash,
                path=f'/splashes/{self.id}',
                state=self._state,
            )

    @property
    def discovery_splash(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the CDN asset for the discovery splash of guild.

        This may be None if the guild has no discovery splash set. This is only applicable
        for guilds with ``DISCOVERY`` feature enabled.
        """
        if self._discovery_splash:
            return CDNAsset(
                key=self._discovery_splash,
                path=f'/discovery-splashes/{self.id}',
                state=self._state,
            )

    @property
    def banner(self) -> Optional[CDNAsset]:
        """
        Optional[:class:`CDNAsset`]: Returns the CDN asset for the invite banner of guild.

        This may be None if the guild has no banner set.
        """
        if self._banner:
            return CDNAsset(
                key=self._banner,
                path=f'/banners/{self.id}',
                state=self._state,
            )


    @property
    def joined_at(self) -> Optional[datetime]:
        """
        Returns :class:`datetime.datetime` representation of when the bot
        has joined the guild.

        This could be unavailable in some (rare) cases.
        """
        if self._joined_at:
            return helpers.iso_to_datetime(self._joined_at)

    @property
    def vanity_invite(self) -> Optional[str]:
        """
        Returns the string for guild's vanity invite URL if available.
        """
        if self.vanity_url_code:
            return f'https://discord.gg/{self.vanity_url_code}'


    def _add_role(self, data: RolePayload) -> Role:
        role = Role(data, guild=self)
        self._roles[role.id] = role
        return role

    def _remove_role(self, id: int, /) -> Optional[Role]:
        return self._roles.pop(id, None)

    @property
    def roles(self) -> List[Role]:
        """
        Returns the list of :class:`Role` that belong to this guild.
        """
        return list(self._roles.values())

    def get_role(self, id: int, /) -> Optional[Role]:
        """
        Gets a role from the guild. This method returns None is the role with ID
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

    def _add_member(self, data: MemberPayload):
        member = GuildMember(data, guild=self)
        # although user should always be present in this
        # case of scenario but i'm not sure on this statement
        # so here is a check.
        if 'user' in data:
            user = self._state.add_user(data['user']) # type: ignore
        self._members[member.id] = member
        return member

    def _remove_member(self, id: int):
        return self._members.pop(id, None)

    @property
    def members(self) -> List[GuildMember]:
        """
        Returns the list of :class:`GuildMember` that belong to this guild.

        This requires :class:`GatewayIntents.guild_members` to be enabled.
        """
        return list(self._members.values())

    def get_member(self, id: int, /) -> Optional[GuildMember]:
        """
        Gets a member from the guild. This method returns None is the member with ID
        is not found.

        This requires :class:`GatewayIntents.guild_members` to be enabled.

        Parameters
        ----------
        id: :class:`int`
            The ID of the member.

        Returns
        -------
        :class:`GuildMember`
            The requested member.
        """
        return self._members.get(id)

    async def fetch_member(self, id: int, /) -> GuildMember:
        """
        Fetches a member from the guild.

        This is a direct API call and shouldn't be used in general cases. If you
        have member intents, Consider using :meth:`.get_member`

        Parameters
        ----------
        id: :class:`int`
            The snowflake ID of member.

        Returns
        -------
        :class:`GuildMember`
            The requested member.

        Raises
        ------
        NotFound:
            Member not found.
        HTTPError
            Fetching of member failed.
        """
        data = await self.state.http.get_guild_member(guild_id=self.id, member_id=id)
        return GuildMember(data, guild=self)

    async def edit_member(self,
        member: DiscordModel, *,
        nick: Optional[str] = MISSING,
        roles: Optional[List[DiscordModel]] = MISSING,
        mute: Optional[bool] = MISSING,
        deaf: Optional[bool] = MISSING,
        voice_channel: Optional[DiscordModel] = MISSING,
        reason: str = None
    ):
        """
        Edits a member from this guild.

        This is a shorthand to :meth:`GuildMember.edit` except this doesn't requires the
        member to be fetched explicitly.

        Except ``member``, All parameters are optional and keyword only.

        Parameters
        ----------
        member: :class:`Member`
            The member that will be edited. :class:`ModelMimic` can be passed
            to avoid fetching or getting the member explicitly.
        nick: :class:`str`
            The new nickname of member.
        roles: List[:class:`Role`]
            List of roles (or :class:`ModelMimic`) that should be assigned to member.
        mute: :class:`bool`
            Whether to mute the member in voice channel. Requires member to be in voice
            channel.
        deaf: :class:`bool`
            Whether to deafen the member in voice channel. Requires member to be in voice
            channel.
        voice_channel: :class:`VoiceChannel`
            The voice channel to move the member to. Requires member to be in voice
            channel.
        reason: :class:`str`
            The reason for this action that shows up on audit log.
        """
        payload = {}

        if nick is not MISSING:
            payload['nick'] = nick
        if roles is not MISSING:
            payload['roles'] = [r.id for r in roles]
        if mute is not MISSING:
            payload['mute'] = mute
        if deaf is not MISSING:
            payload['deaf'] = deaf
        if voice_channel is not MISSING:
            payload['channel_id'] = voice_channel.id

        if payload:
            await self.state.http.edit_guild_member(
                guild_id=self.id,
                member_id=member.id,
                payload=payload,
                reason=reason
                )

    async def kick_member(self, member: DiscordModel, *, reason: str = None):
        """
        Kicks a member from this guild.

        This is a shorthand to :meth:`GuildMember.kick` except this doesn't requires the
        member to be fetched explicitly.

        Except ``member``, All parameters are optional and keyword only.

        Parameters
        ----------
        member: :class:`Member`
            The member that will be kicked. :class:`ModelMimic` can be passed
            to avoid fetching or getting the member explicitly.
        reason: :class:`str`
            The reason for this action that shows up on audit log.
        """
        await self.state.http.kick_guild_member(
            guild_id=self.id,
            member_id=member.id,
            reason=reason
            )

    def _add_channel(self, data: Any) -> GuildChannel:
        cls = channel_factory(int(data['type']))
        channel = cls(data, guild=self)
        self._channels[channel.id] = channel
        return channel

    def _remove_channel(self, id: int, /) -> Optional[GuildChannel]:
        return self._channels.pop(id, None)

    @property
    def channels(self) -> List[GuildChannel]:
        """List[:class:`GuildChannel`]: Returns the list of channels in guild.

        These are sorted in the same way as in the Discord client i.e voice channels
        below other channels.
        """
        channels = list(self._channels.values())
        channels.sort(key=lambda c: c.position)

        return channels

    def get_channel(self, id: int, /) -> Optional[GuildChannel]:
        """
        Gets a channel from the guild. This method returns None is the channel with ID
        is not found.

        Parameters
        ----------
        id: :class:`int`
            The ID of the channel.

        Returns
        -------
        :class:`GuildChannel`
            The requested channel.
        """
        return self._channels.get(id)

    def _add_emoji(self, data: EmojiPayload):
        emoji = Emoji(data, guild=self)
        self._emojis[emoji.id] = emoji
        return emoji

    def _remove_emoji(self, id: int):
        return self._emojis.pop(id, None)

    def _bulk_overwrite_emojis(self, emojis: List[EmojiPayload]):
        # This is for GUILD_EMOJIS_UPDATE event, we don't have separate
        # create or delete events for emojis.

        self._emojis.clear()

        for emoji in emojis:
            self._add_emoji(emoji)


    def get_emoji(self, id: int, /) -> Optional[Emoji]:
        """
        Gets a custom emoji from the guild. This method returns None is the emoji with
        provided ID is not found.

        Parameters
        ----------
        id: :class:`int`
            The ID of the emoji.

        Returns
        -------
        :class:`Emoji`
            The requested emoji.
        """
        return self._emojis.get(id)

    @property
    def emojis(self) -> List[Emoji]:
        """
        List[:class:`Emoji`]: Returns the list of custom emojis that belong to this guild.
        """
        return list(self._emojis.values())

    async def fetch_emoji(self, id: int, /) -> Emoji:
        """
        Fetches a custom emoji from the guild.

        This is a direct API call and shouldn't be used in general cases.
        Consider using :meth:`.get_emoji` instead.

        Parameters
        ----------
        id: :class:`int`
            The snowflake ID of emoji.

        Returns
        -------
        :class:`Emoji`
            The requested emoji.

        Raises
        ------
        NotFound:
            Emoji not found.
        HTTPError
            Fetching of emoji failed.
        """
        data = await self._state.http.get_guild_emoji(guild_id=self.id, emoji_id=id)
        return Emoji(data, guild=self)

    async def fetch_emojis(self) -> List[Emoji]:
        """
        Fetches all custom emojis from the guild.

        This is a direct API call and shouldn't be used in general cases.
        Consider using :attr:`.emojis` instead.

        Returns
        -------
        List[:class:`Emoji`]
            The list of emojis in the guild.

        Raises
        ------
        HTTPError
            Fetching of emojis failed.
        """
        data = await self._state.http.get_guild_emojis(guild_id=self.id)
        return [Emoji(emj, guild=self) for emj in data]

    async def create_emoji(self, *,
        emoji: bytes,
        name: str,
        roles: Optional[List[DiscordModel]] = None,
        reason: Optional[str] = None,
        ) -> Emoji:
        """
        Creates a custom guild emoji.

        You must have :attr:`~Permissions.manage_emojis` to perform this
        action in the guild.

        Parameters
        ----------
        emoji: :class:`bytes`
            The bytes like object of data representing the emoji. The size must be less
            then or equal to 256kb. Supported types are GIF, PNG, JPEG, and WebP.
        name: :class:`str`
            The name of emoji.
        roles: List[:class:`Role`]
            The list of roles that can use this emoji.
        reason: :class:`str`
            Reason for creating this emoji that shows up on guild's audit log.

        Raises
        ------
        Forbidden:
            You don't have permissions to create an emoji.
        HTTPError
            Creation of emoji failed.
        """
        payload = {}

        payload['image'] = helpers.get_image_data(emoji)
        payload['name'] = str(name)

        if roles is not None:
            payload['roles'] = [r.id for r in roles]

        data = await self._state.http.create_guild_emoji(
            guild_id=self.id,
            payload=payload,
            reason=reason
            )
        return Emoji(data, guild=self)

    def _add_event(self, data: GuildScheduledEventPayload):
        event = ScheduledEvent(data, guild=self)
        self._scheduled_events[event.id] = event
        return event

    def _remove_event(self, id: int):
        return self._scheduled_events.pop(id, None)

    def get_scheduled_event(self, id: int, /) -> Optional[ScheduledEvent]:
        """
        Gets a scheduled event from the guild. This method returns None is the scheduled event
        with provided ID is not found.

        Parameters
        ----------
        id: :class:`int`
            The ID of the event.

        Returns
        -------
        Optional[:class:`ScheduledEvent`]
            The requested event, if found.
        """
        return self._scheduled_events.get(id)

    @property
    def scheduled_events(self) -> List[ScheduledEvent]:
        """
        List[:class:`ScheduledEvent`]: Returns the list of scheduled events that belong to
        this guild.
        """
        return list(self._scheduled_events.values())