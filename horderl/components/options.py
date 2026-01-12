from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Options(Component):
    """
    A component that stores user interface and gameplay options for the game.

    This class inherits from the base Component class and provides configuration options
    that control various aspects of the game's presentation and behavior.

    """

    show_breadcrumbs: bool = False
    """
    Controls whether navigation breadcrumbs are displayed in the user interface.
    """
