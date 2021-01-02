"""
In this module you will find functions to find hands which satisfy these three
properties:
    - they do not have a pair or better (unless it's only on the board).
    - they have three-to-a-flush using both hole cards,
    - they have three-to-a-straight using both hole cards, and
Expert poker players will recognise these as good candidates to use as bluffs.
"""
from itertools import chain

from pypokertools.pokertools import CANONICAL_HOLECARDS, ConflictingCards, five_cards
from pypokertools.properties.complex import is_3flush, is_3straight, is_onepair
from pypokertools.properties.hand import is_twopair_or_better as hand_is_twopair_or_better


@five_cards
def is_bluffcandidate(holecards, flop):
    """
    Returns a bool indicating whether our holecards are a good
    candidate for bluffing.

    Checks whether our hand has three properties:
        - not(pair-or-better) unless it's a pair on the board
        - three-to-a-flush using both hole cards
        - three-to-a-straight using both hole cards

    Example:
        >>> from src.pypokertools.pokertools import holecards, flop
        >>> assert holecards('Qd Jd') in get_bluffcandidates(flop('Kc 2d 2h'))
        >>> assert holecards('8s 7s') in get_bluffcandidates(flop('9c 4s 3d'))
        >>> assert holecards('Kc Jc') in get_bluffcandidates(flop('Qc 8d 3h'))
    """
    hand = tuple(chain(holecards, flop))
    return (
        not is_onepair(holecards, flop, exclude_board=True)
        and not hand_is_twopair_or_better(hand)
        and is_3flush(holecards, flop, required_holecards=2)
        and is_3straight(holecards, flop, required_holecards=2)
    )


def get_bluffcandidates(flop, range=None):
    for holecards in range or CANONICAL_HOLECARDS.values():
        try:
            if is_bluffcandidate(holecards, flop):
                yield holecards
        except ConflictingCards:
            pass
