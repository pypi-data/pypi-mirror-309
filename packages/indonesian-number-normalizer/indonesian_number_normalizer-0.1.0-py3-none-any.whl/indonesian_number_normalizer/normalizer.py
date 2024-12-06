"""Main module for Indonesian number normalization."""

import re
from typing import Dict, List, Tuple, Union
from dataclasses import dataclass
import decimal

from .constants import (
    UNITS,
    SCALES,
    CURRENCY_UNITS,
    PATTERNS,
    ORDINAL_SPECIAL,
)


@dataclass
class NumberMatch:
    """Class to store information about a number match in text."""

    original: str
    start: int
    end: int
    value: Union[int, float, str]
    type: str  # 'integer', 'decimal', 'percentage', 'currency', 'ordinal', 'time'


class IndonesianNumberNormalizer:
    """Class to handle conversion of numbers to Indonesian words."""

    def _split_decimal(self, num: float) -> Tuple[int, str]:
        """Split decimal number into integer and decimal parts."""
        decimal_str = str(decimal.Decimal(str(num)))
        if "." in decimal_str:
            integer_part, decimal_part = decimal_str.split(".")
            return int(integer_part), decimal_part
        return int(decimal_str), ""

    def _convert_tens(self, number: int) -> str:
        """Convert numbers from 0-99 to words."""
        if number < 12:
            return UNITS[number]
        elif number < 20:
            return f"{UNITS[number % 10]} belas"
        elif number < 100:
            tens, remainder = divmod(number, 10)
            if remainder == 0:
                return f"{UNITS[tens]} puluh"
            return f"{UNITS[tens]} puluh {UNITS[remainder]}"

    def _convert_hundreds(self, number: int) -> str:
        """Convert numbers from 0-999 to words."""
        if number < 100:
            return self._convert_tens(number)

        hundreds, remainder = divmod(number, 100)
        if hundreds == 1:
            prefix = "seratus"
        else:
            prefix = f"{UNITS[hundreds]} ratus"

        if remainder == 0:
            return prefix
        return f"{prefix} {self._convert_tens(remainder)}"

    def number_to_words(self, number: Union[int, float]) -> str:
        """Convert any number to Indonesian words."""        
        # Handle scientific notation by converting to int if possible
        if isinstance(number, float):
            if number.is_integer():
                number = int(number)
                integer_part = number
                decimal_part = ""
            else:
                integer_part, decimal_part = self._split_decimal(number)
                # Only add decimal part if it's not zero
                if decimal_part.rstrip('0'):
                    return f"{self.number_to_words(integer_part)} koma {' '.join(UNITS[int(d)] for d in decimal_part.rstrip('0'))}"
                return self.number_to_words(integer_part)
        else:
            integer_part, decimal_part = number, ""

        # Handle negative numbers first
        prefix = ""
        if integer_part < 0:
            prefix = "minus "
            integer_part = abs(integer_part)

        if integer_part == 0 and not decimal_part:
            result = "nol"
        else:
            groups = []
            if integer_part == 0:
                groups.append("nol")
            else:
                current = integer_part
                group_idx = 0

                while current > 0:
                    group = current % 1000
                    if group != 0:
                        prefix_word = self._convert_hundreds(group)
                        if group_idx > 0:
                            suffix = SCALES[group_idx]
                            if group == 1 and group_idx == 1:  # Special case for 1000
                                groups.insert(0, f"se{suffix}")
                            else:
                                groups.insert(0, f"{prefix_word} {suffix}")
                        else:
                            groups.insert(0, prefix_word)
                    current //= 1000
                    group_idx += 1

            result = " ".join(groups)

        if decimal_part:
            # Handle leading zeros in decimal part
            decimal_words = []
            for d in decimal_part:
                decimal_words.append(UNITS[int(d)])
            result += f" koma {' '.join(decimal_words)}"

        return prefix + result

    def convert_currency(self, amount: Union[int, float], currency: str = "IDR") -> str:
        """Convert currency amounts to words.
        
        Args:
            amount: The amount to convert
            currency: Currency code ('IDR', 'USD', or 'EUR')
            
        Returns:
            str: The amount in words with currency
            
        Examples:
            >>> normalizer.convert_currency(1500.50, "USD")
            'seribu lima ratus dolar lima puluh sen'
        """
        main_unit, sub_unit = CURRENCY_UNITS.get(currency, CURRENCY_UNITS["IDR"])

        if isinstance(amount, int):
            return f"{self.number_to_words(amount)} {main_unit}"

        # Handle decimal amount
        main, decimal_str = str(amount).split('.')
        main_words = self.number_to_words(int(main))
        
        if all(d == '0' for d in decimal_str):
            return f"{main_words} {main_unit}"
            
        # Convert decimal part using proper tens format
        decimal_val = int(decimal_str)
        if decimal_val < 10:
            decimal_val *= 10  # Convert single digit to tens
        decimal_words = self._convert_tens(decimal_val)
        
        return f"{main_words} {main_unit} {decimal_words} {sub_unit}"
    
    def convert_percentage(self, number: float) -> str:
        """Convert percentage to words.
        
        Args:
            number: The percentage to convert
            
        Returns:
            str: The percentage in words
            
        Examples:
            >>> normalizer.convert_percentage(2.5)
            'dua koma lima persen'
        """
        if isinstance(number, (int, float)):
            try:
                # Split into integer and decimal parts
                integer_part = int(number)
                decimal_str = f"{abs(number - integer_part):.10f}".strip('0').strip('.')
                
                # Build the words
                if number == int(number):
                    return f"{self.number_to_words(integer_part)} persen"
                else:
                    integer_words = self.number_to_words(integer_part)
                    decimal_words = " ".join(UNITS[int(d)] for d in decimal_str if d != '0')
                    return f"{integer_words} koma {decimal_words} persen"
            except (ValueError, decimal.InvalidOperation):
                return str(number)
        return str(number)

    def convert_ordinal(self, number: int) -> str:
        """Convert number to ordinal words.
        
        Args:
            number: The number to convert to ordinal
            
        Returns:
            str: The ordinal number in words
            
        Examples:
            >>> normalizer.convert_ordinal(3)
            'ketiga'
        """
        if number in ORDINAL_SPECIAL:
            return ORDINAL_SPECIAL[number]
        return f"ke{self.number_to_words(number)}"

    def convert_time(self, time_str: str) -> str:
        """Convert time string (HH:MM) to words.
        
        Args:
            time_str: Time string in HH:MM format
            
        Returns:
            str: The time in words
            
        Examples:
            >>> normalizer.convert_time("09:30")
            'sembilan lewat tiga puluh menit'
        """
        try:
            hours, minutes = map(int, time_str.split(":"))

            # Validate time
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                return time_str

            result = []

            # Convert hours to 12-hour format and determine period
            if hours == 0 or hours == 24:
                result.append("dua belas malam")
            elif hours == 12:
                result.append("dua belas siang")
            else:
                # Convert to 12-hour format
                hour_12 = hours if hours <= 12 else hours - 12
                result.append(self.number_to_words(hour_12))

            # Add minutes
            if minutes > 0:
                result.append(f"lewat {self.number_to_words(minutes)} menit")

            # Add period only if it's a complete time (no minutes)
            if minutes == 0 and hours != 0 and hours != 12:
                if hours < 12:
                    result.append("pagi")
                else:
                    result.append("sore")

            return " ".join(result)
        except:
            return time_str

    def find_numbers(self, text: str) -> List[NumberMatch]:
        """Find all numbers in text and their positions."""
        matches = []

        # Process patterns in order (percentage should be first to avoid partial matches)
        for pattern_type, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                match_start = match.start()
                match_end = match.end()
                
                # Skip if this position has already been matched
                if any(m.start <= match_start < m.end or 
                      m.start < match_end <= m.end for m in matches):
                    continue
                
                value = match.group()
                try:
                    if pattern_type == "currency":
                        # Remove 'Rp' and thousand separators, convert to float
                        num_str = value.replace("Rp", "").replace(".", "").replace(",", ".")
                        num_val = float(num_str)
                    elif pattern_type == "percentage":
                        # Handle percentage with comma decimal separator
                        num_str = value.rstrip('%').replace(",", ".")
                        num_val = float(num_str)
                    elif pattern_type == "decimal":
                        # Convert decimal comma to point
                        num_val = float(value.replace(",", "."))
                    elif pattern_type == "integer":
                        # Remove thousand separators
                        num_val = int(value.replace(".", ""))
                    else:  # time
                        num_val = value

                    matches.append(
                        NumberMatch(
                            original=value,
                            start=match_start,
                            end=match_end,
                            value=num_val,
                            type=pattern_type
                        )
                    )
                except (ValueError, decimal.InvalidOperation):
                    continue

        # Sort by position
        matches.sort(key=lambda x: x.start)
        return matches

    def convert_decimal_number(self, number: float) -> str:
        """Convert decimal number to words, ensuring consistent use of 'koma'.
        
        Args:
            number: The decimal number to convert
            
        Returns:
            str: The decimal number in words
            
        Examples:
            >>> normalizer.convert_decimal_number(5.5)
            'lima koma lima'
        """
        try:
            integer_part = int(number)
            decimal_str = f"{abs(number - integer_part):.10f}".strip('0').strip('.')
            
            if not decimal_str:  # No decimal part
                return self.number_to_words(integer_part)
            
            # Preserve leading zeros by getting the correct number of decimals
            original_decimal_str = str(number).split('.')[1]
            decimal_words = []
            for d in original_decimal_str:
                decimal_words.append(UNITS[int(d)])
            
            integer_words = self.number_to_words(integer_part)
            return f"{integer_words} koma {' '.join(decimal_words)}"
        except (ValueError, decimal.InvalidOperation):
            return str(number)

    def normalize_text(self, text: str) -> str:
        """Convert all numbers in text to their word representation.
        
        Args:
            text: Input text containing numbers
            
        Returns:
            str: Text with all numbers converted to words
        """
        matches = self.find_numbers(text)
        if not matches:
            return text

        # Process matches in reverse order
        result = text
        for match in reversed(matches):
            try:
                if match.type == "currency":
                    # Convert currency without using koma for the main amount
                    replacement = self.convert_currency(match.value)
                elif match.type == "percentage":
                    # Extract number from percentage value and convert
                    number = float(match.original.rstrip('%').replace(',', '.'))
                    replacement = f"{self.convert_decimal_number(number)} persen"
                elif match.type == "time":
                    replacement = self.convert_time(match.value)
                elif match.type == "decimal":
                    number = float(match.original.replace(',', '.'))
                    if match.original.startswith('-'):
                        replacement = f"minus {self.convert_decimal_number(abs(number))}"
                    else:
                        replacement = self.convert_decimal_number(number)
                elif match.type == "integer":
                    # Handle negative numbers
                    if match.original.startswith('-'):
                        replacement = f"minus {self.number_to_words(abs(match.value))}"
                    else:
                        replacement = self.number_to_words(match.value)

                result = result[:match.start] + replacement + result[match.end:]
            except (ValueError, decimal.InvalidOperation):
                continue

        return result


def create_normalizer() -> IndonesianNumberNormalizer:
    """Factory function to create a normalizer instance.
    
    Returns:
        IndonesianNumberNormalizer: A new instance of the normalizer
        
    Examples:
        >>> normalizer = create_normalizer()
        >>> normalizer.number_to_words(1234)
        'seribu dua ratus tiga puluh empat'
    """
    return IndonesianNumberNormalizer()
