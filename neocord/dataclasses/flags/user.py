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

from neocord.dataclasses.flags.base import BaseFlags, flag

class UserFlags(BaseFlags):
    """
    Represents the public flags of a user that appear on the user accounts.
    They are often referred as "badges" in the UI and are shown on the profile
    of users.

    This class is not generally created manually.

    Attributes
    ----------
    value: :class:`int`
        The raw integer value of flags.
    discord_employee: :class:`bool`
        Returns ``True`` if the user is a Discord staff.
    partnered_server_owner: :class:`bool`
        Returns ``True`` if the user has the partnered server owner badge.
    hypesquad_events: :class:`bool`
        Returns ``True`` if the user has Hypesquad events badge.
    bug_hunter_level_1: :class:`bool`
        Returns ``True`` if the user has the level one of bug hunter badge.
    house_bravery: :class:`bool`
        Returns ``True`` if the user's house is HypeSquad Bravery.
    house_brilliance: :class:`bool`
        Returns ``True`` if the user's house is HypeSquad Brilliance.
    house_balance: :class:`bool`
        Returns ``True`` if the user's house is HypeSquad Balance.
    early_supporter: :class:`bool`
        Returns ``True`` if the user has the "Early Supporter" badge.
    team_user: :class:`bool`
        Returns ``True`` if user is a "team user".
    bug_hunter_level_2: :class:`bool`
        Returns ``True`` if the has the user level two on bug hunter badge.
    verified_bot: :class:`bool`
        Returns ``True`` if the has the user is a verified bot.
    early_verified_bot_developer: :class:`bool`
        Returns ``True`` if the has the "Early Verified Bot Developer" badge.
    discord_certified_moderator: :class:`bool`
        Returns ``True`` if the has the "Certified Discord Moderator" badge.
    """

    def __init__(self, value: int):
        super().__init__(value=value)

    @flag
    def discord_employee(self) -> int:
        return 1 << 0

    @flag
    def partnered_server_owner(self) -> int:
        return 1 << 1

    @flag
    def hypesquad_events(self) -> int:
        return 1 << 2

    @flag
    def bug_hunter_level_1(self) -> int:
        return 1 << 3

    @flag
    def house_bravery(self) -> int:
        return 1 << 6

    @flag
    def house_brilliance(self) -> int:
        return 1 << 7

    @flag
    def house_balance(self) -> int:
        return 1 << 8

    @flag
    def early_supporter(self) -> int:
        return 1 << 9

    @flag
    def team_user(self) -> int:
        return 1 << 10

    @flag
    def bug_hunter_level_2(self) -> int:
        return 1 << 14

    @flag
    def verified_bot(self) -> int:
        return 1 << 16

    @flag
    def early_verified_bot_developer(self) -> int:
        return 1 << 17

    @flag
    def discord_certified_moderator(self) -> int:
        return 1 << 18