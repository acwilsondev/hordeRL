import random
from dataclasses import dataclass

from engine.components import EnergyActor
from horderl.content.enemies.juggernaut import make_juggernaut
from horderl.content.enemies.juvenile import make_juvenile
from horderl.content.enemies.pirhana import make_pirhana
from horderl.content.enemies.sneaker import make_sneaker


@dataclass
class HordelingSpawner(EnergyActor):
    """
    Hordelings will spawn at this object's location.
    """

    energy_cost: int = EnergyActor.HOURLY
    waves: int = 1

    def act(self, scene):
        spawn_hordeling(scene)
        self.pass_turn(
            random.randint(EnergyActor.QUARTER_HOUR, EnergyActor.HOURLY * 20)
        )

        self.waves -= 1

        if self.waves <= 0:
            scene.cm.delete(self.entity)


def spawn_hordeling(scene):
    """
    Add a hordeling spawner to a random edge of the map.
    """
    x, y = get_wall_coords(scene.config)
    roll = random.random()
    if roll > 0.8:
        maker = random.choice([make_sneaker, make_juggernaut, make_pirhana])
        scene.cm.add(*maker(x, y)[1])
    else:
        scene.cm.add(*make_juvenile(x, y)[1])


def get_wall_coords():
    return random.choice(
        [
            (get_random_width_location(), 0),
            (0, get_random_height_location()),
            (settings.MAP_WIDTH - 1, get_random_height_location()),
            (get_random_width_location(), settings.MAP_HEIGHT - 1),
        ]
    )


def get_random_width_location(config):
    return random.randrange(1, config.map_width - 1)


def get_random_height_location(config):
    return random.randrange(1, config.map_height - 1)
