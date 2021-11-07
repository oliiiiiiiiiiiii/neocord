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
from typing import Any, Optional, Set, Callable

# Inspired by Discord.py


class BaseFlags:
    VALID_FLAGS: Set[str]

    def __init__(self, value: Optional[int] = None, **flags: Any):
        invalid = set(flags.keys()) - set(self.VALID_FLAGS)
        if invalid:
            raise TypeError('Invalid keyword arguments {0} for {1}()'.format(invalid, self.__class__.__name__))

        if value:
            self._value = value
        else:
            self._value = 0
            for flag in flags:
                if flag:
                    self._value |= getattr(self.__class__, flag)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new: int) -> None:
        if not isinstance(new, int):
            raise TypeError('new value must be an int.')

        self._value = new

    @classmethod
    def from_value(cls, value: int):
        raise NotImplementedError

class flag:
    def __init__(self, func: Callable[[Any], int]):
        self.func = func
        self.value = func(None)

    def __get__(self, instance: Optional[BaseFlags], *_: Any):
        if not instance:
            return self.value

        return (self.value & instance.value)  == self.value

    def __set__(self, instance: Optional[BaseFlags], val: bool):
        if not instance:
            return

        exists = (self.value & instance.value)  == self.value

        if val is False and exists:
            instance._value -= self.value
        elif val is True and not exists:
            instance._value += self.value

    def __repr__(self):
        return f'<flag value={self.value}>'
