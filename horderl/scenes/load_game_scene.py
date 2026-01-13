import os

from horderl import palettes
from engine import GameScene
from horderl.gui.easy_menu import EasyMenu
from horderl.gui.labels import Label
from horderl.i18n import t
from horderl.scenes.defend_scene import DefendScene


class LoadMenuScene(GameScene):
    """
    Show a menu with links to other scenes.
    """

    def __init__(self):
        super().__init__()
        self.title = t("menu.load_title")
        self.title_label = None

    def on_load(self):
        center_x = (self.config.screen_width - len(self.title)) // 2
        center_y = self.config.screen_height // 2 - 4
        self.title_label = Label(
            center_x, center_y, self.title, fg=palettes.FRESH_BLOOD
        )
        self.add_gui_element(self.title_label)

    def before_update(self, dt: float):
        # pre-render the gui elements so that they show up before menu pauses
        # execution
        self.gui = self.controller.gui
        self.render()

    def update(self, dt: float):
        """
        Show the menu and wait for player selection.
        """
        files = []

        for file in os.listdir("."):
            if file.endswith(".world"):
                files.append(file)

        self.gui.add_element(
            EasyMenu(
                t("menu.load_prompt"),
                {world: self.get_world_loader(world) for world in files},
                self.config.inventory_width,
                self.config,
                on_escape=self.pop(),
            )
        )

    def get_world_loader(self, file_name):
        def out_fn():
            self.load_world(file_name)

        return out_fn

    def load_world(self, file_name):
        self.pop()
        self.controller.push_scene(DefendScene(from_file=file_name))
