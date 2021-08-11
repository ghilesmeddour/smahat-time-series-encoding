from typing import Iterable

from bitarray import bitarray
from bitarray import util

from .result import SmahatContent


class Decoder:
    """
    Smahat Decoder.
    """
    def __init__(self, bit_array, shift, n_bits_per_value):
        self.bit_array = bit_array
        self.shift = shift
        self.n_bits_per_value = n_bits_per_value

    def decode_next(self) -> int:
        shifted_value = util.ba2int(self.bit_array[:self.n_bits_per_value])
        del self.bit_array[:self.n_bits_per_value]
        value = shifted_value - self.shift
        return value

    @staticmethod
    def decode_all(content: SmahatContent) -> Iterable[int]:
        bit_array = bitarray(endian='big')
        bit_array.frombytes(content['encoded'])

        nb_values = (len(bit_array) -
                     content['n_padding_bits']) // content['n_bits_per_value']

        decoder = Decoder(bit_array, content['shift'],
                          content['n_bits_per_value'])

        return [decoder.decode_next() for _ in range(nb_values)]
