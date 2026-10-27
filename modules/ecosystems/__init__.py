"""
Marine ecosystems analytics and coral reef thermal stress monitoring.
"""
from modules.ecosystems.coral_bleaching import (
    classify_thermal_stress,
    calculate_degree_heating_weeks
)

__all__ = ["classify_thermal_stress", "calculate_degree_heating_weeks"]
