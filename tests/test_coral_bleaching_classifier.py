from modules.ecosystems.coral_bleaching import (
    classify_thermal_stress,
    calculate_degree_heating_weeks
)

def test_no_stress():
    res = classify_thermal_stress(sst_anomaly_celsius=-0.5, dhw_degree_weeks=0.0)
    assert res["alert_level"] == 0
    assert res["status"] == "NO_STRESS"
    assert res["risk"] == "none"

def test_bleaching_watch():
    res = classify_thermal_stress(sst_anomaly_celsius=0.8, dhw_degree_weeks=0.5)
    assert res["alert_level"] == 1
    assert res["status"] == "BLEACHING_WATCH"
    assert res["risk"] == "low"

def test_bleaching_warning():
    res = classify_thermal_stress(sst_anomaly_celsius=1.2, dhw_degree_weeks=2.5)
    assert res["alert_level"] == 2
    assert res["status"] == "BLEACHING_WARNING"
    assert res["risk"] == "medium"

def test_alert_level_1():
    res = classify_thermal_stress(sst_anomaly_celsius=1.5, dhw_degree_weeks=5.2)
    assert res["alert_level"] == 3
    assert res["status"] == "ALERT_LEVEL_1"
    assert res["risk"] == "high"

def test_alert_level_2_severe():
    res = classify_thermal_stress(sst_anomaly_celsius=2.1, dhw_degree_weeks=10.4)
    assert res["alert_level"] == 4
    assert res["status"] == "ALERT_LEVEL_2"
    assert res["risk"] == "critical"

def test_calculate_degree_heating_weeks():
    # 7 days with HotSpot = 1.0 deg C -> exactly 1.0 DHW
    daily_values = [1.0] * 7 + [0.5] * 10  # 0.5 is ignored as < 1.0
    dhw = calculate_degree_heating_weeks(daily_values)
    assert dhw == 1.0
