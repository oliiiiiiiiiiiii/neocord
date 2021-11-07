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
from typing import Optional, TYPE_CHECKING

from neocord.models.base import DiscordModel

if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.typings.user import User as UserPayload

__all__ = ()

class BaseUser(DiscordModel):

    if TYPE_CHECKING:
        username: str
        discriminator: str
        bot: bool
        system: bool
        _avatar: Optional[str]
        _banner: Optional[str]
        _accent_color: str
        _public_flags: int

    def __init__(self, data: UserPayload, state: State):
        self._state = state
        self._update(data)

    def _update(self, data: UserPayload) -> None:
        self.username = data["username"]
        self.id = int(data["id"])
        self.discriminator = data["discriminator"]
        self.bot = data.get("bot", False)
        self.system = data.get("system", False)

        self._avatar = data.get("avatar", None)
        self._banner = data.get("banner", None)
        self._accent_colour = data.get("accent_color", None)
        self._public_flags = data.get("public_flags", 0)


class ClientUser(BaseUser):
    """
    Represents a Discord User for the connected client. The most common
    way of accessing this is by :attr:`neocord.Client.user` attribute.

    Attributes
    ----------
    username: :class:`str`
        The username of user as shown in Discord.
    id: :class:`int`
        The user's unique snowflake ID.
    discriminator: :class:`str`
        The 4 digits discriminator of user.
    bot: :class:`bool`
        A boolean representing if the user is a bot or not, In case of this class
        this is usually ``True``
    system: :class:`bool`
        A boolean representing if the user is a system user i.e Official Discord System
        This is usually ``False``
    verified: :class:`bool`
        A boolean representing if the user has a verified email on the account.
    locale: Optional[:class:`str`]
        The language tag used to identify the language the user is using.
    mfa_enabled: :class:`bool`
        A boolean representing if the user has MFA enabled on the account.
    """
    if TYPE_CHECKING:
        verified: bool
        locale: Optional[str]
        mfa_enabled: bool

    def __init__(self, data: UserPayload, state: State):
        super().__init__(data, state)

    def _update(self, data: UserPayload):
        super()._update(data)

        # add additional non-common attributes
        self.verified = data.get('verified', False)
        self.locale = data.get('locale')
        self.mfa_enabled = data.get('mfa_enabled', False)

    # TODO: ClientUser.edit()

class User(BaseUser):
    """
    Represents a discord user entity.

    Attributes
    ----------
    username: :class:`str`
        The username of user as shown in Discord.
    id: :class:`int`
        The user's unique snowflake ID.
    discriminator: :class:`str`
        The 4 digits discriminator of user.
    bot: :class:`bool`
        A boolean representing if the user is a bot or not, In case of this class
        this is usually ``True``
    system: :class:`bool`
        A boolean representing if the user is a system user i.e Official Discord System
        This is usually ``False``
    """

    def __init__(self, data: UserPayload, state: State):
        super().__init__(data, state)