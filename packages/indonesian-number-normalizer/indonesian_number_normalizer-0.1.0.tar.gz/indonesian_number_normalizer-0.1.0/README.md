# Indonesian Number Normalizer

A Python package for converting numbers to Indonesian words. This package is particularly useful for Text-to-Speech (TTS) preprocessing where numbers need to be converted to their word representations.

## Features

- Convert numbers to Indonesian words
- Support for:
  - Integers
  - Decimal numbers
  - Currency (IDR, USD, EUR)
  - Percentages
  - Time
  - Ordinal numbers
- Automatic number detection in text
- Comprehensive text normalization

## Installation

```bash
pip install indonesian-number-normalizer
```

## Quick Start

```python
from indonesian_number_normalizer import create_normalizer

# Create normalizer instance
normalizer = create_normalizer()

# Convert simple numbers
print(normalizer.number_to_words(1234))  # "seribu dua ratus tiga puluh empat"

# Convert currency
print(normalizer.convert_currency(4150))  # "empat ribu seratus lima puluh rupiah"

# Normalize text containing numbers
text = "Harga saham naik 2,5% menjadi Rp4.150 per lembar."
normalized = normalizer.normalize_text(text)
print(normalized)  # "Harga saham naik dua koma lima persen menjadi empat ribu seratus lima puluh rupiah per lembar."
```

## Advanced Usage

### Currency Conversion
```python
# Indonesian Rupiah
normalizer.convert_currency(1500000)  # "satu juta lima ratus ribu rupiah"

# US Dollar
normalizer.convert_currency(1500.50, currency="USD")  # "seribu lima ratus dolar lima puluh sen"

# Euro
normalizer.convert_currency(1500.50, currency="EUR")  # "seribu lima ratus euro lima puluh sen"
```

### Time Conversion
```python
normalizer.convert_time("09:30")  # "sembilan lewat tiga puluh menit"
```

### Percentage Conversion
```python
normalizer.convert_percentage(2.5)  # "dua koma lima persen"
```

### Ordinal Numbers
```python
normalizer.convert_ordinal(3)  # "ketiga"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
