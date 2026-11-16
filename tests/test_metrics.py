from qrt.metrics import weighted_accuracy


def test_weighted_accuracy_weights_by_magnitude():
    y = [0.10, -0.01]
    assert weighted_accuracy(y, [1, 1]) == 0.10 / 0.11
    assert weighted_accuracy(y, [1, -1]) == 1.0
