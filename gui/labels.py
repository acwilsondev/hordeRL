from components.actors.calendar_actor import Calendar
from components.move_costs.swamped_state import Swamped
from engine import palettes, core, PLAYER_ID
from gui.gui_element import GuiElement


class Label(GuiElement):
    """Represent a text label."""
    def __init__(self, x, y, value, fg=palettes.WHITE, bg=palettes.BACKGROUND, name=None):
        super().__init__(x, y, name=name)
        self.value = value
        self.fg = fg
        self.bg = bg

    def render(self, panel):
        """Draw the bar onto the panel"""
        panel.print(self.x, self.y, self.value, fg=self.fg, bg=self.bg)


class GoldLabel(GuiElement):
    """Represent a text label."""
    def __init__(self, x, y):
        super().__init__(x, y, name='gold-label')
        self.value = 0

    def update(self, scene):
        self.value = scene.gold

    def render(self, panel):
        """Draw the bar onto the panel"""
        panel.print(self.x, self.y, f'Gold: {self.value}', fg=palettes.GOLD, bg=palettes.BACKGROUND)


class CalendarLabel(GuiElement):
    """Represent a text label."""
    def __init__(self, x, y):
        super().__init__(x, y, name='calendar-label')
        self.value = '#problem#'

    def update(self, scene):
        calendar = scene.cm.get_one(Calendar, entity=core.get_id('calendar'))
        if calendar:
            self.value = calendar.get_timecode()

    def render(self, panel):
        """Draw the bar onto the panel"""
        panel.print(self.x, self.y, f'{self.value}', fg=palettes.GOLD, bg=palettes.BACKGROUND)


class HordeStatusLabel(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, name='calendar-label')
        self.value = '#problem#'

    def update(self, scene):
        calendar = scene.cm.get_one(Calendar, entity=core.get_id('calendar'))
        if calendar:
            self.value = calendar.status

    def render(self, panel):
        """Draw the bar onto the panel"""
        panel.print(self.x, self.y, f'{self.value}', fg=palettes.HORDELING, bg=palettes.BACKGROUND)


class SwampedLabel(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, name='swamped-label')
        self.value = '#problem#'

    def update(self, scene):
        swamped = scene.cm.get_one(Swamped, entity=PLAYER_ID)
        if swamped:
            self.value = "*Swamped*"
        else:
            self.value = ""

    def render(self, panel):
        """Draw the bar onto the panel"""
        panel.print(self.x, self.y, f'{self.value}', fg=palettes.LIGHT_WATER, bg=palettes.WATER)
