import tcod

from horderl.engine_adapter import GuiElement, core

from .. import palettes
from ..components.ability_tracker import AbilityTracker
from ..components.actors.calendar_actor import Calendar
from ..components.states.move_cost_affectors import (
    MoveCostAffector,
    MoveCostAffectorType,
)
from ..components.world_building.world_parameters import WorldParameters
from ..constants import PLAYER_ID
from ..i18n import t
from ..systems.abilities import ability_selection_system
from ..systems.actor_system import get_timecode


class Label(GuiElement):
    """
    Represent a text label.
    """

    def __init__(self, x, y, value, fg=None, bg=None, name=None):
        super().__init__(x, y, name=name)
        self.value = value
        self.fg = palettes.WHITE if fg is None else fg
        self.bg = palettes.BACKGROUND if bg is None else bg

    def render(self, panel):
        """
        Draw the bar onto the panel.
        """
        panel.print(self.x, self.y, self.value, fg=self.fg, bg=self.bg)


class GoldLabel(GuiElement):
    """
    Represent a text label.
    """

    def __init__(self, x, y):
        super().__init__(x, y, name="gold-label")
        self.value = "0c"

    def update(self, scene, dt_ms: int):
        self.value = f"{scene.gold}c"

    def render(self, panel):
        """
        Draw the bar onto the panel.
        """
        panel.print(
            self.x,
            self.y,
            t("label.gold", value=self.value),
            fg=palettes.GOLD,
            bg=palettes.BACKGROUND,
        )


class CalendarLabel(GuiElement):
    """
    Represent a text label.
    """

    def __init__(self, x, y):
        super().__init__(x, y, name="calendar-label")
        self.value = "#problem#"

    def update(self, scene, dt_ms: int):
        calendar = scene.cm.get_one(Calendar, entity=core.get_id("calendar"))
        timecode = get_timecode(calendar)
        self.value = f"{timecode}"

    def render(self, panel):
        """
        Draw the bar onto the panel.
        """
        panel.print(
            self.x,
            self.y,
            f"{self.value}",
            fg=palettes.GOLD,
            bg=palettes.BACKGROUND,
        )


class HordeStatusLabel(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, name="calendar-label")
        self.value = "#problem#"

    def update(self, scene, dt_ms: int):
        calendar = scene.cm.get_one(Calendar, entity=core.get_id("calendar"))
        if calendar:
            self.value = calendar.status

    def render(self, panel):
        """
        Draw the bar onto the panel.
        """
        panel.print(
            self.x,
            self.y,
            f"{self.value}",
            fg=palettes.HORDELING,
            bg=palettes.BACKGROUND,
        )


class SpeedLabel(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, name="hindered-label")
        self.value = "#problem#"

    def update(self, scene, dt_ms: int):
        hindered = _get_move_cost_affector(
            scene, PLAYER_ID, MoveCostAffectorType.HINDERED
        )
        haste = _get_move_cost_affector(
            scene, PLAYER_ID, MoveCostAffectorType.HASTE
        )
        if hindered:
            self.value = t("label.hindered")
        elif haste:
            self.value = t("label.haste")
        else:
            self.value = ""

    def render(self, panel):
        """
        Draw the bar onto the panel.
        """
        panel.print(
            self.x,
            self.y,
            f"{self.value}",
            fg=palettes.LIGHT_WATER,
            bg=palettes.BACKGROUND,
        )


class AbilityLabel(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, name="hindered-label")
        self.value = t("label.no_abilities")

    def render(self, panel: tcod.console.Console) -> None:
        panel.print(
            self.x,
            self.y,
            f"{self.value}",
            fg=palettes.WHITE,
            bg=palettes.BACKGROUND,
        )

    def update(self, scene, dt_ms: int):
        ability_tracker = scene.cm.get(AbilityTracker)
        if ability_tracker:
            ability_tracker = ability_tracker[0]
            ability = ability_selection_system.get_current_ability(
                scene, ability_tracker
            )
            self.value = f"{ability.ability_title} - {ability.use_cost}c"
        else:
            self.value = t("label.loading")


class VillageNameLabel(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, name="village-name-label")
        self.value = t("label.village")

    def render(self, panel: tcod.console.Console) -> None:
        panel.print(
            self.x,
            self.y,
            self.value,
            fg=palettes.WHITE,
            bg=palettes.BACKGROUND,
        )

    def update(self, scene, dt_ms: int):
        params = scene.cm.get(WorldParameters)
        if params:
            params = params[0]
            self.value = f"{params.world_name}"
        else:
            self.value = t("label.loading")


def _get_move_cost_affector(scene, entity, affector_type):
    return next(
        iter(
            scene.cm.get(
                MoveCostAffector,
                query=lambda affector: affector.entity == entity
                and affector.affector_type == affector_type,
            )
        ),
        None,
    )
