# Phonochrome

Phonochrome is a bijective 8-bit RGB encoding library that generates phonotactically plausible appellations. The library constructs a unique string for each of the 16.7 million possible 8-bit RGB tuple permutations ($256^3 = 16,777,216$).

Each RGB component is first converted to base 16, which allows us to derive values from a more compact set of characters, represented as $S$. Let $x^1$ and $x^2$ represent the two hexadecimal digits (since the range 0-255 only comprises up to FF). If a component is less than 16, its hexadecimal string will be zero-padded to a length of two. Each hexadecimal character is then reconverted into decimal to serve as an index. $x^1$ maps to $C \subsetneq S$, and $x^2$ maps to $V \subsetneq S$, where $C$ and $V$ are lists of consonants and vowels (or vowel-like phonetics), meticulously curated to ensure phonotactic plausibility. The order of these lists changes based on the index of the enumerated RGB tuple. This is done for each component before the generated parts are concatenated and returned as an appellation.

## Example Usage

The library is extremely easy to use, and comes with two functions: ``encode`` and ``decode``.

```py
>>> import phonochrome

>>> black_rgb = (0, 0, 0) # define our RGB tuple
>>> phonochrome.encode(black_rgb) # encode the RGB into a phonochrome appellation
'bacedi'
```
```py
>>> import phonochrome

>>> phonochrome.decode('bacedi') # encode the RGB into a phonochrome appellation
(0, 0, 0)
```

## Command Line Interface

Phonochrome comes with a command line interface which is automatically added to your
environment's scripts upon installation. You can invoke it like this:

```bash
$ phonochrome encode 122 16 14
'kusdeda'
```
```bash
$ phonochrome decode kusdeda
(122, 16, 14)
```
```bash
$ phonochrome --help

usage: phonochrome [-h] {encode,decode} ...

Phonochrome: A bijective 8-bit RGB encoding library that generates phonotactically plausible appellations.

options:
  -h, --help       show this help message and exit

Commands:
  {encode,decode}
    encode         Encode an 8-bit RGB tuple into a phonochrome appellation.
    decode         Decode a phonochrome appellation into an 8-bit RGB tuple.
```

In the event that an invalid argument was passed to encode/decode, the script will terminate with
exit code 2, otherwise code 0.

```bash
$ phonochrome encode 295 543 712
Error: Invalid 8-bit RGB tuple: (295, 543, 712)
```
```bash
$ phonochrome decode invalid
Error: Invalid appellation: 'invalid'
```

## Installation

Install from pip:

```bash
pip install phonochrome
```
