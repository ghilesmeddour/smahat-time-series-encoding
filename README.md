# Smahat Time Series Encoding

Smahat allows to encode a sequence of integer values using a fixed (for all values) number of bits but minimal with regards to the data range. For example: for a series of boolean values only one bit is needed, for a series of integer percentages 7 bits are needed, etc.

Smahat is useful when:
- Time series is integer-valued. (It doesn't work with floats :))
- The range of the data is known in advance (if not streaming, this is not necessary).
- The data range is relatively small.
- The data does not have properties that would make other compression algorithms useful, or these other algorithms have an unacceptable cost for the use case.

Smahat can also be used as a baseline to calculate the true compression ratio of a compression algorithm on data of a certain nature.

## Installation

To install the latest release:
```
$ pip install smahat
```

You can also build a local package and install it:
```
$ make build
$ pip install dist/*.whl
```

## Usage

Import `smahat` module.

```python
>>> import smahat
```

Data to encode.

```python
>>> values = [12, 0, 17, 15, 78, 10]
```

### Encoding

You can use `encode_next` to encode one value by one:

```python
>>> encoder = smahat.Encoder(min_value=0, max_value=100, strategy='saturate')
>>> for v in values:
...     encoder.encode_next(v)
>>> content = encoder.get_encoded()
>>> content
{'encoded': b'\x18\x00\x88\xf9\xc2\x80', 'shift': 0, 'n_bits_per_value': 7, 'n_padding_bits': 6}
```

Or you can use `Encoder.encode_all` to encode all values (range min and max will be inferred from values if not provided):
```python
>>> content = smahat.Encoder.encode_all(values, min_value=0, max_value=100, strategy='saturate')
>>> content
{'encoded': b'\x18\x00\x88\xf9\xc2\x80', 'shift': 0, 'n_bits_per_value': 7, 'n_padding_bits': 6}
```

### Decoding

To decode use `Decoder.decode_all`.

```python
>>> smahat.Decoder.decode_all(content)
[12, 0, 17, 15, 78, 10]
```

## Encoding result

The result of the encoding of a sequence of values using Smahat is a `SmahatContent` dictionary containing the `encoded` data, plus three fields : `shift` is used to bring the data range to start from zero (values are shifted and encoded in pure binary), `n_bits_per_value` indicates the number of bits used to encode each value, `n_padding_bits` (between 0 and 7) indicates the number of unused padding bits within the last byte.

```python
class SmahatContent(TypedDict):
    encoded: bytes
    shift: int
    n_bits_per_value: int
    n_padding_bits: int
```

If you want to use this library for message exchanges, you can serialize the result of the encoding as you like (JSON, protobuf, etc.)

## Contribute

```
$ git clone https://github.com/ghilesmeddour/smahat-time-series-encoding.git
$ cd smahat-time-series-compression
```

```
make format
make dead-code-check
make test
make type-check
make coverage
make build
```

### TODOs

- [ ] Add unit tests.
- [ ] Improve doc.
