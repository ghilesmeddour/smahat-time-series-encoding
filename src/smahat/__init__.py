import logging

logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger('Smahat')

from .encode import Encoder
from .decode import Decoder
