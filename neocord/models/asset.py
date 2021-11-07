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
from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from neocord.api.state import State

class CDNAsset:
    """
    Represents an asset from Discord's CDN like icons, avatars etc.

    Attributes
    ----------
    url: :class:`str`
        The URL of the asset.
    key: :class:`str`
        The identification unique key of the asset.
    animated: :class:`bool`
        Whether this asset is animated.
    """
    BASE_CDN_URL: ClassVar[str] = 'https://cdn.discordapp.com'

    __slots__ = ('key', '_path', '_state')

    def __init__(self, key: str, path: str, state: State):
        self.key = key
        self._path = path
        self._state = state

    def __repr__(self):
        return f'<CDNAsset animated={self.animated} url={self.url}>'

    @property
    def url(self) -> str:
        """Returns the access URL of this asset."""
        fmt = 'gif' if self.animated else 'png'
        return f'{self.BASE_CDN_URL}{self._path}/{self.key}.{fmt}'

    @property
    def animated(self) -> bool:
        """Returns a boolean representing, Whether this asset is animated or not."""
        # the hashes of animated assets start with 'a_'.
        return self.key.startswith('a_')

    def with_size(self, size: int) -> str:
        """
        Returns the URL of asset with provided size.

        Parameters
        ----------
        size: :class:`int`
            The size of asset, size can be power of 2 between 16 to 4096.

        Raises
        ------
        ValueError:
            The provided size is not valid.

        Returns
        -------
        :class:`str`
            The URL with desired size attached.
        """
        if not size & (size - 1) and 4096 >= size >= 16:
            raise ValueError('size parameter must be a power of 2 between 16 and 4096')

        return self.url + f'?size={size}'
