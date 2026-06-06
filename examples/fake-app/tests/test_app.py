import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app import summarize_lane


def test_summarize_lane_normalizes_status():
    assert summarize_lane("demo", " COMPLETE ") == {
        "lane": "demo",
        "status": "complete",
    }


def test_summarize_lane_rejects_empty_lane():
    try:
        summarize_lane(" ", "planned")
    except ValueError as exc:
        assert "lane_name" in str(exc)
    else:
        raise AssertionError("expected ValueError")

