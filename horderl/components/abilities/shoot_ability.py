from dataclasses import dataclass

from engine.components import Coordinates
from engine.utilities import is_visible

from ...content.states import confused_animation
from ..animation_controllers.blinker_animation_controller import (
    BlinkerAnimationController,
)
from ..brains.ability_actors.ranged_attack_actor import RangedAttackActor
from ..season_reset_listeners.seasonal_actor import SeasonResetListener
from ..tags.hordeling_tag import HordelingTag
from .ability import Ability


@dataclass
class ShootAbility(SeasonResetListener, Ability):
    ability_title: str = "Shoot Bow"
    ability_title_key: str = "ability.shoot_bow"
    count: int = 5
    max: int = 5
    unlock_cost: int = 100
    use_cost: int = 5

    def on_season_reset(self, scene, season):
        self.count = self.max

    def use(self, scene, dispatcher):
        hordelings = [
            e
            for e in scene.cm.get(HordelingTag)
            if is_visible(
                scene, scene.cm.get_one(Coordinates, entity=e.entity)
            )
        ]
        if not hordelings:
            self._handle_confused(scene)
            return
        self._handle_shoot(scene, hordelings, dispatcher)

    def _handle_shoot(self, scene, hordelings, dispatcher):
        target = hordelings[0]
        new_controller = RangedAttackActor(
            entity=self.entity,
            old_actor=dispatcher,
            target=target.entity,
            shoot_ability=self.id,
        )
        blinker = BlinkerAnimationController(entity=target.entity)
        scene.cm.stash_component(dispatcher)
        scene.cm.add(new_controller, blinker)
        # TODO why are we removing gold in the ability? You may have declined to shoot.
        scene.gold -= 5

    def _handle_confused(self, scene):
        player_coords = scene.cm.get_one(Coordinates, entity=self.entity)
        confused_anim = confused_animation(player_coords.x, player_coords.y)
        scene.cm.add(*confused_anim[1])
