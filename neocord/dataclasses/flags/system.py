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

class SystemChannelFlags(BaseFlags):
    """Represents the flags for a guild system channel.

    Attributes
    ----------
    value: :class:`int`
        The raw integer value of flag.
    """
    VALID_FLAGS = {
        "suppress_join_notifications",
        "suppress_premium_subscriptions",
        "suppress_guild_reminder_notifications",
        "suppress_join_notification_replies"
    }


    @flag
    def suppress_join_notifications(self) -> int:
        """Returns True if join notifications is enabled in system channels."""
        return 1 << 0

    @flag
    def suppress_premium_subscriptions(self) -> int:
        """Returns True if server boosts notifications is enabled in system channels."""
        return 1 << 1

    @flag
    def suppress_guild_reminder_notifications(self) -> int:
        """Returns True if guild reminders in system channels is enabled."""
        return 1 << 2

    @flag
    def suppress_join_notification_replies(self) -> int:
        """Returns True if user are allowed to reply to system channel join messages."""
        return 1 << 3