from engine.component_manager import ComponentManager
from horderl.components.show_debug import ShowDebug
from horderl.systems.debug_menu import run as run_debug_menu


class DummyConfig:
    inventory_width = 30


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()
        self.config = DummyConfig()
        self.gui_elements = []
        self.player = 1
        self.gold = 0

    def add_gui_element(self, element) -> None:
        self.gui_elements.append(element)


def test_debug_menu_system_adds_menu_and_clears_component():
    scene = DummyScene()
    scene.cm.add(ShowDebug(entity=scene.player))

    run_debug_menu(scene)

    assert len(scene.gui_elements) == 1
    assert scene.gui_elements[0].__class__.__name__ == "EasyMenu"
    assert scene.cm.get(ShowDebug) == []
