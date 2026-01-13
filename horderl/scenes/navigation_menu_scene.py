import sys
from collections import OrderedDict

from horderl.engine import GameScene
from horderl import palettes
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

    def before_update(self, dt: float):
        """
        Pre-render GUI elements before the menu is displayed.

        This method ensures that all GUI elements (like the title) are rendered before
        the interactive menu is shown. This is important because the EasyMenu component
        will pause execution while waiting for player input, and we want the title and
        other elements to be visible during this time.

        The method captures the controller's GUI context and triggers a render pass
        before the update cycle continues.

        """
        # pre-render the gui elements so that they show up before menu pauses
        # execution
        self.gui = self.controller.gui
        self.render(dt)

    def update(self, dt: float):
        """
        Show the interactive menu and wait for player selection.

        This method creates and displays an EasyMenu component populated with
        the options provided during initialization. Each menu option is linked
        to a callback function that will push the corresponding scene onto
        the controller's scene stack when selected.

        The menu is configured to:
        - Display in a centered position (y=24)
        - Show a background
        - Exit the game when the Escape key is pressed

        The method blocks until the player makes a selection or exits.

        """
        self.add_gui_element(
            EasyMenu(
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
        )

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
        self.sound.play("theme")
