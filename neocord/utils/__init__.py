"""
neocord.utils
~~~~~~~~~~~~~

Utilities for Neocord.
"""
from __future__ import annotations
from typing import Sequence, Any, Optional, List

def _get_items_with_traits(seq, traits, return_first: bool = False) -> Union[List[Any], Any]:
    matching = []

    for item in seq:
        try:
            matches_traits = all([getattr(item, key) == value for key, value in traits.items()])
        except AttributeError:
            continue
        else:
            if not matches_traits:
                continue

            if return_first:
                return item

            matching.append(item)

    return matching

def get_one(sequence: Sequence[Any], **traits: Any) -> Any:
    """Gets the first item from provided sequence that matches the provided traits.

    For example to get a text channel from a guild with name general::

        channel = neocord.utils.get(guild.channels, name='general', type=neocord.ChannelType.TEXT)

    This function returns None if no item in sequence matches the provided
    traits.

    Parameters
    ----------
    sequence:
        The sequence to lookup item from.
    **traits:
        The keyword arguments representing the traits of item.

    Returns
    -------
    The item with matching traits; if found.
    """
    return _get_items_with_traits(sequence, traits, return_first=True)

def get_all(sequence: Sequence[Any], **traits: Any) -> List[Any]:
    """Gets all items from provided sequence that matches the provided traits.

    For example to get all members named "Foobar" from a guild::

        members_named_foobar = neocord.utils.get(guild.members, name='Foobar')

    This function returns an empty list if no item in sequence matches the provided
    traits.

    Parameters
    ----------
    sequence:
        The sequence to lookup items from.
    **traits:
        The keyword arguments representing the traits of item.

    Returns
    -------
    :class:`list`:
        The list of items with matching traits.
    """
    return _get_items_with_traits(sequence, traits)