from horderl.engine_adapter import GuiElement, core

from .easy_menu import EasyMenu


class HelpDialogue(GuiElement):
    def __init__(self, messages, config):
        super().__init__(0, 0)
        self.messages = list(messages)
        self.config = config
        self.index = 0
        self.menu = EasyMenu(
            self._current_message(),
            {},
            self.config.inventory_width,
            self.config,
            return_only=True,
        )
        self.modal = True

    def _current_message(self):
        return f"{self.messages[self.index]} [ENTER]"

    def update(self, scene, dt_ms: int) -> None:
        import tcod.event

        key_event = core.get_key_event()
        if key_event is None:
            return

        if int(key_event.sym) == tcod.event.KeySym.RETURN:
            if self.index + 1 < len(self.messages):
                self.index += 1
                self.menu.header = self._current_message()
                return
            self.close()

    def render(self, panel):
        self.menu.render(panel)
