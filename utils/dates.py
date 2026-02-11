from datetime import datetime


def format_date(value: str | None) -> str:
    """Format a date/datetime string into dd-mm-yyyy. Returns '-' if None/empty."""
    if not value:
        return "-"

    # Try parsing common formats
    fmts = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
    ]
    for f in fmts:
        try:
            dt = datetime.strptime(value, f)
            return dt.strftime("%d-%m-%Y")
        except Exception:
            continue

    # Fallback: try fromisoformat
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d-%m-%Y")
    except Exception:
        pass

    # If nothing works, try to extract date part
    try:
        parts = value.split(" ")[0].split("T")[0].split("-")
        if len(parts) == 3:
            return "{}-{}-{}".format(parts[2], parts[1], parts[0])
        return value
    except Exception:
        return value
