import unittest

from engine.ui.gui_adapter import GuiAdapter


class DummyRoot:
    def __init__(self) -> None:
        self.cleared = False

    def clear(self) -> None:
        self.cleared = True


class DummyGui:
    def __init__(self) -> None:
        self.root = DummyRoot()
        self.added = []

    def add_element(self, element) -> None:
        self.added.append(element)


class DummyElement:
    def __init__(self) -> None:
        self.rendered_with = None

    def render(self, panel) -> None:
        self.rendered_with = panel


class DummyConfig:
    screen_width = 80
    screen_height = 50
    inventory_width = 20


class DummyPopup:
    def __init__(self, message, config):
        self.message = message
        self.config = config


class TestGuiAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.gui = DummyGui()
        self.adapter = GuiAdapter(
            self.gui,
            popup_factory=lambda message, config: DummyPopup(message, config),
        )

    def test_clear_root(self) -> None:
        self.assertFalse(self.gui.root.cleared)
        self.adapter.clear_root()
        self.assertTrue(self.gui.root.cleared)

    def test_render_element(self) -> None:
        element = DummyElement()
        self.adapter.render_element(element)
        self.assertIs(element.rendered_with, self.gui.root)

    def test_render_single_shot(self) -> None:
        element = DummyElement()
        self.adapter.render_single_shot(element)
        self.assertIs(element.rendered_with, self.gui.root)
        self.assertEqual(self.gui.added, [])

    def test_create_popup(self) -> None:
        popup = self.adapter.create_popup("Hello", DummyConfig())
        self.assertIsInstance(popup, DummyPopup)
        self.assertEqual(popup.message, "Hello")


if __name__ == "__main__":
    unittest.main()
