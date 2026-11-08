import itertools

from gain_of_thrones.album import shifted_targets


def test_loudest_lands_at_target_and_differences_survive():
    L = {"a": -11.9, "b": -12.07, "c": -10.37, "d": -14.234, "e": -10.77}
    T = shifted_targets(L, -9.5)
    assert T["c"] == -9.5
    for x, y in itertools.combinations(L, 2):
        assert abs((T[x] - T[y]) - (L[x] - L[y])) <= 0.1 + 1e-9  # within the 0.1 LU rounding


def test_reproduces_freaks_targets():
    # Original loudness and targets from the prototype's targets.tsv for the Freaks EP.
    L = {"01": -11.90, "02": -12.07, "03": -11.64, "04": -10.90, "05": -10.37, "06": -10.77}
    assert shifted_targets(L, -9.5) == {"01": -11.0, "02": -11.2, "03": -10.8, "04": -10.0, "05": -9.5, "06": -9.9}
