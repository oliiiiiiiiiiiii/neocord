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
from typing import Union, Literal, TYPE_CHECKING, Iterator, Tuple

from neocord.dataclasses.flags.base import BaseFlags, flag
from neocord.internal.missing import MISSING

if TYPE_CHECKING:
    PermissionOverwriteType = Union[Literal[None], bool]

class Permissions(BaseFlags):
    """
    Represents the permissions that can be applied on channels, roles, users
    and other entities.

    This data class wraps the permissions bitwise in user friendly form so they can
    be easily manipulated.

    You can either pass a raw permission bitwise value or permissions as keyword
    arguments to initalize an instance of this class.

    Parameters
    ----------
    value: :class:`int`
        The raw permissions value.
    """
    VALID_FLAGS = {
        'create_instant_invite', 'kick_members', 'ban_members', 'administrator',
        'manage_channels', 'manage_channel', 'manage_guild', 'add_reactions',
        'view_audit_log', 'priority_speaker', 'stream', 'view_channels',
        'view_channel', 'send_messages', 'send_tts_messages', 'manage_messages',
        'embed_links', 'attach_files', 'read_message_history', 'mention_everyone',
        'use_external_emojis', 'view_guild_insights', 'connect', 'speak', 'mute_members',
        'deafen_members', 'move_members', 'use_vad', 'change_nickname', 'manage_nicknames',
        'manage_roles', 'manage_webhooks', 'manage_emojis_and_stickers', 'use_application_commands',
        'request_to_speak', 'manage_events', 'manage_threads', 'create_public_threads',
        'create_private_threads', 'use_external_stickers', 'send_messages_in_threads',
        'start_embedded_activites',
    }

    @flag
    def create_instant_invite(self) -> int:
        """
        :class:`bool`: Indicates whether user can create invites or not.
        """
        return 1 << 0


    @flag
    def kick_members(self) -> int:
        """
        :class:`bool`: Indicates whether user can kick other members in guild.
        """
        return 1 << 1

    @flag
    def ban_members(self) -> int:
        """
        :class:`bool`: Indicates whether user can ban other members in guild.
        """
        return 1 << 2

    @flag
    def administrator(self) -> int:
        """
        :class:`bool`: Indicates if the "Administrator" permission is enabled. This
        permission bypasses all permissions.
        """
        return 1 << 3

    @flag
    def manage_channels(self) -> int:
        """
        :class:`bool`: Indicates if user can manage the guild channels or not.
        """
        return 1 << 4

    @flag
    def manage_channel(self) -> int:
        """
        An alias for :attr:`.manage_channels`
        """
        return 1 << 4

    @flag
    def manage_guild(self) -> int:
        """
        :class:`bool`: Indicates if user can manage the guild or not.
        """
        return 1 << 5

    @flag
    def add_reactions(self) -> int:
        """
        :class:`bool`: Indicates if the user can add reactions on reactions or not.
        """
        return 1 << 6

    @flag
    def view_audit_log(self) -> int:
        """
        :class:`bool`: Indicates if the user can see the audit logs of guild or not.
        """
        return 1 << 7

    @flag
    def priority_speaker(self) -> int:
        """
        :class:`bool`: Indicates if the user's voice is prioritized in vocal channels.
        """
        return 1 << 8

    @flag
    def stream(self) -> int:
        """
        :class:`bool`: Indicates if the user can stream in voice channels.
        """
        return 1 << 9

    @flag
    def view_channels(self) -> int:
        """
        :class:`bool`: Indicates if the user can view the channels including reading
        messages of the channels.
        """
        return 1 << 10


    @flag
    def view_channel(self) -> int:
        """
        An alias for :attr:`.view_channels`.
        """
        return 1 << 10

    @flag
    def send_messages(self) -> int:
        """
        :class:`bool`: Indicates whether the user can send messages in channels.
        """
        return 1 << 11

    @flag
    def send_tts_messages(self) -> int:
        """
        :class:`bool`: Indicates whether the user can send text-to-speech messages in channels.
        """
        return 1 << 12

    @flag
    def manage_messages(self) -> int:
        """
        :class:`bool`: Indicates whether the user can manage i.e delete, pin, messages in a channel.
        """
        return 1 << 13

    @flag
    def embed_links(self) -> int:
        """
        :class:`bool`: Indicates whether the user can send embedded messages.
        """
        return 1 << 14

    @flag
    def attach_files(self) -> int:
        """
        :class:`bool`: Indicates whether the user can attach files in messages.
        """
        return 1 << 15

    @flag
    def read_message_history(self) -> int:
        """
        :class:`bool`: Indicates whether the user can read the message history of a channel.
        """
        return 1 << 16


    @flag
    def mention_everyone(self) -> int:
        """
        :class:`bool`: Indicates whether the user can tag @everyone and @here roles in
        messages.
        """
        return 1 << 17

    @flag
    def use_external_emojis(self) -> int:
        """
        :class:`bool`: Indicates whether the user can use emojis from other servers in
        messages.
        """
        return 1 << 18

    @flag
    def view_guild_insights(self) -> int:
        """
        :class:`bool`: Indicates whether the user can view the insights stats for
        a guild.
        """
        return 1 << 19

    @flag
    def connect(self) -> int:
        """
        :class:`bool`: Indicates whether the user can connect to voice channels or not.
        """
        return 1 << 20

    @flag
    def speak(self) -> int:
        """
        :class:`bool`: Indicates whether the user can speak to voice channels or not.
        """
        return 1 << 21

    @flag
    def mute_members(self) -> int:
        """
        :class:`bool`: Indicates whether the user can mute members of voice channels or not.
        """
        return 1 << 22

    @flag
    def deafen_members(self) -> int:
        """
        :class:`bool`: Indicates whether the user can deafen members of voice channels or not.
        """
        return 1 << 23

    @flag
    def move_members(self) -> int:
        """
        :class:`bool`: Indicates whether the user can move or disconnect members of
        voice channels or not.
        """
        return 1 << 24

    @flag
    def use_vad(self) -> int:
        """
        :class:`bool`: Indicates whether the user can use voice activity in a voice channels.
        """
        return 1 << 25

    @flag
    def change_nickname(self) -> int:
        """
        :class:`bool`: Indicates whether the user can modify own nickname in a guild.
        """
        return 1 << 26

    @flag
    def manage_nicknames(self) -> int:
        """
        :class:`bool`: Indicates whether the user can modify other members nicknames in a guild.
        """
        return 1 << 27

    @flag
    def manage_roles(self) -> int:
        """
        :class:`bool`: Indicates whether the user can manage roles of guild.
        """
        return 1 << 28

    @flag
    def manage_webhooks(self) -> int:
        """
        :class:`bool`: Indicates whether the user can manage webhooks or not.
        """
        return 1 << 29

    @flag
    def manage_emojis_and_stickers(self) -> int:
        """
        :class:`bool`: Indicates whether the user can manage custom stickers and emojis.
        """
        return 1 << 30

    @flag
    def use_application_commands(self) -> int:
        """
        :class:`bool`: Indicates whether the user can use application commands i.e slash
        commands or context menus.
        """
        return 1 << 31

    @flag
    def request_to_speak(self) -> int:
        """
        :class:`bool`: Indicates whether the user can request to speak in a stage channel.
        """
        return 1 << 32

    @flag
    def manage_events(self) -> int:
        """
        :class:`bool`: Indicates whether the user can manage guild scheduled events.
        """
        return 1 << 33

    @flag
    def manage_threads(self) -> int:
        """
        :class:`bool`: Indicates whether the user can manage thread channels.
        """
        return 1 << 34

    @flag
    def create_public_threads(self) -> int:
        """
        :class:`bool`: Indicates whether the user can create public thread channels.
        """
        return 1 << 35

    @flag
    def create_private_threads(self) -> int:
        """
        :class:`bool`: Indicates whether the user can create private thread channels.
        """
        return 1 << 36

    @flag
    def use_external_stickers(self) -> int:
        """
        :class:`bool`: Indicates whether the user can use custom stickers from other
        guilds.
        """
        return 1 << 37

    @flag
    def send_messages_in_threads(self) -> int:
        """
        :class:`bool`: Indicates whether the user can send messages in thread channels.
        """
        return 1 << 38

    @flag
    def start_embedded_activites(self) -> int:
        """
        :class:`bool`: Indicates whether the user can create embedded activites in voice
        channels or not.
        """
        return 1 << 39

