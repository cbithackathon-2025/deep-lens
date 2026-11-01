"""
Marine pollution analysis and Sentinel-1 SAR oil slick processing.
"""
from modules.pollution.sar_slick_detector import (
    calculate_damping_ratio_db,
    classify_slick_contrast,
    compute_otsu_threshold
)

__all__ = [
    "calculate_damping_ratio_db",
    "classify_slick_contrast",
    "compute_otsu_threshold"
]
