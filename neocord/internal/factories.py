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

# This module exists to avoid circular imports.

from __future__ import annotations
from typing import TYPE_CHECKING, Type, Any


from neocord.models.channels import (
    ChannelType,
    GuildChannel,
    TextChannel,
    CategoryChannel,
    VoiceChannel,
    StageChannel
)
from neocord.models.stickers import (
    StickerType,
    Sticker,
    StandardSticker,
)

def channel_factory(ctype: int) -> Type[GuildChannel]:
    if ctype == ChannelType.TEXT:
        return TextChannel
    if ctype == ChannelType.CATEGORY:
        return CategoryChannel
    if ctype == ChannelType.VOICE:
        return VoiceChannel
    if ctype == ChannelType.STAGE:
        return StageChannel
    else:
        return GuildChannel

def sticker_factory(stype: int) -> Type[Sticker]:
    if stype == StickerType.STANDARD:
        return StandardSticker
    else:
        return Sticker