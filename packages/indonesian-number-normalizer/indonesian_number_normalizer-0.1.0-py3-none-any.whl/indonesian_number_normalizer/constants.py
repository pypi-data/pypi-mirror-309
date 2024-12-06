"""Constants used in the Indonesian number normalizer."""

UNITS = {
    0: 'nol',
    1: 'satu',
    2: 'dua',
    3: 'tiga',
    4: 'empat',
    5: 'lima',
    6: 'enam',
    7: 'tujuh',
    8: 'delapan',
    9: 'sembilan',
    10: 'sepuluh',
    11: 'sebelas'
}

SCALES = {
    0: '',
    1: 'ribu',
    2: 'juta',
    3: 'milyar',
    4: 'triliun'
}

CURRENCY_UNITS = {
    "IDR": ("rupiah", "sen"),
    "USD": ("dolar", "sen"),
    "EUR": ("euro", "sen")
}

# Regular expressions for number detection
PATTERNS = {
    'currency': r'Rp\s*\d+(?:\.\d{3})*(?:,\d{2})?',
    'percentage': r'-?\d+(?:,\d+)?%',
    'time': r'\d{1,2}:\d{2}',
    'decimal': r'-?\d+,\d+',
    'integer': r'-?\d+(?:\.\d{3})*'
}

ORDINAL_SPECIAL = {
    1: "pertama",
    2: "kedua",
    3: "ketiga",
    4: "keempat",
    5: "kelima",
    6: "keenam",
    7: "ketujuh",
    8: "kedelapan",
    9: "kesembilan",
    10: "kesepuluh"
}
