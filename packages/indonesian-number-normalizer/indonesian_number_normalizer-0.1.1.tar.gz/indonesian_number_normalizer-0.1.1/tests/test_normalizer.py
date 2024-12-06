"""Tests for the Indonesian Number Normalizer package."""

import pytest
from indonesian_number_normalizer import create_normalizer

@pytest.fixture
def normalizer():
    """Create a normalizer instance for testing."""
    return create_normalizer()

def test_basic_numbers(normalizer):
    """Test conversion of basic numbers."""
    assert normalizer.number_to_words(0) == "nol"
    assert normalizer.number_to_words(1) == "satu"
    assert normalizer.number_to_words(10) == "sepuluh"
    assert normalizer.number_to_words(11) == "sebelas"
    assert normalizer.number_to_words(15) == "lima belas"
    assert normalizer.number_to_words(20) == "dua puluh"
    assert normalizer.number_to_words(25) == "dua puluh lima"
    assert normalizer.number_to_words(100) == "seratus"
    assert normalizer.number_to_words(101) == "seratus satu"
    assert normalizer.number_to_words(111) == "seratus sebelas"
    assert normalizer.number_to_words(125) == "seratus dua puluh lima"

def test_large_numbers(normalizer):
    """Test conversion of large numbers."""
    assert normalizer.number_to_words(1000) == "seribu"
    assert normalizer.number_to_words(1001) == "seribu satu"
    assert normalizer.number_to_words(1234) == "seribu dua ratus tiga puluh empat"
    assert normalizer.number_to_words(100000) == "seratus ribu"
    assert normalizer.number_to_words(1000000) == "satu juta"
    assert normalizer.number_to_words(1000000000) == "satu milyar"

def test_decimal_numbers(normalizer):
    """Test conversion of decimal numbers."""
    assert normalizer.number_to_words(1.5) == "satu koma lima"
    assert normalizer.number_to_words(0.5) == "nol koma lima"
    assert normalizer.number_to_words(1.23) == "satu koma dua tiga"
    assert normalizer.convert_decimal_number(2.5) == "dua koma lima"
    assert normalizer.convert_decimal_number(10.05) == "sepuluh koma nol lima"

def test_negative_numbers(normalizer):
    """Test conversion of negative numbers."""
    assert normalizer.number_to_words(-1) == "minus satu"
    assert normalizer.number_to_words(-15) == "minus lima belas"
    assert normalizer.number_to_words(-1.5) == "minus satu koma lima"

def test_currency_conversion(normalizer):
    """Test currency conversion."""
    assert normalizer.convert_currency(1500) == "seribu lima ratus rupiah"
    assert normalizer.convert_currency(1500.50) == "seribu lima ratus rupiah lima puluh sen"
    assert normalizer.convert_currency(1500, "USD") == "seribu lima ratus dolar"
    assert normalizer.convert_currency(1500.50, "USD") == "seribu lima ratus dolar lima puluh sen"
    assert normalizer.convert_currency(1500, "EUR") == "seribu lima ratus euro"

def test_percentage_conversion(normalizer):
    """Test percentage conversion."""
    assert normalizer.convert_percentage(2.5) == "dua koma lima persen"
    assert normalizer.convert_percentage(10) == "sepuluh persen"
    assert normalizer.convert_percentage(0.5) == "nol koma lima persen"

def test_ordinal_conversion(normalizer):
    """Test ordinal number conversion."""
    assert normalizer.convert_ordinal(1) == "pertama"
    assert normalizer.convert_ordinal(2) == "kedua"
    assert normalizer.convert_ordinal(10) == "kesepuluh"
    assert normalizer.convert_ordinal(11) == "kesebelas"
    assert normalizer.convert_ordinal(20) == "kedua puluh"

def test_time_conversion(normalizer):
    """Test time conversion."""
    assert normalizer.convert_time("09:00") == "sembilan pagi"
    assert normalizer.convert_time("09:30") == "sembilan lewat tiga puluh menit"
    assert normalizer.convert_time("12:00") == "dua belas siang"
    assert normalizer.convert_time("15:00") == "tiga sore"
    assert normalizer.convert_time("00:00") == "dua belas malam"

def test_text_normalization(normalizer):
    """Test full text normalization."""
    input_text = "Harga saham naik 2,5% menjadi Rp4.150 per lembar pada pukul 09:30."
    expected = "Harga saham naik dua koma lima persen menjadi empat ribu seratus lima puluh rupiah per lembar pada pukul sembilan lewat tiga puluh menit."
    assert normalizer.normalize_text(input_text) == expected

    input_text = "Suhu turun -2,5 derajat."
    expected = "Suhu turun minus dua koma lima derajat."
    assert normalizer.normalize_text(input_text) == expected

def test_number_detection(normalizer):
    """Test number detection in text."""
    text = "Harga Rp1.500 naik 2,5%"
    matches = normalizer.find_numbers(text)
    
    assert len(matches) == 2
    assert matches[0].type == "currency"
    assert matches[0].value == 1500
    assert matches[1].type == "percentage"
    assert matches[1].value == 2.5

def test_edge_cases(normalizer):
    """Test edge cases and potential error conditions."""
    assert normalizer.normalize_text("") == ""
    assert normalizer.normalize_text("No numbers here") == "No numbers here"
    assert normalizer.convert_time("25:00") == "25:00"  # Invalid time
    assert normalizer.convert_currency(0) == "nol rupiah"
    assert normalizer.number_to_words(1e9) == "satu milyar"
