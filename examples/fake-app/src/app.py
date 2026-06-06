def summarize_lane(lane_name, status):
    """Return a compact lane summary for fake smoke tests."""
    clean_lane = str(lane_name).strip()
    clean_status = str(status).strip().lower()
    if not clean_lane:
        raise ValueError("lane_name is required")
    if clean_status not in {"planned", "running", "blocked", "complete"}:
        raise ValueError("unsupported status")
    return {"lane": clean_lane, "status": clean_status}

