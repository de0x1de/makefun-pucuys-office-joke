"""Write the one-line office joke entry to /output/entry.txt.

The joke is assembled from three parts, validated against the
competition rules (UTF-8 text, 1 to 200 characters, a single line,
not only whitespace), written out, and read back for a byte-exact
comparison before the program exits.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARACTERS = 200

# The joke, in three parts: the setup, the routine, and the punchline.
SETUP = "We installed a suggestion box."
ROUTINE = "HR empties it every Friday directly into the shredder,"
PUNCHLINE = "for morale."


def build_joke() -> str:
    """Join the parts into the single-line joke."""
    return " ".join([SETUP, ROUTINE, PUNCHLINE])


def validate(text: str) -> None:
    """Check the joke against the entry rules."""
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARACTERS:
        raise ValueError(f"entry is {len(text)} characters, over {MAX_CHARACTERS}")
    if not text.startswith("We installed a suggestion box."):
        raise ValueError("entry lost its setup")
    if "shredder" not in text:
        raise ValueError("entry lost its punchline image")
    if not text.endswith("for morale."):
        raise ValueError("entry lost its punchline ending")
    parts = build_joke().split(" ")
    if parts[0] != "We" or parts[-1] != "morale.":
        raise ValueError("entry boundaries drifted from the assembled joke")
    if text.count(" ") != len(parts) - 1:
        raise ValueError("entry spacing is not the single-space join")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry does not round-trip as UTF-8")
    if not text.isascii():
        raise ValueError("entry must be plain ASCII")
    if len(encoded) != len(text):
        raise ValueError("byte count and character count diverged")


def main() -> None:
    joke = build_joke()
    validate(joke)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(joke.encode("utf-8"))
    written = OUTPUT_PATH.read_bytes()
    if written != joke.encode("utf-8"):
        raise SystemExit("read-back mismatch: /output/entry.txt differs from the joke")
    print(f"wrote {len(written)} bytes ({len(joke)} characters) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
