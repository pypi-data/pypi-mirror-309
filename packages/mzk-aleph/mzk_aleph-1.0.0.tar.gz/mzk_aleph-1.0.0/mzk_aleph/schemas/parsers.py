import re
from typing import Optional
from ..datatypes import MaterialType

MATERIAL_TYPE_MAPPING = {
    "BK": MaterialType.Book,
    "CR": MaterialType.ContinuingResource,
    "SE": MaterialType.ContinuingResource,
    "MP": MaterialType.Map,
    "MU": MaterialType.Music,
    "GP": MaterialType.Graphic,
}

PAGE_COUNT_FORMAT = (
    r"^\s*(?:\[?(?:XC|xc|XL|xl|L?X{0,3}|l?x{0,3})"
    r"(?:IX|ix|IV|iv|V?I{0,3}|v?i{0,3})\]?\s*[,-]\s*)?"
    r"\[?(\d+)\]?\s*"
    r"(?:[,-]\s*\[?(?:\d+|(?:XC|xc|XL|xl|L?X{0,3}|l?x{0,3})"
    r"(?:IX|ix|IV|iv|V?I{0,3}|v?i{0,3}))\]?)?\s*"
    r"(s\.|l\.|stran).*"
)
VOLUME_PAGE_COUNTS_PATTERN = (
    r"^\s*\d+\s+(?:sv\.|svazky)\s+[\(\[]((?:\d+[,;]?\s+)+\s*s\.)[\)\]]"
)
VOLUME_NUMBER_PATTERNS = (
    r"^\s*(\d+)[.,]",
    r"(\d+)[.,]\s*$",
)
VOLUME_NUMBER_ROMANS_PATTERN = r"^\s*(IX|ix|IV|iv|V?I{0,3}|v?i{0,3})[.,]"
ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
}


def roman_to_int(roman: str):
    integer_value = 0
    for i in range(len(roman)):
        if (
            i + 1 < len(roman)
            and ROMAN_VALUES[roman[i]] < ROMAN_VALUES[roman[i + 1]]
        ):
            integer_value -= ROMAN_VALUES[roman[i]]
        else:
            integer_value += ROMAN_VALUES[roman[i]]
    return integer_value


def parse_page_count(
    extent: Optional[str], volume: Optional[str] = None
) -> Optional[int]:
    if extent is None:
        return None
    if volume is None:
        match = re.search(PAGE_COUNT_FORMAT, extent)
        return int(match.group(1)) if match else None

    match = re.search(VOLUME_NUMBER_ROMANS_PATTERN, volume)
    if match:
        number = roman_to_int(match.group(1)) - 1
    else:
        for pattern in VOLUME_NUMBER_PATTERNS:
            match = re.search(pattern, volume)
            if match:
                number = int(match.group(1)) - 1
                break
        else:
            return None

    match = re.match(VOLUME_PAGE_COUNTS_PATTERN, extent)
    if not match:
        return None
    inner_content = match.group(1)
    numbers = re.findall(r"\d+", inner_content)
    return int(numbers[number]) if 0 <= number < len(numbers) else None


def parse_material_type(
    material_type: Optional[str],
) -> MaterialType:
    return MATERIAL_TYPE_MAPPING.get(material_type, MaterialType.Other)
