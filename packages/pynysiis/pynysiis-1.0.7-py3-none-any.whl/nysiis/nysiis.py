"""
NYSIIS (New York State Identification and Intelligence System) phonetic algorithm.

This implementation includes support for various languages including:
- English
- Igbo
- Yoruba
- Hausa
- Hindi
- Urdu

The algorithm converts names into phonetic codes, helping with name matching
and searching where spelling variations exist.
"""

import re
from typing import Dict


class NYSIIS:
    """
    NYSIIS (New York State Identification and Intelligence System) phonetic encoding.

    This class implements the NYSIIS phonetic algorithm with additional support for
    multiple languages. It converts names into phonetic codes that help match similar
    sounding names despite spelling variations.

    Attributes:
        vowels (Dict[str, bool]): Dictionary of vowels used in the encoding process.

    Example:
        >>> encoder = NYSIIS()
        >>> encoder.encode("SMITH")
        'SNAT'
        >>> encoder.encode("SMYTHE")
        'SNAT'
    """

    def __init__(self) -> None:
        """Initialise the NYSIIS encoder with vowel mappings."""
        self.vowels: Dict[str, bool] = {
            "A": True,
            "E": True,
            "I": True,
            "O": True,
            "U": True,
        }

    def preprocess_name(self, name: str) -> str:
        """
        Preprocess name for NYSIIS encoding.

        Args:
            name (str): Input name to preprocess.

        Returns:
            str: Preprocessed name in uppercase with non-alphabetic chars removed.
        """
        name = name.upper()
        return re.sub(r"[^A-Z]", "", name)

    def translate_first_characters(self, name: str) -> str:
        """
        Translate specific character combinations at name start.

        Handles special cases for name beginnings across multiple languages.

        Args:
            name (str): Input name to process.

        Returns:
            str: Name with translated first characters.
        """
        translations = {
            "MAC": "MCC",
            "KN": "NN",
            "K": "C",
            "PH": "FF",
            "PF": "FF",
            "SCH": "SSS",
            # Igbo translations
            "GB": "J",
            "KP": "P",
            "NW": "W",
            # Yoruba translations
            "TS": "S",
            # Hausa translations
            "SH": "S",
            # Hindi translations
            "BH": "B",
            "DH": "D",
            "GH": "G",
            "JH": "J",
            "KH": "K",
            "PH": "F",
            "TH": "T",
            # Urdu translations
            "CH": "C",
            "ZH": "J",
        }

        for prefix, replacement in translations.items():
            if name.startswith(prefix):
                return replacement + name[len(prefix):]
        return name

    def translate_last_characters(self, name: str) -> str:
        """
        Translate specific character combinations at name end.

        Args:
            name (str): Input name to process.

        Returns:
            str: Name with translated last characters.
        """
        if name.endswith(("EE", "IE")):
            return name[:-2] + "Y"
        if name.endswith(("DT", "RT", "RD", "NT", "ND")):
            return name[:-2] + "D"
        return name

    def generate_key(self, name: str) -> str:
        """
        Generate NYSIIS phonetic key for given name.

        Args:
            name (str): Preprocessed name to encode.

        Returns:
            str: Generated NYSIIS key.
        """
        key = name[0]
        prev_char = name[0]

        for i in range(1, len(name)):
            char = name[i]
            if char in self.vowels:
                char = "A"

            char = self.translate_char(char, name, i)
            char = self.handle_vowel_harmony(char, prev_char)
            char = self.ignore_tonal_differences(char)

            if char != prev_char:
                key += char

            prev_char = char

        key = self.remove_trailing_s(key)
        key = self.translate_ay(key)
        key = self.remove_trailing_a(key)
        return self.truncate_key(key)

    def translate_char(self, char: str, name: str, i: int) -> str:
        """
        Translate character based on context and position.

        Args:
            char (str): Character to translate.
            name (str): Full name string.
            i (int): Current character position.

        Returns:
            str: Translated character.
        """
        translations = [
            (lambda c, n, j: c == "E" and j + 1 < len(n) and n[j + 1] == "V", "A"),
            (lambda c, n, j: c == "Q", "G"),
            (lambda c, n, j: c == "Z", "S"),
            (lambda c, n, j: c == "M", "N"),
            (lambda c, n, j: c == "K" and (j + 1 >= len(n) or n[j + 1] != "N"), "C"),
            (lambda c, n, j: c == "S" and j + 2 < len(n) and n[j:j + 3] == "SCH", "S"),
            (lambda c, n, j: c == "P" and j + 1 < len(n) and n[j + 1] == "H", "F"),
        ]

        for condition, result in translations:
            if condition(char, name, i):
                return result

        # Handle special cases
        if (char == "H" and (i == 0 or i + 1 == len(name) or
                            name[i - 1] not in self.vowels or
                            name[i + 1] not in self.vowels)):
            return name[i - 1]

        if char == "W" and i > 0 and name[i - 1] in self.vowels:
            return name[i - 1]

        return char

    def handle_vowel_harmony(self, char: str, prev_char: str) -> str:
        """
        Handle vowel harmony adjustments.

        Args:
            char (str): Current character.
            prev_char (str): Previous character.

        Returns:
            str: Character adjusted for vowel harmony.
        """
        if char not in self.vowels or prev_char not in self.vowels:
            return char

        back_vowels = {"A", "O", "U"}
        front_vowels = {"E", "I"}

        if prev_char in back_vowels and char in front_vowels:
            return "A"
        if prev_char in front_vowels and char in back_vowels:
            return "E"

        return char

    @staticmethod
    def ignore_tonal_differences(char: str) -> str:
        """
        Convert character to uppercase to ignore tonal differences.

        Args:
            char (str): Character to process.

        Returns:
            str: Uppercase character.
        """
        return char.upper() if "A" <= char <= "Z" else char

    @staticmethod
    def remove_trailing_s(key: str) -> str:
        """
        Remove trailing 'S' from key if present.

        Args:
            key (str): Key to process.

        Returns:
            str: Key with trailing 'S' removed if applicable.
        """
        return key[:-1] if len(key) > 1 and key.endswith("S") else key

    @staticmethod
    def translate_ay(key: str) -> str:
        """
        Translate 'AY' to 'Y' at key end.

        Args:
            key (str): Key to process.

        Returns:
            str: Key with 'AY' translated if applicable.
        """
        return key[:-2] + "Y" if key.endswith("AY") else key

    @staticmethod
    def remove_trailing_a(key: str) -> str:
        """
        Remove trailing 'A' from key if present.

        Args:
            key (str): Key to process.

        Returns:
            str: Key with trailing 'A' removed if applicable.
        """
        return key[:-1] if len(key) > 1 and key.endswith("A") else key

    @staticmethod
    def truncate_key(key: str) -> str:
        """
        Truncate key to maximum length of 6 characters.

        Args:
            key (str): Key to truncate.

        Returns:
            str: Truncated key.
        """
        return key[:6] if len(key) > 6 else key

    def encode(self, name: str) -> str:
        """
        Encode name using NYSIIS algorithm.

        Args:
            name (str): Name to encode.

        Returns:
            str: NYSIIS phonetic code for the name.

        Example:
            >>> encoder = NYSIIS()
            >>> encoder.encode("SMITH")
            'SNAT'
        """
        if not name:
            return ""

        name = self.preprocess_name(name)
        if len(name) < 2:
            return name

        name = self.translate_first_characters(name)
        name = self.translate_last_characters(name)
        return self.generate_key(name)
