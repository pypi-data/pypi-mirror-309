# iconv.py
import re
import codecs
from decimal import Decimal, ROUND_HALF_UP
from email.utils import parseaddr
from datetime import datetime
from typing import Optional, Union, Callable

# Convert data to SQL format for storage


def none(data: str) -> Optional[str]:
    """Converts various 'null' representations to None."""
    return None if data in ("", "null", "None", "@NULL") else data


def phone(data: str) -> Optional[str]:
    """Extracts a 10-digit phone number or returns None if invalid."""
    if data in ("None", None):
        return None
    cleaned_data = re.sub(r"[^0-9]", "", data)
    match = re.search(r"\d{10}$", cleaned_data)
    return match.group() if match else None


def day_of_week(data: str) -> Optional[int]:
    """Converts day of the week to an integer representation."""
    if not data:
        return None
    days = {
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6,
        "sunday": 7,
        "mon": 1,
        "tue": 2,
        "wed": 3,
        "thu": 4,
        "fri": 5,
        "sat": 6,
        "sun": 7,
    }
    return days.get(data.lower())


def date(data: str, fmt: str = "%Y-%m-%d") -> Optional[datetime.date]:
    """Parses a date string into a date object using the specified format."""
    try:
        return datetime.strptime(data, fmt).date()
    except (ValueError, TypeError):
        return None


def time(data: str, fmt: str = "%X") -> Optional[datetime.time]:
    """Parses a time string into a time object using the specified format."""
    try:
        return datetime.strptime(data, fmt).time()
    except (ValueError, TypeError):
        return None


def timestamp(data: str, fmt: str = "%c") -> Optional[datetime]:
    """Parses a timestamp string into a datetime object using the specified format."""
    try:
        return datetime.strptime(data, fmt)
    except (ValueError, TypeError):
        return None


def email(data: str) -> Optional[str]:
    """Validates and returns an email address if properly formatted."""
    if not data or data.lower() == "none":
        return None
    data = data.strip().lower()
    email_address = parseaddr(data)[1]
    if "@" in email_address and "." in email_address.split("@")[1]:
        return email_address
    raise ValueError("Invalid email format")


def integer(data: str) -> int:
    """Converts a string to an integer, removing non-numeric characters."""
    cleaned_data = re.sub(r"[^0-9\.-]", "", data)
    try:
        return int(float(cleaned_data))
    except ValueError:
        raise ValueError(f"Cannot convert {data} to integer.")


def boolean(data: Union[str, bool]) -> bool:
    """Converts various string representations to a boolean."""
    if isinstance(data, str) and data.lower() in ["false", "", "f", "off", "no"]:
        return False
    return bool(data)


def rot13(data: str) -> str:
    """Encodes a string using ROT13."""
    return codecs.encode(data, "rot13")


def pointer(data: Union[str, None]) -> Optional[int]:
    """Converts a pointer to an integer, or returns None for null values."""
    if data in ("@new", "", "@NULL", None):
        return None
    return int(data)


def money(data: str) -> Optional[Decimal]:
    """Converts a monetary string to a Decimal, removing non-numeric characters."""
    if data in ("None", None):
        return None
    return Decimal(re.sub(r"[^0-9\.-]", "", data))


def round_to(
    precision: int, data: Optional[Union[str, float, Decimal]] = None
) -> Union[Decimal, Callable[[Union[str, float, Decimal]], Decimal]]:
    """Rounds a number to a specified precision."""

    def function(value):
        if value in ("None", None):
            return None
        if isinstance(value, str):
            value = re.sub(r"[^0-9\.-]", "", value)
        return Decimal(value).quantize(
            Decimal(10) ** -precision, rounding=ROUND_HALF_UP
        )

    return function(data) if data is not None else function


def decimal(data: str) -> Optional[Decimal]:
    """Converts a numeric string to a Decimal, removing non-numeric characters."""
    if data in ("None", None):
        return None
    return Decimal(re.sub(r"[^0-9\.-]", "", data))


def ein(data: str) -> Optional[str]:
    """Validates and returns a 9-digit EIN, or None if invalid."""
    if data in ("None", None):
        return None
    cleaned_data = re.sub(r"[^0-9]", "", data)
    match = re.fullmatch(r"\d{9}", cleaned_data)
    return match.group() if match else None


def to_list(data: Union[str, list]) -> Optional[list]:
    """Converts a string or single element into a list representation."""
    if data in (None, "None"):
        return None
    if isinstance(data, str) and data.startswith("["):
        return eval(data)  # Assuming the input string is a list string
    return [data] if not isinstance(data, list) else data


def title(data: str) -> str:
    """Converts a string to title case."""
    return "" if data in (None, "None") else str(data).title()


def lower(data: str) -> str:
    """Converts a string to lowercase."""
    return "" if data in (None, "None") else str(data).lower()


def upper(data: str) -> str:
    """Converts a string to uppercase."""
    return "" if data in (None, "None") else str(data).upper()


def padding(length: int, char: str = " ") -> Callable[[str], Optional[str]]:
    """Pads a string to the specified length with a given character."""

    def inner(data: str) -> Optional[str]:
        if data in [None, "None", ""]:
            return None
        return str(data).rjust(length, char)

    return inner


def string(data: str) -> Optional[str]:
    """Converts an empty string to None, otherwise returns the string itself."""
    return None if data == "" else str(data)
