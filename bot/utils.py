import re

HOMOGLYPH_MAP = {
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M',
    'Н': 'H', 'О': 'O', 'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'У': 'Y',
    'а': 'a', 'в': 'b', 'е': 'e', 'к': 'k', 'м': 'm',
    'н': 'h', 'о': 'o', 'р': 'p', 'с': 'c', 'т': 't', 'х': 'x', 'у': 'y',
}

PLATE_PATTERN = re.compile(r'^[A-Z]{1,3}\d{2,5}[A-Z]{0,3}$', re.IGNORECASE)

def normalize_plate(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', '', text)
    text = text.upper()
    normalized_chars = []
    for char in text:
        normalized_chars.append(HOMOGLYPH_MAP.get(char, char))
    text = "".join(normalized_chars)
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text

def validate_plate_format(text: str) -> bool:
    if not text:
        return False
    if not PLATE_PATTERN.match(text):
        return False
    normalized = normalize_plate(text)
    return 5 <= len(normalized) <= 10
