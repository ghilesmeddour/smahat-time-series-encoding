from typing import Iterable, Optional

from bitarray import bitarray
from bitarray import util

from .result import SmahatContent
from . import Logger


class Encoder:
    """
    Smahat Encoder.

    The user specifies the range of input [min_value, max_value] data 
    and the strategy to adopt if a value is outside this range. 
    The encoder determines from the specified range the number 
    of bits needed to encode each value.

    Parameters
    ----------
    min_value : int
        The minimum (inclusive) expected input value.
    max_value : int
        The maximum (inclusive) expected input value.
    strategy: {{'ignore', 'saturate', 'error'}}, default 'ignore'
        The behavior to adopt if an input value is not encodable 
        (out of range [min_value, max_value]).
        The value will not be encoded with 'ignore', it will be 
        saturated at the range limit if 'saturate' and an error 
        will be raised if 'error'.
    """
    def __init__(self, min_value: int, max_value: int, strategy='saturate'):
        if not (min_value < max_value):
            raise ValueError(
                f'range_min ({min_value}) should be smaller than range_max ({max_value}).'
            )

        if strategy not in ['ignore', 'saturate', 'error']:
            raise ValueError(
                f"Unexpected strategy ({strategy}). Strategy should be 'ignore', 'saturate' or 'error'."
            )

        self.min_value = min_value
        self.max_value = max_value

        self.strategy = strategy

        self.shift = -min_value
        self.n_bits_per_value = (max_value + self.shift).bit_length()

        self.nb_values = 0
        self.bit_array = bitarray(endian='big')

        Logger.info(f"Smahat Encoder initialized with: {self.__dict__}")

    def reinit(self):
        """
        Reset the encoder.
        """
        self.nb_values = 0
        self.bit_array.clear()

    def encode_next(self, value: int) -> bool:
        """
        Encodes a value, returns True if the encoding was done,
        False otherwise.

        Parameters
        ----------
        value : int
            Int value to encode.

        Returns
        -------
        bool
            `True` if the value has been encoded correctly, `False` if not.
        """
        if not (self.min_value <= value <= self.max_value):
            Logger.warning(
                f'Value {value} not in expected range [{self.min_value}, {self.max_value}]'
            )
            if self.strategy == 'error':
                raise Exception('Out of range value')
            elif self.strategy == 'ignore':
                Logger.warning(f'Ignore value {value}')
                return False
            elif self.strategy == 'saturate':
                if value > self.max_value:
                    value = self.max_value
                elif value < self.min_value:
                    value = self.min_value
                Logger.warning(f'Value saturated to {value}')

        shifted_value = value + self.shift
        self.bit_array += util.int2ba(shifted_value,
                                      length=self.n_bits_per_value,
                                      endian='big')
        self.nb_values += 1

        return True

    def get_encoded(self, reinit=True) -> SmahatContent:
        result: SmahatContent = {
            'encoded': self.bit_array.tobytes(),
            'shift': self.shift,
            'n_bits_per_value': self.n_bits_per_value,
            'n_padding_bits': self.bit_array.buffer_info()[3],
        }

        if reinit:
            self.reinit()

        return result

    @staticmethod
    def encode_all(values: Iterable[int],
                   min_value: Optional[int] = None,
                   max_value: Optional[int] = None,
                   strategy='saturate') -> SmahatContent:
        """
        Encode a list of values and return the encoded content.
        Range min and max will be inferred from values if not
        provided.
        """
        if min_value is None:
            min_value = min(values)
        if max_value is None:
            max_value = max(values)

        encoder = Encoder(min_value, max_value, strategy)

        for v in values:
            encoder.encode_next(v)

        return encoder.get_encoded()
