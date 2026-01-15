import sys
from collections import OrderedDict

from horderl import palettes
from horderl.engine_adapter import GameScene
from horderl.gui.easy_menu import EasyMenu
from horderl.gui.labels import Label


class NavigationMenuScene(GameScene):
    """
    A menu system scene that displays navigational options to the player.

    This scene acts as a hub for navigation between different game scenes by presenting
    the player with a menu of options. Each option in the menu corresponds to a
    different scene that can be loaded. The scene handles player input, allowing them to
    select options or exit the game.

    The NavigationMenuScene leverages the EasyMenu component to create an interactive
    menu with customizable options, visual styling, and event handling.

    """

    def __init__(self, title: str, option_scene_map: OrderedDict):
        """
        Initialize the navigation menu with a title and scene options.

        Parameters:
            title (str): The title text to display at the top of the menu.
            option_scene_map (OrderedDict): A mapping of option labels to their
                                           corresponding scene objects. The keys are
                                           displayed as menu options, and the values
                                           are the scenes to push onto the stack when
                                           the option is selected.

        The constructor centers the title on screen and stores the options for
        later use when building the interactive menu. The title is displayed with
        a blood-red color scheme.

        """
        super().__init__()
        self.title = title
        self.options = option_scene_map
        self.title_label = None
        self.menu = None

    def update(self, dt_ms: int):
        """
        Update hook for the navigation scene.

        Ensures the menu is present after returning from a child scene.

        The menu is handled as a persistent GUI element, but selecting an option
        closes it before pushing the next scene. When that child scene is popped,
        the menu needs to be recreated.
        """
        if self.menu is None or self.menu.is_closed:
            self._build_menu()

    def get_push_scene(self, scene):
        """
        Create a callback function that pushes a scene onto the controller stack.

        This helper method generates a closure function that, when called, will
        push the specified scene onto the controller's scene stack. This is used
        to create callback functions for each menu option.

        Parameters:
            scene (GameScene): The scene to push onto the stack when the callback
                              is invoked.

        Returns:
            callable: A function that, when called, pushes the scene onto the
                     controller's scene stack.

        """

        def out_fn():
            self.controller.push_scene(scene)

        return out_fn

    def on_load(self):
        """
        Initialize the scene when it's loaded.

        This lifecycle method is called when the scene is first loaded. It plays the
        theme music to set the atmosphere for the menu. This is part of the scene's
        initialization sequence and runs before the update cycle begins.

        """
        center_x = (self.config.screen_width - len(self.title)) // 2
        center_y = self.config.screen_height // 2 - 4
        self.title_label = Label(
            center_x, center_y, self.title, fg=palettes.FRESH_BLOOD
        )
        self.add_gui_element(self.title_label)
        self._build_menu()
        self.sound.play("theme")

    def _build_menu(self) -> None:
        # Menu selection closes the menu before pushing a new scene, so we keep a
        # handle to recreate it when returning to this scene.
        self.menu = EasyMenu(
            "",
            {
                link[0]: self.get_push_scene(link[1])
                for link in self.options.items()
            },
            24,
            self.config,
            hide_background=False,
            on_escape=lambda: sys.exit(0),
        )
        self.add_gui_element(self.menu)
