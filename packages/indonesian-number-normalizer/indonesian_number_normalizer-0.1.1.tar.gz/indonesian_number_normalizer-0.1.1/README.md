# Indonesian Number Normalizer 🔢

Convert numbers to Indonesian words for Text-to-Speech preprocessing.

[![PyPI version](https://badge.fury.io/py/indonesian-number-normalizer.svg)](https://badge.fury.io/py/indonesian-number-normalizer)
[![Tests](https://github.com/fiddien/indonesian-number-normalizer/actions/workflows/python-package.yml/badge.svg)](https://github.com/fiddien/indonesian-number-normalizer/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Transform numeric text into natural Indonesian words:

```python
"Harga saham naik 2,5% menjadi Rp4.150"
↓
"Harga saham naik dua koma lima persen menjadi empat ribu seratus lima puluh rupiah"
```

## Features 🌟

- **Numbers**: Integers, decimals, negatives
- **Currency**: IDR, USD, EUR
- **Formats**: Percentages, time, ordinals  
- **Text Processing**: Automatic number detection and normalization

## Installation 📦

```bash
pip install indonesian-number-normalizer
```

## Quick Usage 🚀

```python
from indonesian_number_normalizer import create_normalizer

normalizer = create_normalizer()

# Basic numbers
normalizer.number_to_words(1234)  
# "seribu dua ratus tiga puluh empat"

# Currency
normalizer.convert_currency(4150)  
# "empat ribu seratus lima puluh rupiah"

# Text normalization
text = "Harga saham naik 2,5% menjadi Rp4.150 per lembar."
normalizer.normalize_text(text)
# "Harga saham naik dua koma lima persen menjadi empat ribu seratus lima puluh rupiah per lembar."
```

## Advanced Usage 🛠️

### Currency

```python
# Multiple currency support
normalizer.convert_currency(1500000)      # IDR
normalizer.convert_currency(1500.50, "USD")  # USD
normalizer.convert_currency(1500.50, "EUR")  # EUR
```

### Time

```python
normalizer.convert_time("09:30")  
# "sembilan lewat tiga puluh menit"
```

### Percentages & Ordinals

```python
normalizer.convert_percentage(2.5)  # "dua koma lima persen"
normalizer.convert_ordinal(3)       # "ketiga"
```

## Development 🔧

```bash
# Clone repository
git clone https://github.com/fiddien/indonesian-number-normalizer.git
cd indonesian-number-normalizer

# Install development dependencies
pip install -e ".[test]"

# Run tests
pytest
```

## Contributing 🤝

Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

MIT License - see [LICENSE](LICENSE) for details.

## Citation 📚

```bibtex
@software{indonesian_number_normalizer,
  title = {Indonesian Number Normalizer},
  author = {Ilma Aliya Fiddien},
  year = {2024},
  url = {https://github.com/fiddien/indonesian-number-normalizer}
}
```
