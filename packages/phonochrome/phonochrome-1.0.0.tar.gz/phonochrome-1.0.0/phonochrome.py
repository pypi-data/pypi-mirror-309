"""
Phonochrome: A bijective 8-bit RGB encoding library that generates phonotactically plausible appellations.
"""

import re as _re
import sys as _sys

if _sys.version_info >= (3, 9):
    # Use the built-in tuple with type parameters for Python 3.9+
    RGB = tuple[int, int, int]
else:
    # Use Tuple from typing for Python 3.8 and earlier
    from typing import Tuple as _Tuple

    RGB = _Tuple[int, int, int]

C = [
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "r",
    "t",
    "v",
    "z",
]

V = [
    "a",
    "e",
    "i",
    "o",
    "u",
    "ai",
    "io",
    "as",
    "é",
    "ó",
    "us",
    "ü",
    "ia",
    "is",
    "í",
    "os",
]


def encode(rgb: RGB):
    """Encode an 8-bit RGB tuple into a phonochrome appellation."""
    if any(c not in range(256) for c in rgb):
        raise ValueError("Invalid 8-bit RGB tuple: {rgb}".format(rgb=rgb))
    m = ""
    for idx, component in enumerate(rgb):
        c = C[idx:] + C[:idx]
        v = V[idx:] + V[:idx]
        h = hex(component)[2:].zfill(2)
        m += c[int(h[0], 16)] + v[int(h[1], 16)]
    return m


def decode(s: str) -> RGB:
    """Decode a phonochrome appellation into an 8-bit RGB tuple."""
    if not s:
        return ""
    jc = "|".join(C)
    jv = "|".join(sorted(V, key=len, reverse=True))
    pattern = _re.compile(
        "".join(
            "(?P<c{i}>{jc})(?P<v{i}>{jv})".format(i=i, jc=jc, jv=jv)
            for i in range(1, 4)
        )
    )
    match = pattern.match(s)
    if not match:
        raise ValueError("Invalid appellation: '{s}'".format(s=s))
    groups = match.groups()
    rgb = []
    for idx, (c, v) in enumerate(zip(groups[::2], groups[1::2])):
        C_idx = (C[idx:] + C[:idx]).index(c)
        V_idx = (V[idx:] + V[:idx]).index(v)
        int_str = "{:1x}{:1x}".format(C_idx, V_idx)
        rgb.append(int(int_str, 16))
    return tuple(rgb)


def _print_and_exit(func, *args):
    try:
        print(func(*args))
    except ValueError as e:
        print("Error: " + str(e))
        _sys.exit(2)
    else:
        _sys.exit(0)


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Encode Parser
    encode_parser = subparsers.add_parser("encode", help=encode.__doc__)
    encode_parser.add_argument("r", type=int, help="Red component (0-255)")
    encode_parser.add_argument("g", type=int, help="Green component (0-255)")
    encode_parser.add_argument("b", type=int, help="Blue component (0-255)")

    # Decode Parser
    decode_parser = subparsers.add_parser("decode", help=decode.__doc__)
    decode_parser.add_argument("word", type=str, help="Phonochrome to decode")

    args = parser.parse_args()

    if args.command == "encode":
        _print_and_exit(encode, (args.r, args.g, args.b))
    elif args.command == "decode":
        _print_and_exit(decode, args.word)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
