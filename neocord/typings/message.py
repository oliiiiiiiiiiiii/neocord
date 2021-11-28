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
from typing import Literal, Optional, Type, TypedDict, List, Union

from neocord.typings.snowflake import Snowflake
from neocord.typings.member import Member
from neocord.typings.emoji import Emoji
from neocord.typings.user import User

MessageActivityType = Literal[1, 2, 3, 5]
MessageType = Literal[
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
]

class ChannelMention(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    type: int
    name: str

class Reaction(TypedDict):
    count: int
    me: bool
    emoji: Emoji

class MessageActivity(TypedDict):
    type: MessageActivityType
    party_id: str

class _MessageOptional(TypedDict, total=False):
    guild_id: Snowflake
    member: Member
    mention_channels: List[ChannelMention]
    reactions: List[Reaction]
    nonce: Union[str, int]
    webhook_id: Snowflake
    activity: MessageActivity
    flags: int
    # referenced_message: Optional[Message]
    # interaction: Interaction
    # thread: Thread
    # components: List[Component]
    # stickers: List[Sticker]
    # sticker_items: List[StickerItem]

class _AttachmentOptional(TypedDict, total=False):
    ephemeral: bool
    height: Optional[int]
    width: Optional[int]
    description: str

class Attachment(_AttachmentOptional):
    id: Snowflake
    filename: str
    content_type: str
    size: int
    url: str
    proxy_url: str

class Message(_MessageOptional):
    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: str
    edited_timestamp: str
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[Snowflake]
    # attachments: List[Attachment]
    # embeds: List[Embed]
    pinned: bool
    type: MessageType