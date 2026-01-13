from typing import Tuple

import numpy as np

from engine import GameScene, core
from engine.component_manager import ComponentManager
from engine.components.class_register import LoadClasses
from engine.core import timed
from engine.message import Message
from engine.ui.layout import VerticalAnchor
from horderl import palettes
from horderl.components.events.start_game_events import StartGame
from horderl.components.population import Population
from horderl.components.serialization.load_game import LoadGame
from horderl.components.sound.battle_music import BattleMusic
from horderl.components.sound.start_music import StartMusic
from horderl.components.world_beauty import WorldBeauty
from horderl.components.world_building.set_worldbuilder_params import (
    SelectBiome,
)
from horderl.constants import PLAYER_ID
from horderl.content.physics_controller import make_physics_controller
from horderl.content.tax_handler import make_tax_handler
from horderl.content.utilities import make_calendar
from horderl.gui.bars import HealthBar, HordelingBar, PeasantBar, Thwackometer
from horderl.gui.help_tab import HelpTab
from horderl.gui.labels import (
    AbilityLabel,
    CalendarLabel,
    GoldLabel,
    HordeStatusLabel,
    Label,
    SpeedLabel,
    VillageNameLabel,
)
from horderl.gui.message_box import MessageBox
from horderl.gui.play_window import PlayWindow
from horderl.gui.popup_message import PopupMessage
from horderl.systems import act, control_turns, move


class DefendScene(GameScene):
    """
    Core gameplay scene responsible for managing the main game loop during village
    defense.

    This scene manages all aspects of village defense gameplay including:
    - Combat and movement systems
    - Player input handling and turn control
    - GUI elements for gameplay feedback (health, resources, messages)
    - World state tracking (visibility, memory maps)
    - Message handling for player feedback

    The DefendScene integrates multiple game systems and serves as the central
    coordinator for the main gameplay experience, connecting player actions
    with game mechanics and visual representation.

    """

    def __init__(self, from_file=""):
        """
        Initialize a new DefendScene with all required GUI elements and state tracking.

        Sets up the scene with the play window, status bars, labels, and message box.
        Initializes tracking for game visibility and memory maps as well as the message log.

        Args:
            from_file (str, optional): Path to a save file to load. If empty, starts a new game.
                                      Defaults to "".

        """
        super().__init__()
        self.player = PLAYER_ID

        self.memory_map = None
        self.visibility_map = None
        self.messages = []
        self.play_window = None

        self.gold = 0

        self.from_file = from_file

    def on_load(self):
        """
        Initialize the component manager and load all necessary game systems when the
        scene becomes active.

        This method is called when the scene is pushed to the scene stack and becomes active.
        It sets up:
        - Component Manager (CM) for entity-component management
        - Game loading from file (if from_file is specified)
        - World generation and biome selection (for new games)
        - Core game systems (taxes, calendar, physics)
        - Music controllers
        - World beauty and population systems

        The method handles both new game creation and loading saved games.

        """
        self.cm = ComponentManager()
        self.memory_map = np.zeros(
            (self.config.map_width, self.config.map_height),
            order="F",
            dtype=bool,
        )
        self.visibility_map = np.zeros(
            (self.config.map_width, self.config.map_height),
            order="F",
            dtype=bool,
        )
        self.play_window = PlayWindow(
            25,
            0,
            self.config.map_width,
            self.config.map_height,
            self.cm,
            self.visibility_map,
            self.memory_map,
            self.config,
        )

        anchor = VerticalAnchor(1, 1)
        anchor.add_element(
            Label(
                1,
                1,
                f"@ {self.config.character_name}_______________",
            )
        )
        anchor.add_element(HealthBar(1, 0))
        anchor.add_element(Thwackometer(1, 0))
        anchor.add_element(SpeedLabel(1, 0))
        anchor.add_element(CalendarLabel(1, 0))
        anchor.add_element(GoldLabel(1, 0))
        anchor.add_element(AbilityLabel(1, 0))
        anchor.add_space(1)

        anchor.add_element(VillageNameLabel(1, 6))
        anchor.add_element(Label(1, 7, "Peasants"))
        anchor.add_element(PeasantBar(1, 8))
        anchor.add_element(HordeStatusLabel(1, 9))
        anchor.add_element(HordelingBar(1, 10))
        anchor.add_element(MessageBox(1, 11, 23, 16, self.messages))
        anchor.add_space(16)

        anchor.add_element(HelpTab(1, 27))

        self.add_gui_element(anchor)
        self.add_gui_element(self.play_window)
        self.cm.add(LoadClasses(entity=self.player))

        if self.from_file:
            self.cm.add(LoadGame(entity=self.player, file_name=self.from_file))
            self.cm.add(StartGame(entity=self.player))
        else:
            self.cm.add(SelectBiome(entity=core.get_id("world")))
            self.cm.add(*make_tax_handler()[1])
            self.cm.add(*make_calendar()[1])
            self.cm.add(*make_physics_controller()[1])
            self.cm.add(StartMusic(entity=self.player))
            self.cm.add(BattleMusic(entity=self.player))
            self.cm.add(WorldBeauty(entity=core.get_id("world")))
            self.cm.add(Population(entity=core.get_id("world")))

    def popup_message(self, message: str):
        """
        Display a prominent popup message to the player while also adding it to the
        message log.

        This method serves as a high-visibility notification system for important game events
        that require the player's immediate attention.

        Args:
            message (str): The text content to display in the popup and add to the message log.

        """
        self.message(message)
        self.add_gui_element(PopupMessage(message, self.config))

    @timed(100, __name__)
    def update(self, dt: float):
        """
        Main update method called each frame to progress the game state.

        This method is decorated with @timed, which logs performance metrics if
        the method execution exceeds 100ms, helping identify performance bottlenecks.

        The update follows a specific sequence:
        1. act.run - Process entity actions and abilities
        2. move.run - Handle movement and physics
        3. control_turns.run - Manage turn order and player input

        This structured approach ensures game systems are processed in the correct order,
        maintaining game logic consistency.

        """
        act.run(self)
        move.run(self)
        control_turns.run(self)

    def message(self, text: str, color: Tuple[int, int, int] = palettes.MEAT):
        """
        Add a message to the message log with specified text and color.

        The message log has a maximum capacity of 20 messages. When exceeded,
        the oldest message is removed (FIFO behavior). Messages are displayed
        in the MessageBox GUI element and provide important feedback to the player.

        Args:
            text (str): The text content of the message.
            color (Tuple[int, int, int], optional): RGB color tuple for the message.
                                                    Defaults to palettes.MEAT.

        """
        if len(self.messages) > 20:
            self.messages.pop(0)
        self.messages.append(Message(f" {text}", color=color))

    def warn(self, text: str):
        """
        Add a warning message to the message log in a distinctive warning color.

        This is a convenience method for sending warning notifications to the player
        about dangerous situations or potential negative outcomes.

        Args:
            text (str): The warning text to display.

        """
        self.message(text, color=palettes.HORDELING)
