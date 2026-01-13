from types import SimpleNamespace

import pytest

from horderl.gui.help_dialogue import HelpDialogue
from horderl.engine_adapter import core

pytest.importorskip("tcod")
import tcod.event


def test_help_dialogue_advances_and_closes(monkeypatch):
    messages = ["First message", "Second message"]
    config = SimpleNamespace(
        inventory_width=20, screen_width=60, screen_height=40
    )
    dialogue = HelpDialogue(messages, config)

    assert dialogue.menu.header == "First message [ENTER]"

    events = iter(
        [
            SimpleNamespace(sym=tcod.event.KeySym.RETURN),
            SimpleNamespace(sym=tcod.event.KeySym.RETURN),
        ]
    )

    monkeypatch.setattr(core, "get_key_event", lambda: next(events))

    dialogue.update(None, 0.0)
    assert dialogue.menu.header == "Second message [ENTER]"
    assert dialogue.is_closed is False

    dialogue.update(None, 0.0)
    assert dialogue.is_closed is True
