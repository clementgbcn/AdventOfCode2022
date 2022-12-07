import functools
import re

from Day import Day

INT_PATTERN = re.compile(r"\d+")


def extract_int(sentence):
    return list(map(int, INT_PATTERN.findall(sentence)))
