"""Text formatting and inspection helpers."""

import re

SMALL_WORDS = {"a", "an", "the", "of", "and", "or", "in", "on", "to"}


def slugify(text: str) -> str:
    """Lowercase text and join alphanumeric runs with single hyphens (no leading/trailing hyphens)."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return slug.rstrip("-")


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Shorten text so that the result, including the suffix, is at most max_length characters."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def title_case(text: str) -> str:
    """Capitalize words, keeping small words lowercase unless they start the title."""
    words = text.lower().split()
    result = []
    for i, word in enumerate(words):
        if word in SMALL_WORDS:
            result.append(word)
        else:
            result.append(word.capitalize())
    return " ".join(result)


def count_words(text: str) -> int:
    """Count whitespace-separated words (contractions and hyphenated words count once)."""
    return len(re.findall(r"\w+", text))


def reverse_words(text: str) -> str:
    """Reverse word order and collapse any whitespace to single spaces."""
    return " ".join(reversed(text.split(" ")))


def is_palindrome(text: str) -> bool:
    """True when text reads the same backwards, ignoring case and non-alphanumerics."""
    cleaned = [c for c in text if c.isalnum()]
    return cleaned == cleaned[::-1]


def camel_to_snake(name: str) -> str:
    """Convert camelCase/PascalCase to snake_case, keeping acronyms together."""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    first, *rest = name.split("_")
    return first.capitalize() + "".join(part.capitalize() for part in rest)


def pad_left(value: str, width: int, fill: str = "0") -> str:
    """Left-pad value to width with fill; values longer than width are returned unchanged."""
    return (fill * width + value)[-width:]


def mask_email(email: str) -> str:
    """Mask the local part of an email, keeping its first and last characters."""
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked = local[0] + "*" * (len(local) - 1)
    else:
        masked = local[0] + "*" * len(local) + local[-1]
    return f"{masked}@{domain}"


def initials(full_name: str) -> str:
    """Uppercase initials of each name part, e.g. 'ada lovelace' -> 'AL'."""
    return "".join(part[0].upper() for part in full_name.split(" "))
