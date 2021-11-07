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
from typing import List, Optional, TYPE_CHECKING

from neocord.models.base import DiscordModel
from neocord.models.asset import CDNAsset
from neocord.models.role import Role
from neocord.dataclasses.flags.system import SystemChannelFlags
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.typings.guild import Guild as GuildPayload
    from neocord.typings.role import Role as RolePayload
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
        'welcome_screen', 'features', '_roles'
    )

    def __init__(self, data: GuildPayload, state: State):
        self._state = state
        self._voice_states = {}
        self._members = {}
        self._channels = {}
        self._threads = {}
        self._presences = {}
        self._stage_instances = {}
        self._stickers = {}
        self._emojis = {}
        self._roles = {}
        self._update(data)

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

        for role in data.get('roles', []):
            self._add_role(role)

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