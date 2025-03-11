from typing import final

from engine import serialization
from engine.component_manager import ComponentManager
from engine.sound.sound_controller import SoundController
from gui.gui import Gui
from gui.gui_element import GuiElement
from gui.popup_message import PopupMessage


class GameScene:
    """Base class for all game scenes in the hordeRL game engine.
    
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
        """Initialize a new GameScene instance.
        
        Sets up empty GUI element list and initializes core component references.
        The controller, GUI, and sound references will be populated when the scene
        is loaded through the load() method.
        """
        self.gui_elements = []
        self.cm: ComponentManager = ComponentManager()
        self.controller = None
        self.gui = None
        self.sound = None

    def add_gui_element(self, element: GuiElement):
        """Add a GUI element to the scene.
        
        This method handles both persistent and single-shot (temporary) GUI elements differently:
        - Single-shot elements (like popups or temporary menus) are rendered immediately
        - Persistent elements are added to the gui_elements list for later rendering in the render() method
        
        Parameters:
            element (GuiElement): The GUI element to add to the scene
        """
        if element.single_shot:
            # if it's a single shot (menu or popup message), we need to render it directly to the existing window
            element.render(self.gui.root)
        else:
            self.gui_elements.append(element)

    def popup_message(self, message: str):
        """Display a popup message to the user.
        
        Creates a PopupMessage GUI element with the given message text and adds it to the scene.
        This is a convenience method for showing quick notifications to the player.
        
        Parameters:
            message (str): The text message to display in the popup
        """
        self.add_gui_element(PopupMessage(message))

    # Scene Lifecycle Hooks
    # - on_load
    #   - before_update
    #   - update
    #   - render
    # - on_unload
    def on_load(self):
        """Lifecycle hook called when the scene is first loaded.
        
        This method is called automatically by the load() method when the scene is initialized.
        Override this method to perform scene-specific initialization like:
        - Setting up initial game state
        - Creating GUI elements
        - Loading resources needed by the scene
        - Initializing systems or components
        
        This is called once when the scene becomes active, not on every frame.
        """
        pass

    def before_update(self):
        """Lifecycle hook called at the beginning of each frame before the update.
        
        Override this method to perform pre-update operations such as:
        - Processing input that might affect the update
        - Preparing systems for the main update
        - Checking conditions before main game logic runs
        
        This method is called once per frame, before the update() method.
        """
        pass

    def update(self):
        """Lifecycle hook for the main game logic update, called once per frame.
        
        Override this method to implement the core gameplay logic for this scene, such as:
        - Updating game entities and systems
        - Processing game rules
        - Handling time-based events
        - Determining scene transitions
        
        This is the main method where most of the scene's behavior should be implemented.
        It's called once per frame after before_update() and before render().
        """
        pass

    def render(self):
        """Lifecycle hook for rendering the scene, called once per frame.
        
        This method handles the rendering of all GUI elements in the scene.
        It first clears the root GUI container, then updates and renders each GUI element.
        
        The default implementation:
        1. Clears the GUI root container
        2. Updates all GUI elements with the current scene context
        3. Renders all GUI elements to the root container
        
        Override this method if you need custom rendering behavior beyond GUI elements.
        """
        self.gui.root.clear()
        for element in self.gui_elements:
            element.update(self)
        for element in self.gui_elements:
            element.render(self.gui.root)

    def on_unload(self):
        """Lifecycle hook called when transitioning away from this scene.
        
        Override this method to perform cleanup operations when the scene is no longer active:
        - Releasing resources
        - Saving state
        - Cleaning up event listeners
        - Performing any final actions before the scene is unloaded
        
        This is the final lifecycle method called before the scene is removed from the active stack.
        """
        pass

    @final
    def load(
        self,
        controller: "GameSceneController",
        cm: ComponentManager,
        gui: Gui,
        sound: SoundController,
    ):
        """Initialize the scene with required dependencies and trigger the on_load lifecycle hook.
        
        This method is called by the GameSceneController when activating this scene.
        It provides the scene with references to core game systems and then calls the
        on_load() lifecycle hook to perform scene-specific initialization.
        
        This method is marked with @final and should not be overridden by subclasses.
        Instead, override the on_load() method for custom initialization.
        
        Parameters:
            controller (GameSceneController): Reference to the scene controller managing this scene
            cm (ComponentManager): The component manager for entity-component access
            gui (Gui): The GUI system for rendering interface elements
            sound (SoundController): The sound system for audio playback
        """
        self.controller = controller
        self.cm = cm
        self.gui = gui
        self.sound = sound
        self.on_load()

    def pop(self):
        """Remove this scene from the scene stack and return to the previous scene.
        
        This is a convenience method that delegates to the controller's pop_scene method.
        Use this when the scene has completed its purpose and should be removed from the stack.
        """
        self.controller.pop_scene()

    def save_game(self, objects, file_name, extras):
        """Save game state to a file.
        
        This is a convenience method that delegates to the serialization system.
        
        Parameters:
            objects: The game objects to be serialized and saved
            file_name (str): The name/path of the save file
            extras: Additional data to be included in the save file
        """
        serialization.save(objects, file_name, extras)

    def load_game(self, file_name):
        """Load game state from a save file.
        
        This is a convenience method that delegates to the serialization system.
        
        Parameters:
            file_name (str): The name/path of the save file to load
            
        Returns:
            The deserialized game objects and state from the save file
        """
        return serialization.load(file_name)
