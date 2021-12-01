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
from typing import TYPE_CHECKING, List

from neocord.models.base import DiscordModel
from neocord.models.asset import CDNAsset

if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.typings.stickers import (
        Sticker as StickerPayload,
        StickerPack as StickerPackPayload,
    )


__all__ = (
    'Sticker',
    'StickerFormatType',
    'BaseSticker',
    'StandardSticker',
    'StickerPack'
)

class StickerType:
    STANDARD = 1
    GUILD = 2

class StickerFormatType:
    PNG = 1
    APNG = 2
    LOTTIE = 3

class BaseSticker(DiscordModel):
    __slots__ = ('_state', 'id', 'name', 'description', 'type', 'format_type', '_tags')

    def __init__(self, data: StickerPayload, state: State):
        self._state = state
        self._update(data)

    def _update(self, data: StickerPayload):
        self.id = int(data['id'])
        self.name = data.get('name')
        self.description = data.get('description')
        self.type = data.get('type')
        self.format_type = data.get('format_type')

        self._tags = data.get('tags')

    @property
    def tags(self) -> List[str]:
        """
        List[:class:`str`]: Returns a list of autocomplete tags for this sticker.
        """
        return [tag.strip() for tag in self._tags.split(',')]

    @property
    def url(self) -> str:
        """
        :class:`str`: Returns the CDN URL of this sticker.
        """
        # json represents lottie sticker.
        fmt = (
            'png' if self.format_type in [StickerFormatType.PNG, StickerFormatType.APNG]
            else 'json'
            )

        return f'{CDNAsset.BASE_URL}/stickers/{self.id}.{fmt}'

class StickerPack(DiscordModel):
    """Represents a standard sticker pack.

    Attributes
    ----------
    id: :class:`int`
        The ID of this sticker pack.
    stickers: List[:class:`StandardSticker`]
        The list of standard stickers that are available in this
        sticker pack.
    name: :class:`str`
        The name of this sticker pack.
    sku_id: :class:`int`
        The SKU ID of this sticker pack.
    cover_sticker_id: Optional[:class:`int`]
        The ID of sticker that is shown on sticker pack as an icon. This may be
        None in some cases.
    description: :class:`str`
        The description of sticker pack.
    banner_asset_id: :class:`int`
        The ID of asset that is shown as banner for this pack.
    """
    __slots__ = (
        '_state', 'id', 'stickers', 'name', 'description', 'banner_asset_id',
        'cover_sticker_id', 'sku_id'
        )

    def __init__(self, data: StickerPackPayload, state: State):
        self._state = state
        self._update(data)

    def _update(self, data: StickerPackPayload):
        self.id = int(data['id'])
        self.stickers = [StandardSticker(sticker, state=self._state) for sticker in data.get('stickers', [])]
        self.name = data.get('name')
        self.description = data.get('description')

        self.banner_asset_id = helpers.get_snowflake(data, 'banner_asset_id')
        self.cover_sticker_id = helpers.get_snowflake(data, 'cover_sticker_id')
        self.sku_id = helpers.get_snowflake(data, 'sku_id')

    @property
    def cover_sticker(self) -> StandardSticker:
        """
        :class:`StandardSticker`: The sticker that is shown as icon of this pack.
        """
        for sticker in self.stickers:
            if sticker.id == self.cover_sticker_id:
                return sticker

    def banner_asset_url(self, size: int = 512, format: str = 'png') -> str:
        """Returns the URL of the banner asset that this pack has.

        Parameters
        ----------
        size: :class:`int`
            The size that should be returned. Must be a power of 2 between 16 to 4096.
            Defaults to 512.
        format: :class:`str`
            The format to return URL as. Valid formats are:

            * ``png``
            * ``jpg`` or ``jpeg``
            * ``webp``

            Defaults to PNG.
        """
        valid_fmts = ['png', 'jpg', 'jpeg', 'webp']
        format = format.lower()

        if not format in valid_fmts:
            raise ValueError('Invalid format was provided. Must be either of PNG, JPG, JPEG or WEBP.')

        if not size & (size - 1) and 4096 >= size >= 16:
            raise ValueError('size parameter must be a power of 2 between 16 and 4096')


        return f'{CDNAsset.BASE_URL}/app-assets/710982414301790216/store/{self.banner_asset_id}.{format}?size={size}'

class StandardSticker(BaseSticker):
    """Represents a "standard" Discord sticker that can be used by Nitro users.

    Attributes
    ----------
    id: :class:`int`
        The sticker ID.
    name: :class:`str`
        The name of sticker.
    description: :class:`str`
        The description of sticker.
    type: :class:`StickerType`
        The type of sticker. Always :attr:`~StickerType.STANDARD` in this
        case.
    format_type: :class:`StickerFormatType`
        The format type of sticker.
    pack_id: :class:`int`
        The ID of pack that this sticker belongs to.
    sort_value: :class:`int`
        The sorting position in the sticker pack that this sticker belongs to.
    """
    __slots__ = ('pack_id', 'sort_value')

    pack_id: int
    sort_value: int

    def _update(self, data: StickerPayload):
        super()._update(data)

        self.pack_id = helpers.get_snowflake() # type: ignore

        try:
            sort_value = int(data['sort_value'])
        except KeyError:
            self.sort_value = 0
        else:
            self.sort_value = sort_value
