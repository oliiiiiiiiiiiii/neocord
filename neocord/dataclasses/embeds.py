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
from typing import Any, Optional, List, Set, TYPE_CHECKING, Text

if TYPE_CHECKING:
    import datetime

__all__ = (
    'Embed',
    'EmbedField',
    'EmbedAuthor',
    'EmbedFooter',
    'EmbedImage',
    'EmbedThumbnail',
)

class Embed:
    """
    A class that provides an easy to handle interface for creating and managing
    rich message embeds.

    This class implements some helpers that make management of embeds easy.
    """
    if TYPE_CHECKING:
        timestamp: Optional[datetime.datetime]
        footer: Optional[EmbedFooter]
        author: Optional[EmbedAuthor]
        fields: List[EmbedField]

    def __init__(self, **options: Any) -> None:
        self.title = options.get('title')
        self.description = options.get('description')
        self.url = options.get('url')
        self.timestamp = options.get('timestamp')

        self.color = options.get('color')
        self.colour = options.get('colour')

        self.footer = None
        self.image = None
        self.thumbnail = None
        self.video = None
        self.provider = None
        self.author = None
        self.fields = []

        self.type = 'rich'

    def to_dict(self):
        ret = {}
        if self.title is not None:
            ret['title'] = self.title
        if self.description is not None:
            ret['description'] = self.description
        if self.url is not None:
            ret['url'] = self.url
        if self.timestamp is not None:
            ret['timestamp'] = self.timestamp.isoformat()
        if self.color is not None:
            ret['color'] = int(self.color)
        if self.colour is not None:
            ret['color'] = int(self.colour)
        if self.footer is not None:
            ret['footer'] = self.footer.to_dict()
        if self.author is not None:
            ret['author'] = self.author.to_dict()
        if self.fields:
            ret['fields'] = []
            for field in self.fields:
                ret['fields'].append(field.to_dict())

        return ret

    @classmethod
    def from_dict(cls, data: Any) -> Embed:
        # create an empty embed and populate it by data we have.
        embed = cls()

        objects = {
            'fields': EmbedField,
            'image': EmbedImage,
            'thumbnail': EmbedThumbnail,
            'footer': EmbedFooter,
            'author': EmbedAuthor,
        }

        for key in data:
            item = data[key]
            if key in objects:
                obj = objects[key]
                if isinstance(item, list):
                    setattr(embed, key, [obj(**i) for i in item]) # type: ignore
                else:
                    setattr(embed, key, obj(**item))
            else:
                setattr(embed, key, data[key])

        return embed

class BaseEmbedComponent:
    VALID_KEYS: Set[str] = set()

    def __init__(self, **options: Any) -> None:
        invalid = options.keys() - self.VALID_KEYS
        if invalid:
            raise TypeError(f'invalid options were passed: {invalid}')

        self.__dict__.update(options)

    def to_dict(self) -> dict:
        return self.__dict__

class EmbedAuthor(BaseEmbedComponent):
    """
    Represents the author of an embed. The author on all platforms
    is usually rendered on top of embed's title.

    Attributes
    ----------
    name: :class:`str`
        The name of the author.
    url: :class:`str`
        The hyperlink of the author.
    icon_url: :class:`str`
        The url to the image used as author's icon.
    proxy_icon_url: :class:`str`
        The proxied URL to the image used as author's icon.
    """
    VALID_KEYS = ('name', 'url', 'icon_url', 'proxy_icon_url')


class EmbedFooter(BaseEmbedComponent):
    """
    Represents the footer of an embed.

    Attributes
    ----------
    text: :class:`str`
        The text shown on the footer.
    icon_url: :class:`str`
        The url to the image used as footer's icon.
    proxy_icon_url: :class:`str`
        The proxied URL to the image used as footer's icon.
    """
    if TYPE_CHECKING:
        text: str
        icon_url: str
        proxy_icon_url: str

    VALID_KEYS = ('text', 'icon_url', 'proxy_icon_url')


class EmbedField(BaseEmbedComponent):
    """
    Represents a field of an embed.

    Attributes
    ----------
    name: :class:`str`
        The name of field.
    value: :class:`str`
        The value of field.
    inline: :class:`bool`
        Whether the field should line with last field.
    """
    if TYPE_CHECKING:
        name: str
        value: str
        inline: bool

    VALID_KEYS = ('name', 'value', 'inline')

class BaseEmbedAsset(BaseEmbedComponent):
    if TYPE_CHECKING:
        url: str
        proxy_url: str
        height: int
        width: int

    VALID_KEYS = ('url', 'proxy_url', 'height', 'width')

    def to_dict(self) -> dict:
        ret = super().to_dict()

        ret.pop('width', None)
        ret.pop('height', None)
        ret.pop('proxy_url', None)

        return ret

class EmbedThumbnail(BaseEmbedAsset):
    """
    Represents a thumbnail of an embed.

    Attributes
    ----------
    url: :class:`str`
        The image url of thumbnail.
    icon_url: :class:`str`
        The proxied image url of thumbnail.
    height: :class:`int`
        The height of thumbnail. This field cannot be set by bots.
    width: :class:`int`
        The width of embed. This field cannot be set by bots.
    """

class EmbedImage(BaseEmbedAsset):
    """
    Represents a image of an embed.

    Attributes
    ----------
    url: :class:`str`
        The image url.
    icon_url: :class:`str`
        The proxied image url.
    height: :class:`int`
        The height of image. This field cannot be set by bots.
    width: :class:`int`
        The width of image. This field cannot be set by bots.
    """



