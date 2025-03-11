import sys

from ..engine import GameScene


class QuitScene(GameScene):
    """
    A terminal scene that gracefully exits the game.

    This scene serves as the final endpoint in the game's scene flow. When
    loaded and updated, it immediately terminates the game process with a
    clean exit. This scene is typically pushed onto the scene stack when
    the player chooses to quit the game from a menu or when the game reaches
    a natural conclusion.

    Unlike most scenes that have complex update logic and rendering, this
    scene has a single purpose: to exit the game safely.
    """

    def __init__(self):
        """
        Initialize the QuitScene.

        The constructor simply calls the parent GameScene constructor.
        No additional initialization is needed as this scene has minimal
        functionality.
        """
        super().__init__()

    def update(self):
        """
        Perform the scene's update logic, which exits the game.

        This method is called once during the scene's lifecycle. It
        immediately calls sys.exit() to terminate the game process
        with a standard successful exit code (0 by default).

        No rendering or further processing occurs after this method
        is called.
        """
        sys.exit()
