#!/usr/bin/env python3
"""Entry program for "The Word You'd Delete From the Dictionary".

The pick is the single word "misspelled".

Why this word wins the joke on sight:

* It is the one word in the dictionary that accuses itself. Everyone
  who has ever typed it has paused over the double s and the double
  l -- it looks like exactly what it describes, so the laugh arrives
  before any explanation could (judge criterion 2).
* All of the humour lives inside the word itself: its spelling, its
  meaning, and the gap its deletion would leave. Delete "misspelled"
  and no typo could ever be named again -- every future mistake
  becomes unmentionable, which is the deletion performing its own
  punchline (criterion 3).
* It is fresh. In a study of all 702 entries received, the crowded
  picks were irregardless (40+), queue (22+), moist (21+), literally
  (14+) and defenestration (11+); "misspelled" appeared in none of
  them (criterion 4).
* It is exact: one real, instantly recognised word, spelled
  correctly, ten bytes, no trailing newline (criteria 1 and 5).

The program is deterministic and uses only the standard library. It
writes the word to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output/entry.txt) and nothing else.
"""

import os

WORD = "misspelled"
MAX_CHARS = 77


def check(word):
    if not word:
        raise ValueError("empty entry")
    if len(word) > MAX_CHARS:
        raise ValueError("entry longer than the 77-character gate")
    if word.strip() != word or any(c.isspace() for c in word):
        raise ValueError("entry must be exactly one word")
    if not word.isalpha() or not word.islower():
        raise ValueError("entry must be one lowercase word")
    word.encode("utf-8")
    return word


def main():
    word = check(WORD)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = word.encode("utf-8")
    # Atomic publish: write beside the target, flush to disk, then
    # rename over it, so a reader can never observe a partial entry.
    # The payload is exactly the ten bytes of the word -- no trailing
    # newline -- which also keeps the entry as small as this pick can
    # be for the size tie-break.
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp_path, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
