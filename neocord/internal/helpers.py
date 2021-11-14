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
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from neocord.internal.missing import MISSING

import datetime
import base64

if TYPE_CHECKING:
    from neocord.dataclasses.embeds import Embed

def get_image_data(data: Optional[bytes]) -> Optional[str]:
    if data is None or data is MISSING:
        return None

    if data.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
        mime = "image/png"
    elif data[0:3] == b"\xff\xd8\xff" or data[6:10] in (b"JFIF", b"Exif"):
        mime = "image/jpeg"
    elif data.startswith((b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")):
        mime = "image/gif"
    elif data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        raise TypeError("invalid or unsupported image type was provided, valid types are jpeg, png, gif, webp")

    data = base64.b64encode(data)
    ret = data.decode("ascii")
    return "data:{0};base64,{1}".format(mime, ret)

def get_snowflake(data: Any, key: str) -> Optional[int]:
    try:
        return int(data[key])
    except:
        return

def iso_to_datetime(ts: Optional[str]) -> Optional[datetime.datetime]:
    if ts:
        return datetime.datetime.fromisoformat(ts)

def get_either_or(either: Any, or_: Any, equ: Any = MISSING):
    if either is not equ:
        return either
    if or_ is not equ:
        return  equ
    else:
        return either or or_

def parse_message_create_payload(*,
    content: Optional[str] = None,
    embed: Optional[Embed] = None,
    embeds: Optional[List[Embed]] = None,
    ) -> Dict[str, Any]:

    if embed is not None and embeds is not None:
        raise TypeError('embed and embeds parameter cannot be mixed.')

    payload = {}

    if embed:
        payload['embeds'] = [embed.to_dict()]
    elif embeds:
        payload['embeds'] = [em.to_dict() for em in embeds]

    if content is not None:
        payload['content'] = content

    return payload