def _fill_default_overwrite_values(cls):
    for key in Permissions.VALID_FLAGS:
        setattr(cls, key, None)

    return cls

@_fill_default_overwrite_values
class PermissionOverwrite:
    """Represents a permission overwrite for a specific channel.

    The default value of a permission in this class is ``None`` which represents
    that no overwrite is applied. If a permission is ``False``, it indicates that permission
    has been explicitly denied and for a permission set to ``True`` indicates permission
    is explicitly allowed.

    This class takes same parameters (permissions) as :class:`Permissions`.
    """
    def __init__(self, **perms: Any):
        for key, value in perms.items():
            if not key in Permissions.VALID_FLAGS:
                raise TypeError("{} is not a valid permission.".format(key))

            if not value in {True, False, None}:
                raise TypeError("Value for {} expected to be NoneType or bool, Got {} instead.".format(key, value.__class__.__name__))

            setattr(self, key, value)

    def pair(self) -> Tuple[Permissions, Permissions]:
        """
        Creates a (allow, deny) tuple of permissions from this permission
        overwrite.

        Returns
        -------
        Tuple[:class:`Permissions`, :class:`Permissions`]
        """
        allow = Permissions(0)
        deny = Permissions(0)

        for flag in Permissions.VALID_FLAGS:
            val = getattr(self, flag, MISSING)

            if val is False:
                setattr(deny, flag, True)
            elif val is True:
                setattr(allow, flag, True)

        return allow, deny


    @classmethod
    def from_pair(cls, allow: Permissions, deny: Permissions) -> PermissionOverwrite:
        """Creates a permission overwrite with allow, deny permissions pair.

        Parameters
        ----------
        allow: :class:`Permissions`
            The permissions to allow.
        deny: :class:`Permissions`
            The permissions to deny.

        Returns
        -------
        :class:`PermissionOverwrite`
            The created permission overwrite.
        """
        overwrite = cls()

        for key in allow.VALID_FLAGS:
            value = getattr(allow, key)
            if value is True:
                setattr(overwrite, key, True)

        for key in deny.VALID_FLAGS:
            value = getattr(deny, key)
            if value is True:
                setattr(overwrite, key, False)

        return overwrite

    def __setattr__(self, name: str, value: PermissionOverwriteType):
        if name.startswith('_'):
            pass
        else:
            if not name in Permissions.VALID_FLAGS:
                raise TypeError("{} is not a valid permission.".format(name))

            if not value in (None, True, False):
                raise TypeError("Value for {} expected to be NoneType or bool, Got {} instead.".format(key, value.__class__.__name__))

        return super().__setattr__(name, value)