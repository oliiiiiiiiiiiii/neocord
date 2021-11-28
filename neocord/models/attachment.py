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
from typing import TYPE_CHECKING

from neocord.models.base import DiscordModel
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.typings.message import Attachment as AttachmentPayload
    from neocord.api.state import State

class Attachment(DiscordModel):
    """Represents an attachment on a message.

    Attributes
    ----------
    id: :class:`int`
        The ID of attachment.
    filename: :class:`str`
        The name of file that this attachment has.
    description: Optional[:class:`str`]
        The description of attachment.
    content_type: Optional[:class:`str`]
        The content type of this attachment.
    size: :class:`int`
        The size of attachment in bytes.
    url: :class:`str`
        The URL of attachment.
    proxy_url: Optional[:class:`str`]
        The proxied URL of attachment.
    height: Optional[:class:`int`]
        The height of attachment. Only valid for images.
    width: Optional[:class:`int`]
        The width of attachment. Only valid for images.
    ephemeral: :class:`bool`
        Whether this attachment is sent ephemerally as an interaction response.
    """
    __slots__ = (
        '_state', 'id', 'filename', 'description', 'size', 'content_type', 'url',
        'proxy_url', 'height', 'width', 'ephemeral',
    )

    def __init__(self, data: AttachmentPayload, state: State):
        self._state = state
        self._update(data)

    def _update(self, data: AttachmentPayload):
        self.id = helpers.get_snowflake(data, 'id') # type: ignore
        self.filename = data.get('filename')
        self.description = data.get('description')
        self.size = helpers.int_or_none(data, 'size')
        self.content_type = data.get('content_type')
        self.url = data.get('url')
        self.proxy_url = data.get('proxy_url')
        self.height = helpers.int_or_none(data, 'height')
        self.width = helpers.int_or_none(data, 'width')
        self.ephemeral = data.get('ephemeral', False)