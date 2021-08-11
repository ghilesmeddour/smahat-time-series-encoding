from typing import TypedDict


class SmahatContent(TypedDict):
    encoded: bytes
    # [a, b] values range becomes [0, b+`shift`]
    shift: int
    # Number of bits per encoded value.
    n_bits_per_value: int
    # The number of unused padding bits within the last byte.
    # These bits should not be used during decoding.
    # The value is always between 0 and 7.
    n_padding_bits: int
