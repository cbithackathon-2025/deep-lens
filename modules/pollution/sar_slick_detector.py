import math
from typing import List, Dict, Any

def calculate_damping_ratio_db(background_sigma0: float, slick_sigma0: float) -> float:
    """
    Calculates the radar cross section damping ratio in decibels (dB):
    Delta sigma^0 = 10 * log10(sigma^0_bg / sigma^0_slick)
    Quantifies capillary wave dampening contrast of petroleum oil slicks in C-band SAR.
    """
    if background_sigma0 <= 0 or slick_sigma0 <= 0:
        raise ValueError("Radar backscatter intensity values must be positive and non-zero")
    if background_sigma0 < slick_sigma0:
        return 0.0

    ratio = background_sigma0 / slick_sigma0
    return round(10.0 * math.log10(ratio), 2)

def classify_slick_contrast(damping_ratio_db: float) -> str:
    """
    Classifies SAR backscatter contrast into standard marine pollution severity tiers.
    """
    if damping_ratio_db < 3.0:
        return "WEAK_DAMPING"
    elif damping_ratio_db < 7.0:
        return "MODERATE_DAMPING"
    else:
        return "SEVERE_DAMPING"

def compute_otsu_threshold(intensity_values: List[float], num_bins: int = 256) -> float:
    """
    Computes standard Otsu bimodal segmentation threshold separating
    dark slick pixels from brighter ocean background.
    """
    if not intensity_values:
        raise ValueError("intensity_values cannot be empty")

    min_val = min(intensity_values)
    max_val = max(intensity_values)
    if min_val == max_val:
        return min_val

    bin_width = (max_val - min_val) / num_bins
    histogram = [0] * num_bins

    for val in intensity_values:
        idx = min(int((val - min_val) / bin_width), num_bins - 1)
        histogram[idx] += 1

    total_pixels = len(intensity_values)
    sum_total = sum(i * histogram[i] for i in range(num_bins))

    weight_bg = 0
    sum_bg = 0
    max_variance = 0.0
    best_bins = [0]

    for t in range(num_bins):
        weight_bg += histogram[t]
        if weight_bg == 0:
            continue
        weight_fg = total_pixels - weight_bg
        if weight_fg == 0:
            break

        sum_bg += t * histogram[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_total - sum_bg) / weight_fg

        # Between-class variance
        variance = weight_bg * weight_fg * ((mean_bg - mean_fg) ** 2)
        if variance > max_variance:
            max_variance = variance
            best_bins = [t]
        elif variance == max_variance and max_variance > 0:
            best_bins.append(t)

    best_bin = sum(best_bins) / len(best_bins)
    return round(min_val + (best_bin * bin_width), 4)
