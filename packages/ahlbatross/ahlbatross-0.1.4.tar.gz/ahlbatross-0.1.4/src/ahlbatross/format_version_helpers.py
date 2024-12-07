"""
utility functions for parsing strings like 'FV2504' as 'April 2025'
"""

from typing import Tuple


def parse_formatversions(formatversion: str) -> Tuple[int, int]:
    """
    parse <formatversion> string (e.g., "FV2504") into year and month.
    """
    if not formatversion.startswith("FV") or len(formatversion) != 6:
        raise ValueError(f"invalid formatversion: {formatversion}")

    year = int(formatversion[2:4])
    month = int(formatversion[4:6])
    year = 2000 + year

    if not 1 <= month <= 12:
        raise ValueError(f"invalid formatversion: {formatversion}")

    return year, month
