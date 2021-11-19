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
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from neocord.models.base import DiscordModel

class AllowedMentions:
    """
    A dataclass that handles the logic for allowing and disallowing mentions in
    a :class:`Message`.

    Creating an instance without any parameters creates the object with all
    options set to True.

    Parameters
    ----------
    mention_users: :class:`bool`
        Whether to enable user mentions in messages.
    mention_roles: :class:`bool`
        Whether to enable role mentions in messages.
    mention_everyone_here: :class:`bool`
        Whether to enable @everyone and @here mentions in messages.
    mention_replied_user: :class:`bool`
        Whether to mention the user whose message is being replied by message.

    Attributes
    ----------
    roles: List[:class:`int`]
        List of roles IDs that will be mentioned by message.
    users: List[:class:`int`]
        List of users IDs that will be mentioned by message.
    """
    def __init__(self, *,
        mention_users: bool = True,
        mention_roles: bool = True,
        mention_everyone_here: bool = True,
        mention_replied_user: bool = True
        ):
        self.mention_users = mention_users
        self.mention_roles = mention_roles
        self.mention_everyone_here = mention_everyone_here
        self.mention_replied_user = mention_replied_user

        self.roles: List[int] = []
        self.users: List[int] = []

    def add_role(self, role: int):
        """Adds a specific role that will be mentioned in message.

        Parameters
        ----------
        role: :class:`int`
            The role ID that will be mentioned.
        """
        return self.roles.append(role)

    def add_user(self, user: int):
        """Adds a specific user that will be mentioned in message.

        Parameters
        ----------
        user: :class:`int`
            The user ID that will be mentioned.
        """
        return self.users.append(user)

    def remove_role(self, role: int):
        """Removes a specific role from list of roles that will be mentioned.

        If provided role is not found, This function would not raise any
        error.

        Parameters
        ----------
        role: :class:`int`
            The role ID to remove.
        """
        try:
            self.roles.remove(role)
        except:
            return

    def remove_user(self, user: int):
        """Removes a specific user from list of roles that will be mentioned.

        If provided user is not found, This function would not raise any
        error.

        Parameters
        ----------
        user: :class:`int`
            The user ID to remove.
        """
        try:
            self.users.remove(user)
        except:
            return


    def _get_parsed(self):
        ret = []
        if self.mention_users:
            ret.append('users')
        if self.mention_roles:
            ret.append('roles')
        if self.mention_everyone_here:
            ret.append('everyone')

        return ret

    def to_dict(self):
        return {
            'parse': self._get_parsed(),
            'roles': self.roles,
            'users': self.users,
            'replied_user': self.mention_replied_user
        }

    @classmethod
    def none(cls) -> AllowedMentions:
        """
        Creates an allowed mentions object with all options disabled.

        Returns
        -------
        :class:`AllowedMentions`
        """
        return cls()