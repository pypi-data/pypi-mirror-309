import unittest
from indonesian_number_normalizer import create_normalizer

class TestIndonesianNumberNormalizer(unittest.TestCase):
    def setUp(self):
        self.normalizer = create_normalizer()

    def test_basic_numbers(self):
        test_cases = [
            (0, "nol"),
            (1, "satu"),
            (10, "sepuluh"),
            (11, "sebelas"),
            (15, "lima belas"),
            (20, "dua puluh"),
            (21, "dua puluh satu"),
            (100, "seratus"),
            (101, "seratus satu"),
            (111, "seratus sebelas"),
            (200, "dua ratus"),
            (999, "sembilan ratus sembilan puluh sembilan"),
        ]
        for number, expected in test_cases:
            self.assertEqual(self.normalizer.number_to_words(number), expected)

    def test_large_numbers(self):
        test_cases = [
            (1000, "seribu"),
            (2000, "dua ribu"),
            (10000, "sepuluh ribu"),
            (100000, "seratus ribu"),
            (1000000, "satu juta"),
            (1000000000, "satu milyar"),
            (1234567890, "satu milyar dua ratus tiga puluh empat juta lima ratus enam puluh tujuh ribu delapan ratus sembilan puluh"),
            # Special cases
            (1100, "seribu seratus"),
            (1001, "seribu satu"),
            (2001, "dua ribu satu"),
            (21000, "dua puluh satu ribu"),
        ]
        for number, expected in test_cases:
            self.assertEqual(self.normalizer.number_to_words(number), expected)

    def test_decimal_numbers(self):
        test_cases = [
            (1.5, "satu koma lima"),
            (2.05, "dua koma nol lima"),
            (10.01, "sepuluh koma nol satu"),
        ]
        for number, expected in test_cases:
            self.assertEqual(self.normalizer.number_to_words(number), expected)

    def test_currency(self):
        test_cases = [
            ((1500, "IDR"), "seribu lima ratus rupiah"),
            ((1500.50, "USD"), "seribu lima ratus dolar lima puluh sen"),
            ((1500.50, "EUR"), "seribu lima ratus euro lima puluh sen"),
        ]
        for (amount, currency), expected in test_cases:
            self.assertEqual(self.normalizer.convert_currency(amount, currency), expected)

    def test_percentage(self):
        test_cases = [
            (2.5, "dua koma lima persen"),
            (10, "sepuluh persen"),
            (0.5, "nol koma lima persen"),
        ]
        for number, expected in test_cases:
            self.assertEqual(self.normalizer.convert_percentage(number), expected)

    def test_time(self):
        test_cases = [
            ("09:30", "sembilan lewat tiga puluh menit"),
            ("15:00", "tiga sore"),
            ("00:00", "dua belas malam"),
        ]
        for time_str, expected in test_cases:
            self.assertEqual(self.normalizer.convert_time(time_str), expected)

    def test_ordinal(self):
        test_cases = [
            (1, "pertama"),
            (2, "kedua"),
            (10, "kesepuluh"),
            (11, "kesebelas"),
            (20, "kedua puluh"),
        ]
        for number, expected in test_cases:
            self.assertEqual(self.normalizer.convert_ordinal(number), expected)

    def test_text_normalization(self):
        test_cases = [
            (
                "Harga saham naik 2,5% menjadi Rp4.150 per lembar.",
                "Harga saham naik dua koma lima persen menjadi empat ribu seratus lima puluh rupiah per lembar."
            ),
            (
                "Meeting dimulai pukul 09:30 pagi.",
                "Meeting dimulai pukul sembilan lewat tiga puluh menit pagi."
            ),
            (
                "Suhu mencapai 32,5 derajat celcius.",
                "Suhu mencapai tiga puluh dua koma lima derajat celcius."
            ),
            # Add more complex cases
            (
                "Nilai tukar rupiah menguat 2,5% ke level Rp14.255,5 per dolar AS.",
                "Nilai tukar rupiah menguat dua koma lima persen ke level empat belas ribu dua ratus lima puluh lima koma lima rupiah per dolar AS."
            ),
            (
                "Inflasi tahun 2023 mencapai 3,5%, lebih rendah dari 5,51% di 2022.",
                "Inflasi tahun dua ribu dua puluh tiga mencapai tiga koma lima persen, lebih rendah dari lima koma lima puluh satu persen di dua ribu dua puluh dua."
            ),
        ]
        for text, expected in test_cases:
            self.assertEqual(self.normalizer.normalize_text(text), expected)

if __name__ == '__main__':
    unittest.main()