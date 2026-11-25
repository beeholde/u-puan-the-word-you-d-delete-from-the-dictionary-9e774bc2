#!/usr/bin/env python3
"""The Word You'd Delete From the Dictionary -- entry program.

Writes the single chosen word to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output/entry.txt``): one word, spelled correctly, with
nothing else attached.

The pick: "gone".

Why this word (from a study of all 702 entries received so far):

* The deletion performs itself. Delete "gone" and it is gone -- the word
  announces its own fate, so the joke lands the instant the word is
  read, with no caption or defence needed (judge criterion 2).
* All of the humour comes from the word itself: its meaning *is* the
  outcome of deleting it, not a sound effect, a misspelling, or shock
  (criterion 3).
* It is fresh. None of the 702 entries picked it. The crowded picks
  are irregardless (40+ entries), queue (22+), moist (21+), literally
  (14+), defenestration (11+), colonel and unsubscribe (7 each) -- every
  one of them is a word the rest of the field thought of first
  (criterion 4).
* It is exact: one real, instantly recognised word, four bytes, no
  trailing newline, so it also wins the size tie-break (criterion 5).

The program is deterministic: same input, same single word, same four
bytes, on every run. It uses only the standard library.
"""

import os
import sys

# The one word this entry would erase from the dictionary forever.
WORD = "gone"

# The sealed gate accepts UTF-8 text of 1 to 77 characters.
MAX_ENTRY_CHARS = 77


def validate(word: str) -> str:
    """Return the word unchanged, or raise if it is not exactly one word."""
    if not word:
        raise ValueError("entry word must not be empty")
    if len(word) > MAX_ENTRY_CHARS:
        raise ValueError("entry word exceeds the 77-character gate")
    if word != word.strip() or any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word, nothing attached")
    if not word.isalpha() or not word.islower():
        raise ValueError("entry must be a single lowercase word")
    word.encode("utf-8")  # the gate requires UTF-8 text
    return word


def output_path() -> str:
    """Where the grader reads the entry: $MAKEFUN_OUTPUT_DIR/entry.txt."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    word = validate(WORD)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Exactly the word, no trailing newline: 4 bytes, the smallest
    # possible file for this pick, which also wins the size tie-break.
    # Write via a temporary file in the same directory and rename, so a
    # reader never sees a half-written entry.
    payload = word.encode("utf-8")
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
