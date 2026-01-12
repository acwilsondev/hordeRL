import json

import pytest

from horderl import i18n


def _write_locale(tmp_path, locale, data):
    locale_path = (
        tmp_path / "resources" / "locales" / f"{locale}.json"
    )
    locale_path.parent.mkdir(parents=True, exist_ok=True)
    locale_path.write_text(json.dumps(data))
    return locale_path


def _patch_resource_path(monkeypatch, tmp_path):
    def fake_resource_path(relative_path):
        return tmp_path / relative_path

    monkeypatch.setattr(i18n, "resource_path", fake_resource_path)


def test_load_locale_falls_back_to_default(monkeypatch, tmp_path):
    _write_locale(tmp_path, "en", {"greeting": "Hello"})
    _patch_resource_path(monkeypatch, tmp_path)

    i18n.load_locale("fr")

    assert i18n.t("greeting") == "Hello"


def test_t_formats_kwargs(monkeypatch, tmp_path):
    _write_locale(tmp_path, "en", {"welcome": "Welcome, {name}!"})
    _patch_resource_path(monkeypatch, tmp_path)

    i18n.load_locale("en")

    assert i18n.t("welcome", name="Traveler") == "Welcome, Traveler!"


def test_t_returns_key_when_missing(monkeypatch, tmp_path):
    _write_locale(tmp_path, "en", {})
    _patch_resource_path(monkeypatch, tmp_path)

    i18n.load_locale("en")

    assert i18n.t("missing.key") == "missing.key"
