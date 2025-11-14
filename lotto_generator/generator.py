import random
from dataclasses import dataclass
from typing import List


@dataclass
class Game:
    mains: List[int]
    bonus: int

    def format(self) -> str:
        """Return a human-readable representation, e.g. '2 8 11 21 28 30 + 32'."""
        mains_str = ", ".join(f"{n:02d}" for n in self.mains)
        return f"{mains_str}  +  {self.bonus:02d}"


def generate_single_game(
    max_number: int = 45,
    main_count: int = 6,
) -> Game:
    """
    Generate a single 6+1 game.

    :param max_number: Highest possible number (inclusive).
    :param main_count: How many main numbers.
    :return: Game with sorted main numbers and a bonus.
    """
    if main_count + 1 > max_number:
        raise ValueError("Not enough numbers in range to generate unique 6+1 game.")

    # Randomly pick 7 unique numbers from 1..max_number
    picks = random.sample(range(1, max_number + 1), main_count + 1)

    mains = sorted(picks[:main_count])
    bonus = picks[main_count]
    return Game(mains=mains, bonus=bonus)


def generate_games(
    count: int,
    max_number: int = 45,
    main_count: int = 6,
) -> List[Game]:
    """
    Generate multiple 6+1 games.

    :param count: How many games to generate.
    """
    if count <= 0:
        raise ValueError("count must be a positive integer.")
    return [generate_single_game(max_number, main_count) for _ in range(count)]
