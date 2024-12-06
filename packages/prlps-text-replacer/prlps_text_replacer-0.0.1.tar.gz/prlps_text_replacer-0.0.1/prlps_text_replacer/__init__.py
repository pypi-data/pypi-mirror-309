from functools import lru_cache
from re import IGNORECASE, Match, Pattern, UNICODE, compile, escape


@lru_cache(maxsize=None)
def compile_pattern(replacements_keys: tuple[str, ...]) -> Pattern[str]:
    sorted_keys = sorted(replacements_keys, key=len, reverse=True)
    pattern = compile('|'.join(escape(key) for key in sorted_keys), IGNORECASE | UNICODE)
    return pattern


def transform_case(original_substring: str, replacement_substring: str) -> str:
    if original_substring.islower():
        return replacement_substring.lower()
    elif original_substring.isupper():
        return replacement_substring.upper()
    elif original_substring.istitle():
        return replacement_substring.title()
    else:
        result = []
        for o, r in zip(original_substring, replacement_substring):
            result.append(r.upper() if o.isupper() else r.lower())
        result.extend(replacement_substring[len(original_substring):])
        return ''.join(result)


def replacement(match: Match[str], replacements: dict[str, list[tuple[str, str]]]):
    matched_text = match.group(0)
    lower_text = matched_text.lower()
    if lower_text in replacements:
        for original_key, value in replacements[lower_text]:
            if original_key == matched_text:
                return transform_case(matched_text, value)
    return matched_text


def text_replace_by_dict(text: str, replacements: dict[str, str]) -> str:
    if text is None or replacements is None:
        raise TypeError('text и replacements не могут быть `None`')

    replacements_dict = {}
    for key, value in replacements.items():
        lower_key = key.lower()
        if lower_key not in replacements_dict:
            replacements_dict[lower_key] = []
        replacements_dict[lower_key].append((key, value))

    sorted_keys = tuple(sorted(replacements, key=len, reverse=True))
    pattern = compile_pattern(sorted_keys)
    return pattern.sub(lambda match: replacement(match, replacements_dict), text)
