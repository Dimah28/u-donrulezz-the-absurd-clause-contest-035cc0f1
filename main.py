"""Clause 12.4: an absurd clause buried in a terms-of-service agreement.

The program drops a single 165-character clause sentence into
/output/entry.txt. Standard library only, no network access, no
secrets, and the same bytes come out on every run.
"""

import os

# Split across lines only for readability; the value is one sentence.
CLAUSE = (
    "12.4 The user agrees that, by accepting these terms, they have "
    "adopted the company office goldfish, including all future feeding, "
    "naming disputes, and funeral costs."
)

LIMIT = 200
ENDERS = (".", "!", "?")
BREAKS = (". ", "! ", "? ")


def reject(message):
    """Abort the run with a plain-language reason."""
    raise SystemExit(message)


def ensure_one_sentence(text):
    """Reject the text if it hides a second sentence inside it.

    A break is a sentence-ending mark followed by a space. A bare
    period on its own is not a break, so decimals and abbreviations
    do not trigger this.
    """
    for mark in BREAKS:
        if mark in text:
            reject(f"clause holds more than one sentence (found {mark!r})")


def validate_clause(raw):
    """Run the bounty gate over the clause; return the cleaned text.

    The gate: 1 to LIMIT characters, not blank, a single line, ending
    in sentence punctuation, and exactly one sentence long.
    """
    text = raw.strip()
    if not text:
        reject("clause is empty or only whitespace")
    if "\n" in text or "\r" in text:
        reject("clause must fit on one line")
    if len(text) > LIMIT:
        reject(f"clause is {len(text)} characters, over the {LIMIT} limit")
    if text[-1] not in ENDERS:
        reject("clause must end with sentence-ending punctuation")
    ensure_one_sentence(text)
    return text


def main():
    clause = validate_clause(CLAUSE)
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(clause + "\n")


if __name__ == "__main__":
    main()
