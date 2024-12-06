# test_iconv.py
import unittest
import re
import codecs
from decimal import Decimal, InvalidOperation
from datetime import datetime, date, time
from typing import Optional, Union, Callable
from velocity.misc.conv.iconv import (
    none,
    phone,
    day_of_week,
    date as date_func,
    time as time_func,
    timestamp,
    email,
    integer,
    boolean,
    rot13,
    pointer,
    money,
    round_to,
    decimal as decimal_func,
    ein,
    to_list,
    title,
    lower,
    upper,
    padding,
    string,
)


class TestIconvModule(unittest.TestCase):

    def test_none(self):
        self.assertIsNone(none(""))
        self.assertIsNone(none("null"))
        self.assertIsNone(none("None"))
        self.assertIsNone(none("@NULL"))
        self.assertEqual(none("value"), "value")

    def test_phone(self):
        self.assertEqual(phone("123-456-7890"), "1234567890")
        self.assertEqual(phone("(123) 456-7890"), "1234567890")
        self.assertIsNone(phone("12345"))
        self.assertIsNone(phone(None))
        self.assertIsNone(phone("None"))

    def test_day_of_week(self):
        self.assertEqual(day_of_week("Monday"), 1)
        self.assertEqual(day_of_week("fri"), 5)
        self.assertIsNone(day_of_week("Funday"))
        self.assertIsNone(day_of_week(""))
        self.assertIsNone(day_of_week(None))

    def test_date(self):
        self.assertEqual(date_func("2023-01-01"), date(2023, 1, 1))
        self.assertIsNone(date_func("2023/01/01"))
        self.assertIsNone(date_func(""))
        self.assertIsNone(date_func(None))
        self.assertEqual(date_func("01-02-2023", fmt="%d-%m-%Y"), date(2023, 2, 1))

    def test_time(self):
        self.assertEqual(time_func("23:59:59"), time(23, 59, 59))
        self.assertIsNone(time_func("24:00:00"))
        self.assertIsNone(time_func(""))
        self.assertIsNone(time_func(None))
        self.assertEqual(time_func("11:30 PM", fmt="%I:%M %p"), time(23, 30))

    def test_timestamp(self):
        self.assertEqual(
            timestamp("01 Jan 23 12:34:56", fmt="%d %b %y %H:%M:%S"),
            datetime(2023, 1, 1, 12, 34, 56),
        )
        self.assertIsNone(timestamp("Invalid date"))
        self.assertIsNone(timestamp(""))
        self.assertIsNone(timestamp(None))

    def test_email(self):
        self.assertEqual(email("Test@Example.com"), "test@example.com")
        self.assertEqual(
            email("  user.name+tag+sorting@example.com  "),
            "user.name+tag+sorting@example.com",
        )
        self.assertIsNone(email(None))
        self.assertIsNone(email("None"))
        with self.assertRaises(ValueError):
            email("invalid-email")

    def test_integer(self):
        self.assertEqual(integer("123"), 123)
        self.assertEqual(integer("-123"), -123)
        self.assertEqual(integer("1,234"), 1234)
        self.assertEqual(integer("$1,234.56"), 1234)
        self.assertEqual(integer("abc123xyz"), 123)
        with self.assertRaises(ValueError):
            integer("abc")

    def test_boolean(self):
        self.assertFalse(boolean(""))
        self.assertFalse(boolean("false"))
        self.assertFalse(boolean("False"))
        self.assertFalse(boolean("f"))
        self.assertFalse(boolean("off"))
        self.assertFalse(boolean("no"))
        self.assertTrue(boolean("True"))
        self.assertTrue(boolean("yes"))
        self.assertTrue(boolean(True))
        self.assertFalse(boolean(False))

    def test_rot13(self):
        self.assertEqual(rot13("Hello"), "Uryyb")
        self.assertEqual(rot13("Uryyb"), "Hello")
        self.assertEqual(rot13(""), "")
        self.assertEqual(
            rot13("Gur Dhvpx Oebja Sbk Whzcf Bire Gur Ynml Qbt."),
            "The Quick Brown Fox Jumps Over The Lazy Dog.",
        )

    def test_pointer(self):
        self.assertIsNone(pointer("@new"))
        self.assertIsNone(pointer("@NULL"))
        self.assertIsNone(pointer(None))
        self.assertIsNone(pointer(""))
        self.assertEqual(pointer("123"), 123)
        self.assertEqual(pointer(456), 456)
        with self.assertRaises(ValueError):
            pointer("abc")

    def test_money(self):
        self.assertEqual(money("$1,234.56"), Decimal("1234.56"))
        self.assertEqual(money("-$1,234.56"), Decimal("-1234.56"))
        self.assertIsNone(money("None"))
        self.assertIsNone(money(None))
        with self.assertRaises(InvalidOperation):
            money("Invalid")

    def test_round_to(self):
        func = round_to(2)
        self.assertEqual(func("123.456"), Decimal("123.46"))
        self.assertEqual(func(Decimal("123.451")), Decimal("123.45"))
        self.assertIsNone(func(None))
        self.assertEqual(round_to(2, "123.456"), Decimal("123.46"))

    def test_decimal(self):
        self.assertEqual(decimal_func("123.456"), Decimal("123.456"))
        self.assertEqual(decimal_func("$1,234.56"), Decimal("1234.56"))
        self.assertIsNone(decimal_func("None"))
        self.assertIsNone(decimal_func(None))
        with self.assertRaises(InvalidOperation):
            decimal_func("Invalid")

    def test_ein(self):
        self.assertEqual(ein("12-3456789"), "123456789")
        self.assertEqual(ein("123456789"), "123456789")
        self.assertIsNone(ein("123-45-6789"))
        self.assertIsNone(ein("12345678"))
        self.assertIsNone(ein(None))
        self.assertIsNone(ein("None"))

    def test_to_list(self):
        self.assertEqual(to_list("[1, 2, 3]"), [1, 2, 3])
        self.assertEqual(to_list("['a', 'b', 'c']"), ["a", "b", "c"])
        self.assertEqual(to_list("value"), ["value"])
        self.assertEqual(to_list(["value1", "value2"]), ["value1", "value2"])
        self.assertIsNone(to_list(None))
        self.assertIsNone(to_list("None"))
        # Test with potential security risk input
        with self.assertRaises(SyntaxError):
            to_list("__import__('os').system('echo dangerous')")

    def test_title(self):
        self.assertEqual(title("hello world"), "Hello World")
        self.assertEqual(title("TEST"), "Test")
        self.assertEqual(title(None), "")
        self.assertEqual(title("None"), "")

    def test_lower(self):
        self.assertEqual(lower("Hello World"), "hello world")
        self.assertEqual(lower("TEST"), "test")
        self.assertEqual(lower(None), "")
        self.assertEqual(lower("None"), "")

    def test_upper(self):
        self.assertEqual(upper("Hello World"), "HELLO WORLD")
        self.assertEqual(upper("test"), "TEST")
        self.assertEqual(upper(None), "")
        self.assertEqual(upper("None"), "")

    def test_padding(self):
        pad_func = padding(5)
        self.assertEqual(pad_func("1"), "    1")
        self.assertEqual(pad_func("12345"), "12345")
        self.assertEqual(pad_func("123456"), "123456")
        self.assertIsNone(pad_func(None))
        self.assertIsNone(pad_func(""))
        pad_func_char = padding(5, "0")
        self.assertEqual(pad_func_char("1"), "00001")

    def test_string(self):
        self.assertEqual(string("value"), "value")
        self.assertIsNone(string(""))
        self.assertEqual(string(None), None)


if __name__ == "__main__":
    unittest.main()
