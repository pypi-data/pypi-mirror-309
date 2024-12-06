import pytest

from picarlo.sim import Config, stringify_the_float


def test_config():
    config = Config()
    assert config.num_samples == 10000000


@pytest.mark.parametrize(
    "input, expected",
    [
        (3.14159, "3 dot 14"),
        (122.71828, "122 dot 71"),
        (0.41421, "0 dot 41"),
        (1.0, "1 dot 0"),
        (1, "1 dot 0"),
        (0.1, "0 dot 10"),
        (0.09, "0 dot 9"),
    ],
)
def test_stringify_the_float(input, expected):
    assert stringify_the_float(input) == expected
