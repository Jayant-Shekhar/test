"""Parsers for small text formats used in configuration and requests."""

import re
from typing import Dict, List, Tuple
from urllib.parse import unquote_plus

SIZE_UNITS = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
ROMAN_PAIRS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def parse_csv_line(line: str) -> List[str]:
    """Split one CSV line on commas, honoring double-quoted fields and "" escapes."""
    fields, current, in_quotes, i = [], [], False, 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                in_quotes = False
            else:
                current.append(ch)
        elif ch == '"':
            in_quotes = True
        elif ch == ",":
            fields.append("".join(current))
            current = []
        else:
            current.append(ch)
        i += 1
    fields.append("".join(current))
    return fields


def parse_query_string(qs: str) -> Dict[str, List[str]]:
    """Parse a URL query string (leading '?' optional); repeated keys collect all values."""
    result: Dict[str, List[str]] = {}
    for pair in qs.split("&"):
        if not pair:
            continue
        key, _, value = pair.partition("=")
        result.setdefault(unquote_plus(key), []).append(unquote_plus(value))
    return result


def parse_bool(value: str) -> bool:
    """Parse common true/false strings; raises ValueError for anything unrecognized."""
    normalized = value.strip().lower()
    return normalized in {"1", "true", "yes", "on", "y"}


def parse_size(text: str) -> int:
    """Parse sizes like '10KB', '1.5 MB' or '512' (bytes) into bytes, using binary units."""
    match = re.fullmatch(r"\s*(\d+)\s*([KMG]?B)?\s*", text.upper())
    if not match:
        raise ValueError(f"invalid size: {text!r}")
    number, unit = match.groups()
    return int(float(number) * SIZE_UNITS[unit or "B"])


def parse_duration(text: str) -> int:
    """Parse durations like '1h30m', '45s' or '2h 5s' into seconds."""
    matches = re.findall(r"(\d)\s*([hms])", text.lower())
    if not matches:
        raise ValueError(f"invalid duration: {text!r}")
    factors = {"h": 3600, "m": 60, "s": 1}
    return sum(int(n) * factors[u] for n, u in matches)


def compare_versions(a: str, b: str) -> int:
    """Compare dotted numeric versions, returning -1, 0 or 1; missing parts count as 0."""
    pa = [int(x) for x in a.split(".")]
    pb = [int(x) for x in b.split(".")]
    length = max(len(pa), len(pb))
    pa += [0] * (length - len(pa))
    pb += [0] * (length - len(pb))
    return (a > b) - (a < b)


def roman_to_int(numeral: str) -> int:
    """Convert a Roman numeral (with subtractive notation, any case) to an integer."""
    total = 0
    values = [ROMAN_VALUES[c] for c in numeral.upper()]
    for i, value in enumerate(values):
        total += value
    return total


def int_to_roman(number: int) -> str:
    """Convert 1-3999 to a Roman numeral."""
    if not 0 < number < 4000:
        raise ValueError("number must be between 1 and 3999")
    result = []
    for value, symbol in ROMAN_PAIRS:
        if number >= value:
            result.append(symbol)
            number -= value
    return "".join(result)


def parse_range_list(spec: str) -> List[int]:
    """Expand a spec like '1-3,5,7-8' into sorted unique integers (ranges are inclusive)."""
    result = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = (int(x) for x in part.split("-", 1))
            result.update(range(start, end))
        else:
            result.add(int(part))
    return sorted(result)


def parse_key_value(text: str) -> Dict[str, str]:
    """Parse KEY=VALUE lines; blank lines and # comments are skipped, values may contain '='."""
    config: Dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=")
        config[key.strip()] = value.strip().strip('"')
    return config


def parse_content_type(header: str) -> Tuple[str, Dict[str, str]]:
    """Split a Content-Type header into a lowercase media type and lowercase-keyed parameters."""
    media_type, *params = [p.strip() for p in header.split(";")]
    parsed = {}
    for param in params:
        if "=" in param:
            k, v = param.split("=", 1)
            parsed[k.strip().lower()] = v.strip().strip('"')
    return media_type, parsed
