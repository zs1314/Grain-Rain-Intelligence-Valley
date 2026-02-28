"""Core rainfall analytics logic."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean, median


@dataclass(frozen=True)
class RainfallReport:
    """Structured summary for rainfall analytics output."""

    count: int
    total: float
    mean: float
    median: float
    minimum: float
    maximum: float
    trend: str
    risk: str

    def to_dict(self) -> dict[str, float | int | str]:
        """Convert report to a plain dictionary."""
        return asdict(self)


def _validate_samples(samples: list[float]) -> None:
    if not samples:
        raise ValueError("samples cannot be empty")
    if any(value < 0 for value in samples):
        raise ValueError("rainfall samples must be non-negative")


def _detect_trend(samples: list[float], window: int = 3) -> str:
    """Detect trend by comparing the average of head and tail windows."""
    if len(samples) < window * 2:
        return "stable"

    head = mean(samples[:window])
    tail = mean(samples[-window:])
    delta = tail - head

    threshold = max(1.0, 0.1 * max(head, tail, 1.0))
    if delta > threshold:
        return "increasing"
    if delta < -threshold:
        return "decreasing"
    return "stable"


def _risk_from_stats(avg: float, trend: str) -> str:
    """Map average rainfall and trend into a risk category."""
    if avg >= 25 or (avg >= 18 and trend == "increasing"):
        return "high"
    if avg >= 10 or trend == "increasing":
        return "medium"
    return "low"


def analyze_rainfall(samples: list[float]) -> RainfallReport:
    """Compute rainfall statistics and business-oriented indicators."""
    _validate_samples(samples)

    avg = mean(samples)
    trend = _detect_trend(samples)
    risk = _risk_from_stats(avg, trend)

    return RainfallReport(
        count=len(samples),
        total=round(sum(samples), 2),
        mean=round(avg, 2),
        median=round(median(samples), 2),
        minimum=round(min(samples), 2),
        maximum=round(max(samples), 2),
        trend=trend,
        risk=risk,
    )


def suggest_action(report: RainfallReport) -> str:
    """Provide a recommendation based on risk level."""
    if report.risk == "high":
        return "建议立即检查排涝设施并减少易涝地块灌溉。"
    if report.risk == "medium":
        return "建议优化排水并关注短期强降雨预警。"
    return "降雨风险较低，保持常规田间管理即可。"
