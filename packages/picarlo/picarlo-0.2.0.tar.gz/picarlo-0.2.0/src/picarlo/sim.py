import random
from dataclasses import dataclass


def monte_carlo_pi(num_samples: int) -> float:
    in_circle_count = 0
    in_square_count = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            in_circle_count += 1
        in_square_count += 1
    return 4 * in_circle_count / in_square_count


@dataclass
class Config:
    """
    Configuration class for simulation parameters.

    Attributes:
        num_samples (int): The number of samples to be used in the simulation.
        Default is 10,000,000.
    """

    num_samples: int = 10000000


def hello() -> str:
    print("inside hello!")
    return "hello"


def goodbye() -> str:
    print("inside goodbye!")
    return "goodbye"


def stringify_the_float(value: float) -> str:
    return f"{int(value):d} dot {int((value-int(value))*100):d}"
