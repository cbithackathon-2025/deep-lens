import pytest
from modules.pollution.sar_slick_detector import (
    calculate_damping_ratio_db,
    classify_slick_contrast,
    compute_otsu_threshold
)

def test_damping_ratio_known_values():
    # 10x ratio -> 10 dB
    assert calculate_damping_ratio_db(100.0, 10.0) == 10.0
    # 2x ratio -> ~3.01 dB
    assert calculate_damping_ratio_db(2.0, 1.0) == 3.01
    # Equal -> 0 dB
    assert calculate_damping_ratio_db(5.0, 5.0) == 0.0

def test_damping_ratio_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_damping_ratio_db(-10.0, 5.0)
    with pytest.raises(ValueError):
        calculate_damping_ratio_db(10.0, 0.0)

def test_classify_slick_contrast():
    assert classify_slick_contrast(2.5) == "WEAK_DAMPING"
    assert classify_slick_contrast(5.2) == "MODERATE_DAMPING"
    assert classify_slick_contrast(11.8) == "SEVERE_DAMPING"

def test_otsu_threshold_bimodal_distribution():
    # Two distinct clusters around 10.0 (slick) and 80.0 (clean water)
    data = [9.0, 10.0, 11.0, 10.5, 9.5] * 20 + [78.0, 80.0, 82.0, 81.0, 79.0] * 20
    thresh = compute_otsu_threshold(data)
    assert 11.0 < thresh < 78.0
