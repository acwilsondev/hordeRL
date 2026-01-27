from typing import TYPE_CHECKING, Any, final

from engine import serialization
from engine.component_manager import ComponentManager
from engine.logging import get_logger
from engine.sound.sound_controller import SoundController
from engine.ui_context import UiContext

if TYPE_CHECKING:
    from engine.game_scene_controller import GameSceneController


class GameScene:
    """
    Base class for all game scenes in the hordeRL game engine.

    The GameScene class serves as the foundation for scene management within the game,
    providing a structured lifecycle for initialization, updates, rendering, and cleanup.
    Each specific game scene (like menus, gameplay screens, etc.) should inherit from this
    class and override the lifecycle hooks as needed.

    Lifecycle Hooks (in execution order):
    1. on_load: Called when the scene is first loaded
    2. before_update: Called at the beginning of each frame before update logic
    3. update: Called each frame to perform game logic
    4. render: Called each frame to display the scene
    5. on_unload: Called when transitioning away from this scene

    The class also manages GUI elements and provides methods for scene transitions,
    as well as game state serialization.

    """

    def __init__(self):
        """
        Initialize a new GameScene instance.

        Sets up empty GUI element list and initializes core component references. The
        controller, GUI, and sound references will be populated when the scene is loaded
        through the load() method.

        """
        self.gui_elements = []
        self.cm: ComponentManager = ComponentManager()
        self.controller = None
        self.gui = None
        self.ui_context: UiContext | None = None
        self.sound = None
        self.config = None
        self.logger = get_logger(f"{self.__class__.__name__}")

    def add_gui_element(self, element: Any):
        """
        Add a GUI element to the scene.

        This method handles both persistent and single-shot (temporary) GUI elements differently:
        - Single-shot elements (like popups or temporary menus) are rendered immediately
        - Persistent elements are added to the gui_elements list for later rendering in the render() method

        Parameters:
            element (GuiElement): The GUI element to add to the scene

        """
        if element.single_shot:
            # if it's a single shot (menu or popup message), we need to render it directly to the existing window
            self.logger.debug(
                "Rendering single-shot GUI element:"
                f" {element.__class__.__name__}"
            )
            if self.ui_context is None:
                raise RuntimeError(
                    "UI context is not configured for this scene."
                )
            self.ui_context.render_single_shot(element)
        else:
            self.logger.debug(
                f"Adding persistent GUI element: {element.__class__.__name__}"
            )
            self.gui_elements.append(element)

    def has_modal_gui(self) -> bool:
        return any(
            element.modal and not element.is_closed
            for element in self.gui_elements
        )

    def popup_message(self, message: str):
        """
        Display a popup message to the user.

        Creates a PopupMessage GUI element with the given message text and adds it to the scene.
        This is a convenience method for showing quick notifications to the player.

        Parameters:
            message (str): The text message to display in the popup

        """
        self.logger.info(f"Displaying popup message: {message}")
        if self.ui_context is None:
            raise RuntimeError("UI context is not configured for this scene.")
        self.add_gui_element(
            self.ui_context.create_popup(message, self.config)
        )

    # Scene Lifecycle Hooks
    # - on_load
    #   - before_update
    #   - update
    #   - render
    # - on_unload
    def on_load(self):
        """
        Lifecycle hook called when the scene is first loaded.

        This method is called automatically by the load() method when the scene is initialized.
        Override this method to perform scene-specific initialization like:
        - Setting up initial game state
        - Creating GUI elements
        - Loading resources needed by the scene
        - Initializing systems or components

        This is called once when the scene becomes active, not on every frame.

        """
        pass

    def before_update(self, dt_ms: int):
        """
        Lifecycle hook called at the beginning of each frame before the update.

        Override this method to perform pre-update operations such as:
        - Processing input that might affect the update
        - Preparing systems for the main update
        - Checking conditions before main game logic runs

        This method is called once per frame, before the update() method.

        Args:
            dt_ms (int): Elapsed time in milliseconds since the last frame.

        """
        pass

    def update(self, dt_ms: int):
        """
        Lifecycle hook for the main game logic update, called once per frame.

        Override this method to implement the core gameplay logic for this scene, such as:
        - Updating game entities and systems
        - Processing game rules
        - Handling time-based events
        - Determining scene transitions

        This is the main method where most of the scene's behavior should be implemented.
        It's called once per frame after before_update() and before render().

        Args:
            dt_ms (int): Elapsed time in milliseconds since the last frame.

        """
        pass

    def render(self, dt_ms: int):
        """
        Lifecycle hook for rendering the scene, called once per frame.

        This method handles the rendering of all GUI elements in the scene.
        It first clears the root GUI container, then updates and renders each GUI element.

        The default implementation:
        1. Clears the GUI root container
        2. Updates all GUI elements with the current scene context
        3. Renders all GUI elements to the root container

        Override this method if you need custom rendering behavior beyond GUI elements.

        Args:
            dt_ms (int): Elapsed time in milliseconds since the last frame.

        """
        if self.ui_context is None:
            raise RuntimeError("UI context is not configured for this scene.")
        self.ui_context.clear_root()
        self.logger.debug(f"Rendering {len(self.gui_elements)} GUI elements")
        for element in self.gui_elements:
            element.update(self, dt_ms)
        self.gui_elements = [
            element for element in self.gui_elements if not element.is_closed
        ]
        for element in self.gui_elements:
            self.ui_context.render_element(element)

    def on_unload(self):
        """
        Lifecycle hook called when transitioning away from this scene.

        Override this method to perform cleanup operations when the scene is no longer active:
        - Releasing resources
        - Saving state
        - Cleaning up event listeners
        - Performing any final actions before the scene is unloaded

        This is the final lifecycle method called before the scene is removed from the active stack.

        """
        self.logger.info(f"Unloading scene: {self.__class__.__name__}")
        pass

    @final
    def load(
        self,
        controller: "GameSceneController",
        cm: ComponentManager,
        gui: Any,
        sound: SoundController,
        ui_context: UiContext,
    ):
        """
        Initialize the scene with required dependencies and trigger the on_load
        lifecycle hook.

        This method is called by the GameSceneController when activating this scene.
        It provides the scene with references to core game systems and then calls the
        on_load() lifecycle hook to perform scene-specific initialization.

        This method is marked with @final and should not be overridden by subclasses.
        Instead, override the on_load() method for custom initialization.

        Parameters:
            controller (GameSceneController): Reference to the scene controller managing this scene
            cm (ComponentManager): The component manager for entity-component access
            gui (Any): The GUI system for rendering interface elements
            sound (SoundController): The sound system for audio playback
            ui_context (UiContext): Adapter for rendering and UI helpers

        """
        self.logger.info(f"Loading scene: {self.__class__.__name__}")
        self.controller = controller
        self.cm = cm
        self.gui = gui
        self.sound = sound
        self.ui_context = ui_context
        self.config = controller.config
        self.logger.debug(f"Calling on_load() for {self.__class__.__name__}")
        self.on_load()

    def pop(self):
        """
        Remove this scene from the scene stack and return to the previous scene.

        This is a convenience method that delegates to the controller's pop_scene
        method. Use this when the scene has completed its purpose and should be removed
        from the stack.

        """
        self.logger.info(f"Popping scene: {self.__class__.__name__}")
        self.controller.pop_scene()

    def save_game(self, objects, file_name, extras):
        """
        Save game state to a file.

        This is a convenience method that delegates to the serialization system.

        Parameters:
            objects: The game objects to be serialized and saved
            file_name (str): The name/path of the save file
            extras: Additional data to be included in the save file

        """
        self.logger.info(f"Saving game to file: {file_name}")
        try:
            serialization.save(objects, file_name, extras)
            self.logger.debug(f"Game saved successfully to {file_name}")
        except Exception as e:
            self.logger.error(
                f"Failed to save game to {file_name}: {str(e)}", exc_info=True
            )

    def load_game(self, file_name):
        """
        Load game state from a save file.

        This is a convenience method that delegates to the serialization system.

        Parameters:
            file_name (str): The name/path of the save file to load

        Returns:
            The deserialized game objects and state from the save file

        """
        self.logger.info(f"Loading game from file: {file_name}")
        try:
            data = serialization.load(file_name)
            self.logger.debug(f"Game loaded successfully from {file_name}")
            return data
        except Exception as e:
            self.logger.error(
                f"Failed to load game from {file_name}: {str(e)}",
                exc_info=True,
            )
            raise
