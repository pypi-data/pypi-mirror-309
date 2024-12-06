import os
import re


FR_DICTIONARY = "fr_dictionary.txt"


class Normalizer:
    """
    Utility to normalize a full postal address

    IMPORTANT: It does not validate the input format, only transforms it
    """

    dictionary = dict()

    def __init__(self, filepath: str = None):
        if not filepath:
            filepath = os.path.join(os.path.dirname(__file__), FR_DICTIONARY)
        with open(filepath, "r") as f:
            for line in f:
                [word, substitution] = line.split("\t", 2)
                self.dictionary[word] = substitution

    def normalize(self, address: str) -> str:
        """
        Returns the normalized address
        """
        return normalize(address, self.dictionary)


def normalize(address: str, dictionary: dict) -> str:
    """
    Returns a full address normalized using the passed dictionary
    """
    normalized = re.sub(r"[\s\.,;:\/\\'\"\-_\(\)$+=]+", " ", address.lower()).strip()
    normalized = normalized.translate(
        str.maketrans("àäãâçéèêëìïôöòùûü", "aaaaceeeeiiooouuu")
    )
    return substitute(normalized, dictionary)


def substitute(input: str, dictionary: dict) -> str:
    words = input.split(" ")
    output = []
    for word in words:
        output.append(dictionary[word] if word in dictionary.keys() else word)
    return re.sub(r"\s+", " ", " ".join(output)).strip()
