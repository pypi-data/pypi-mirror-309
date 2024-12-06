"""Model quality test."""

from mlops.modeling.train import main


def test_model_accuracy():

    accuracy = main()
    assert accuracy > 0.8
