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
from typing import Union

import os
import io

class File:
    """
    A class that aids in sending file attachments in messages.

    Example::

        file = neocord.File('path/to/file.png')
        await channel.send(file=file)

    .. note::
        This class is meant to be for one time use only and you should re-create the class
        everytime you want to send a file.

    Parameters
    ----------
    fp: Union[:class:`os.PathLike`, :class:`io.BufferedIOBase`]
        The path to the file or the file-like object opened in read or read-binary
        mode.
    name: :class:`str`
        The name of file.
    spoiler: :class:`bool`
        Whether this file is marked as spoiler.
    """
    def __init__(self,
        fp: Union[str, bytes, os.PathLike, io.BufferedIOBase],
        *,
        name: Optional[str] = None,
        spoiler: bool = False,
        description: Optional[str] = None,
    ):
        self.description = description
        if isinstance(fp, str):
            self._owner = True
            self.fp = open(fp, 'rb')
        else:
            self._owner = False
            self.fp = fp

        if name is None:
            if isinstance(fp, str):
                _, self.name = os.path.split(fp)
            else:
                try:
                    self.name = getattr(fp, "name")
                except AttributeError:
                    self.name = None

        self.spoiler = spoiler

    @property
    def proper_name(self) -> Optional[str]:
        if self.name is None:
            return None

        ret = self.name

        if self.spoiler:
            ret = 'SPOILER_' + ret

        return ret

    def close(self):
        if self._owner:
            self.fp.close()