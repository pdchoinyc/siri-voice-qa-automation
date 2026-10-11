
import pytest

from run_performance_regression import calculate_regression_percent


def test_zero_baseline_raises_error():
    with pytest.raises(ValueError, match="Baseline must be greater than zero"):
        calculate_regression_percent(0, 0.5)


def test_negative_baseline_raises_error():
    with pytest.raises(ValueError, match="Baseline must be greater than zero"):
        calculate_regression_percent(-1, 0.5)


def test_performance_regression_calculation():
    result = calculate_regression_percent(0.5, 0.6)

    assert result == pytest.approx(20.0)


def test_performance_improvement_calculation():
    result = calculate_regression_percent(0.5, 0.4)

    assert result == pytest.approx(-20.0)
