import json
import os
from typing import Any, Dict

from horderl.config import resource_path

_DEFAULT_LOCALE = "en"
_ACTIVE_LOCALE = _DEFAULT_LOCALE
_TRANSLATIONS: Dict[str, Any] = {}


def _load_translation_file(locale_code: str) -> Dict[str, Any]:
    path = resource_path(f"resources/locales/{locale_code}.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Locale file {path} must contain a JSON object")
    return data


def load_locale(locale_code: str | None) -> None:
    """Load translations for the requested locale code."""
    global _ACTIVE_LOCALE
    global _TRANSLATIONS

    requested = (locale_code or _DEFAULT_LOCALE).strip() or _DEFAULT_LOCALE
    translations = _load_translation_file(requested)
    if not translations and requested != _DEFAULT_LOCALE:
        requested = _DEFAULT_LOCALE
        translations = _load_translation_file(requested)

    _ACTIVE_LOCALE = requested
    _TRANSLATIONS = translations


def t(key: str, **kwargs: Any) -> str:
    """Translate a key using the active locale."""
    if not _TRANSLATIONS:
        load_locale(_ACTIVE_LOCALE)
    value = _TRANSLATIONS.get(key, key)
    if kwargs:
        try:
            return str(value).format(**kwargs)
        except KeyError:
            return str(value)
    return str(value)
