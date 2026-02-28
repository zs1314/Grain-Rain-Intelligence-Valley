from grain_rain_intelligence_valley.analytics import analyze_rainfall, suggest_action


def test_analyze_rainfall_basic_stats() -> None:
    report = analyze_rainfall([12.0, 10.0, 14.0, 16.0, 18.0, 20.0])

    assert report.count == 6
    assert report.total == 90.0
    assert report.mean == 15.0
    assert report.median == 15.0
    assert report.minimum == 10.0
    assert report.maximum == 20.0
    assert report.trend == "increasing"
    assert report.risk == "medium"


def test_analyze_rainfall_raises_on_empty() -> None:
    try:
        analyze_rainfall([])
    except ValueError as exc:
        assert "cannot be empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty samples")


def test_suggest_action_high_risk() -> None:
    report = analyze_rainfall([30.0, 28.0, 31.0, 29.0, 32.0, 35.0])
    recommendation = suggest_action(report)

    assert report.risk == "high"
    assert "排涝" in recommendation
