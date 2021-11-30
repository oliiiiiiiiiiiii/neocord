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

class MessageFlags(BaseFlags):
    """Represents the flags for a message.

    Attributes
    ----------
    crossposted: :class:`bool`
        Returns True if message has been published.
    crosspost: :class:`bool`
        Returns True if message is a crosspost by a channel followed by message's channel.
    suppress_embeds: :class:`bool`
        Returns True if embeds on the message should be suppressed.
    source_message_deleted: :class:`bool`
        Returns True if message is a crosspost and the original message has been deleted.
    urgent: :class:`bool`
        Returns True if the message is an urgent system message.
    thread_parent: :class:`bool`
        Returns True if the message has a thread belonging to it.
    ephemeral: :class:`bool`
        Returns True if only the user who created the interaction can see this message.
    loading: :class:`bool`
        Returns True if the message is an interaction response and the application is
        currently in "Thinking" state.
    """
    VALID_FLAGS = {
        'crossposted', 'crosspost', 'suppress_embeds', 'source_message_deleted', 'urgent',
        'thread_parent', 'ephemeral', 'loading'
    }

    @flag
    def crossposted(self) -> int:
        return 1 << 0

    @flag
    def crosspost(self) -> int:
        return 1 << 1

    @flag
    def suppress_embeds(self) -> int:
        return 1 << 2

    @flag
    def source_message_deleted(self) -> int:
        return 1 << 3

    @flag
    def urgent(self) -> int:
        return 1 << 4

    @flag
    def thread_parent(self) -> int:
        return 1 << 5

    @flag
    def ephemeral(self) -> int:
        return 1 << 6

    @flag
    def loading(self) -> int:
        return 1 << 7




