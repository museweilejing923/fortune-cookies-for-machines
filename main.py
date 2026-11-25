"""A fortune-cookie line for machines, written out by a tiny script.

One fixed sentence lives in this file. Before anything is saved,
the sentence is walked through a set of small named checks; only
a sentence that clears all of them reaches /output/entry.txt.
The program takes no input and keeps no state, so every run
writes exactly the same bytes.
"""

import sys
from pathlib import Path

ENTRY = "You will meet a tall, dark stranger: it is your own context window, and it has already forgotten you."
MAX_LEN = 200
TARGET = Path("/output/entry.txt")

TERMINATORS = ".!?"


def fail(msg):
    print(f"rejected: {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_on_theme(text):
    if "context" not in text:
        fail("entry is off topic")


def check_within_limit(text):
    if len(text) > MAX_LEN:
        fail("entry is longer than the limit")


def check_has_text(text):
    if not text or not text.strip():
        fail("entry is empty")


def check_tidy(text):
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        fail("entry has ragged edges or line breaks")


def check_ends_well(text):
    if not text or text[-1] not in TERMINATORS:
        fail("entry must end with . ! or ?")


def check_no_controls(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        fail("entry has control characters")


def check_has_letters(text):
    if not any(ch.isalpha() for ch in text):
        fail("entry has no letters")


def check_not_digits_only(text):
    if text.isdigit():
        fail("entry is only digits")


def check_not_marks_only(text):
    if not any(ch.isalnum() for ch in text):
        fail("entry is only punctuation")


def check_not_shouting(text):
    if any(ch.isalpha() for ch in text) and text == text.upper():
        fail("entry is written in all caps")


def check_no_zwj(text):
    if "\u200d" in text:
        fail("entry contains a zero-width joiner")


CHECKS = (
    check_no_zwj,
    check_on_theme,
    check_within_limit,
    check_has_text,
    check_tidy,
    check_ends_well,
    check_no_controls,
    check_has_letters,
    check_not_digits_only,
    check_not_marks_only,
    check_not_shouting,
)


def validate(text):
    for checker in CHECKS:
        checker(text)


def main():
    validate(ENTRY)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
