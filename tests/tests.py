import sys
import unittest

import numpy as np

sys.path.insert(0, '..')
from src.smahat.encode import Encoder
from src.smahat.decode import Decoder


class TestSmahat(unittest.TestCase):
    def test_random(self):
        np.random.seed(0)

        sizes = [np.random.randint(0, 1000) for _ in range(10)]

        # booleans, percentages, negatives
        mins = [0, 0, -50]
        maxs = [1, 100, 50]

        for size in sizes:
            for min_v, max_v in zip(mins, maxs):
                values = np.random.randint(min_v, max_v + 1, size)
                values = list(map(lambda x: x.item(), values))

                encoder = Encoder(min_value=min_v, max_value=max_v)

                for v in values:
                    encoder.encode_next(v)

                content = encoder.get_encoded()

                self.assertEqual(
                    Encoder.encode_all(values,
                                       min_value=min_v,
                                       max_value=max_v), content)
                self.assertEqual(Decoder.decode_all(content), values)
