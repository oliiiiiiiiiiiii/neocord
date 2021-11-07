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

from neocord.dataclasses.flags.base import BaseFlags, flag

class GatewayIntents(BaseFlags):
    """Represents the gateway intents.

    Intents allow you to choose to enable or disable certain events
    that you don't want or need to recieve over gateway.

    Following are the privileged intents that are required to be explicitly
    enabled from Discord Developer portal and require whitelisting if the bot
    if in over 100 guilds:

    - :attr:`GatewayIntents.members`
    - :attr:`GatewayIntents.presence`

    To see a brief list of events that would be recieved over gateway for
    certain intents, See the official
    `documentation`_ <https://discord.com/developers/docs/topics/gateway#gateway-intents>.

    Attributes
    ----------
    value: :class:`int`
        The raw integer value of the intents.
    """
    # (p): privileged
    VALID_FLAGS = {
        'guilds',
        'members', # (p)
        'bans',
        'emojis_and_stickers',
        'integrations',
        'webhooks',
        'invites',
        'voice_states',
        'presences', # (p)
        'guild_messages',
        'guild_messages_reactions',
        'guild_messages_typing',
        'direct_messages',
        'direct_messages_reactions',
        'direct_messages_typing',
        "messages"
    }
    def __init__(self, **intents):
        super().__init__(**intents)

    @classmethod
    def from_value(cls, value: int) -> GatewayIntents:
        """Constructs the :class:`GatewayIntents` from the raw value.

        Parameters
        ----------
        value: :class:`int`
            The raw value to construct intents with.

        Returns
        -------
        :class:`GatewayIntents`
            The constructed intents from the value.
        """
        # we want to bypass __init__ here so we would use __new__
        # and manually set the value.

        intents = cls.__new__(cls)
        intents._value = value
        return intents

    @classmethod
    def all(cls) -> GatewayIntents:
        """Constructs a :class:`GatewayIntents` with all intents enabled
        (including privileged ones).

        Returns
        -------
        :class:`GatewayIntents`
        """
        flags = {flag: True for flag in cls.VALID_FLAGS}
        return cls(**flags)

    @classmethod
    def unprivileged(cls) -> GatewayIntents:
        """Constructs a :class:`GatewayIntents` with all default intents enabled
        except privileged ones.

        Returns
        -------
        :class:`GatewayIntents`
        """
        intents = cls.all()
        intents.members = False
        intents.presences = False
        return intents

    @flag
    def messages(self) -> int:
        """A shorthand that represents both :attr:`.guild_messages` and :attr:`.direct_messages`"""
        return 1 << 9 | 1 << 12

    @flag
    def messages_reactions(self) -> int:
        """A shorthand that represents both :attr:`.guild_messages_reactions` and :attr:`.direct_messages_reactions`"""
        return 1 << 10 | 1 << 13

    @flag
    def typing(self) -> int:
        """A shorthand that represents both :attr:`.guild_messages_typing` and :attr:`.direct_messages_typing`"""
        return 1 << 11 | 1 << 14

    @flag
    def guilds(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild intents are enabled."""
        return 1 << 0

    @flag
    def members(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild members intents are enabled.

        This is a privileged intent and must be explicitly enabled from Developers portal.
        If your bot is in more then 100 Guilds, you would require verification and
        intents whitelisting.
        """
        return 1 << 1

    @flag
    def bans(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild bans intents are enabled."""
        return 1 << 2

    @flag
    def emojis_and_stickers(self) -> int:
        """:class:`bool`: Returns ``True`` if the emojis and stickers intents are enabled."""
        return 1 << 3

    @flag
    def integrations(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild integrations intents are enabled."""
        return 1 << 4

    @flag
    def webhooks(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild webhooks intents are enabled."""
        return 1 << 5

    @flag
    def invites(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild invites intents are enabled."""
        return 1 << 6

    @flag
    def voice_states(self) -> int:
        """:class:`bool`: Returns ``True`` if the voice states intents are enabled."""
        return 1 << 7

    @flag
    def presences(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild members presences intents are enabled."""
        return 1 << 8

    @flag
    def guild_messages(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild messages intents are enabled."""
        return 1 << 9

    @flag
    def guild_messages_reactions(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild message reactions intents are enabled."""
        return 1 << 10

    @flag
    def guild_messages_typing(self) -> int:
        """:class:`bool`: Returns ``True`` if the guild messages typing trigger intents are enabled."""
        return 1 << 11

    @flag
    def direct_messages(self) -> int:
        """:class:`bool`: Returns ``True`` if the direct messages intents are enabled."""
        return 1 << 12

    @flag
    def direct_messages_reactions(self) -> int:
        """:class:`bool`: Returns ``True`` if the direct message reactions intents are enabled."""
        return 1 << 13

    @flag
    def direct_messages_typing(self) -> int:
        """:class:`bool`: Returns ``True`` if the direct messages typing trigger intents are enabled."""
        return 1 << 14