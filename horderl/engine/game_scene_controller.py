from time import perf_counter
from typing import List

from tcod import libtcodpy as tcd

from horderl.config import Config

from ..engine import GameScene, palettes
from ..engine.component_manager import ComponentManager
from ..engine.core import log_debug
from ..engine.logging import get_logger
from ..engine.sound.default_sound_controller import DefaultSoundController
from ..gui.gui import Gui


class GameSceneController:
    """
    Finite State Machine (FSM) Controller for managing game scenes.

    This class serves as the central controller for the game's scene system,
    implementing a stack-based FSM architecture. It manages scene transitions,
    maintains the scene stack, and coordinates the game loop execution.

    The controller orchestrates the lifecycle of GameScene instances by:
    - Maintaining a stack of active scenes (Last-In-First-Out)
    - Handling scene transitions (push/pop)
    - Executing the main game loop for the active scene
    - Providing access to shared resources (GUI, components, sound)

    The scene at the top of the stack is considered the active scene and
    receives update, render, and input events during each game loop iteration.

    """

    @log_debug(__name__)
    def __init__(self, title: str, config: Config):
        """
        Initialize a new GameSceneController instance.

        Creates a new controller with an empty scene stack and initializes
        all required subsystems (GUI, component manager, sound).

        Args:
            title (str): The title of the game window that will be displayed
                         in the window caption/title bar.

        Attributes:
            title (str): The game window title.
            gui (Gui): The graphical user interface manager for rendering.
            cm (ComponentManager): Manages game components and their interactions.
            sound (DefaultSoundController): Controls game audio.
            _scene_stack (List[GameScene]): Stack of active game scenes with the
                                           most recent scene at the top.

        """
        self.title: str = title
        self.config = config
        palettes.apply_config(config)
        self.gui: Gui = Gui(
            config.screen_width,
            config.screen_height,
            title=self.title,
            font_path=config.font,
        )
        self.cm = ComponentManager()
        self.sound = DefaultSoundController()
        self._scene_stack: List[GameScene] = []
        self.logger = get_logger(__name__)
        self.logger.debug(
            "GameSceneController instantiated", extra={"title": self.title}
        )

    @log_debug(__name__)
    def push_scene(self, scene: GameScene):
        """
        Add a new scene to the top of the scene stack and make it active.

        This method performs the following actions:
        1. Loads the scene by providing references to controller, component manager,
           GUI, and sound systems
        2. Initializes all GUI elements associated with the scene
        3. Adds the scene to the top of the stack, making it the active scene

        The previously active scene remains in the stack but becomes inactive
        until the new scene is popped.

        Args:
            scene (GameScene): The scene instance to push onto the stack and activate.

        """
        scene.load(self, self.cm, self.gui, self.sound)
        for gui_element in scene.gui_elements:
            gui_element.on_load()
        self._scene_stack.append(scene)
        self.logger.info(
            f"Scene pushed: {scene.__class__.__name__}",
            extra={
                "scene_type": scene.__class__.__name__,
                "stack_size": len(self._scene_stack),
                "action": "push_scene",
            },
        )

    @log_debug(__name__)
    def pop_scene(self):
        """
        Remove and return the top scene from the scene stack.

        This method:
        1. Removes the current active scene from the top of the stack
        2. Calls its on_unload method to perform cleanup
        3. Returns the removed scene

        After popping, the next scene in the stack (if any) becomes the active scene.

        Returns:
            GameScene: The scene that was removed from the stack.

        Note:
            Will raise IndexError if the stack is empty.

        """
        scene = self._scene_stack.pop()
        scene.on_unload()
        self.logger.info(
            f"Scene popped: {scene.__class__.__name__}",
            extra={
                "scene_type": scene.__class__.__name__,
                "stack_size": len(self._scene_stack),
                "action": "pop_scene",
            },
        )
        return scene

    @log_debug(__name__)
    def clear_scenes(self):
        """
        Remove all scenes from the scene stack.

        Completely empties the scene stack, effectively terminating any running
        game states. This is typically used during game shutdown or when
        transitioning between major game modes (e.g., from gameplay to main menu).

        Note:
            This method does not call on_unload() on the scenes being cleared.
            If cleanup is needed, pop_scene() should be called for each scene
            individually before using this method.

        """
        stack_size = len(self._scene_stack)
        self._scene_stack.clear()
        self.logger.info(
            f"Scene stack cleared, removed {stack_size} scenes",
            extra={"previous_size": stack_size, "action": "clear_scenes"},
        )

    @log_debug(__name__)
    def start(self):
        """
        Invoke the FSM execution and run the main game loop.

        This method starts the main game loop that continues until the scene stack
        is empty. For each iteration of the loop, it:

        1. Gets the current active scene from the top of the stack
        2. Calls before_update() to prepare the scene for the current frame
        3. Calls update() to process game logic, input, and state changes
        4. Calls render() to draw the scene to the screen
        5. Flushes the console to display the rendered frame

        The loop continues until either:
        - The scene stack becomes empty (all scenes are popped)
        - A scene explicitly terminates execution (e.g., by calling sys.exit())

        This method coordinates the execution flow between scenes and ensures
        proper sequencing of the update and render cycles according to the
        FSM design pattern.

        """
        self.logger.info(
            "Starting game scene controller main loop",
            extra={"action": "start", "stack_size": len(self._scene_stack)},
        )
        last_frame_time = perf_counter()
        while self._scene_stack:
            current_scene = self._scene_stack[-1]
            scene_name = current_scene.__class__.__name__
            now = perf_counter()
            dt = now - last_frame_time
            last_frame_time = now

            self.logger.debug(
                f"Processing frame for scene: {scene_name}",
                extra={
                    "scene_type": scene_name,
                    "stack_position": len(self._scene_stack) - 1,
                    "phase": "before_frame",
                },
            )

            current_scene.before_update(dt)
            current_scene.update(dt)
            current_scene.render(dt)
            tcd.console_flush()
