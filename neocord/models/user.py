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
from typing import Optional, TYPE_CHECKING, Union

from neocord.models.base import DiscordModel
from neocord.models.asset import CDNAsset
from neocord.dataclasses.flags.user import UserFlags
from neocord.dataclasses.color import Color
from neocord.internal.missing import MISSING
from neocord.internal import helpers

if TYPE_CHECKING:
    from neocord.api.state import State
    from neocord.typings.user import User as UserPayload

class BaseUser(DiscordModel):

    if TYPE_CHECKING:
        username: str
        discriminator: str
        bot: bool
        system: bool
        _avatar: Optional[str]
        _banner: Optional[str]
        _accent_color: Optional[int]
        _public_flags: int

    def __init__(self, data: UserPayload, state: State):
        self._state = state
        self._update(data)

    def _update(self, data: UserPayload) -> None:
        self.name = data["username"]
        self.id = int(data["id"])
        self.discriminator = data["discriminator"]
        self.bot = data.get("bot", False)
        self.system = data.get("system", False)

        self._avatar = data.get("avatar", None)
        self._banner = data.get("banner", None)
        self._accent_color = data.get("accent_color")
        self._public_flags = data.get("public_flags", 0)

    @property
    def public_flags(self) -> UserFlags:
        """:class:`UserFlags: Returns the public flags of a user."""
        return UserFlags(value=self._public_flags)

    @property
    def avatar(self) -> Optional[CDNAsset]:
        """:class:`CDNAsset`: Returns the CDN asset for user avatar."""
        if self._avatar is not None:
            return CDNAsset(
                key=self._avatar,
                path=f'/avatars/{self.id}',
                state=self._state,
            )

    @property
    def banner(self) -> Optional[CDNAsset]:
        """:class:`CDNAsset`: Returns the CDN asset for user banner."""
        if self._banner is not None:
            return CDNAsset(
                key=self._banner,
                path=f'/banners/{self.id}',
                state=self._state,
            )

    @property
    def accent_color(self) -> Color:
        """:class:`Color`: Returns the color representation of the user's banner color."""
        if self._accent_color is None:
            return Color(0)

        return Color(self._accent_color)

    # alias
    accent_colour = accent_color

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} id={self.id} name={self.name} \
                 discriminator={self.discriminator} bot={self.bot}>'
        )

    def __str__(self):
        return f'{self.name}#{self.discriminator}'

class ClientUser(BaseUser):
    """
    Represents a Discord User for the connected client. The most common
    way of accessing this is by :attr:`neocord.Client.user` attribute.

    Attributes
    ----------
    name: :class:`str`
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

    async def edit(self, *,
        name: Optional[str] = MISSING,
        avatar: Optional[str] = MISSING,
        ):
        """
        Edits the client user.

        All parameters in this method are optional. This method returns None and
        updates the instance in-place with new data.

        Parameters
        ----------
        name: :class:`str`
            The new name of the user.
        avatar: Optional[:class:`bytes`]
            The bytes like object that represents the new avatar's image data.
            None can be passed to remove the avatar.
        """
        payload = {}

        if name is not MISSING:
            payload['username'] = name
        if avatar is not MISSING:
            payload['avatar'] = helpers.get_image_data(avatar) # type: ignore

        if payload:
            data = await self.state.http.edit_client_user(payload=payload)
            self._update(data)


class User(BaseUser):
    """
    Represents a discord user entity.

    Attributes
    ----------
    name: :class:`str`
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