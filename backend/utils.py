from typing import List


def camel_case_to_title_case(elements: List[str]) -> List[str]:
    """Return a list of camel cased words as splitted title case.

    e.g.: newWorld -> New World
    """
    new_elements = []
    for word in elements:
        new_word = ""
        for idx, letter in enumerate(word):
            if letter.isupper():
                new_word += " " + letter
            elif idx == 0:
                new_word += letter.title()
            else:
                new_word += letter
        new_elements.append(new_word)
    return new_elements
