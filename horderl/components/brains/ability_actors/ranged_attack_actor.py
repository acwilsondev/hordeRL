from dataclasses import dataclass

import tcod

from engine import constants, core
from engine.components import Coordinates, EnergyActor
from engine.utilities import is_visible
from horderl.components.actions.attack_action import AttackAction
from horderl.components.animation_definitions.blinker_animation_definition import (
    BlinkerAnimationDefinition,
)
from horderl.components.brains.brain import Brain
from horderl.components.enums import Intention
from horderl.components.tags.hordeling_tag import HordelingTag
from horderl.systems import brain_stack


@dataclass
class RangedAttackActor(Brain):
    energy_cost: int = EnergyActor.INSTANT
    target: int = 0
    shoot_ability: int = constants.INVALID

    def act(self, scene):
        self._handle_input(scene)

    def _handle_input(self, scene):
        key_event = core.get_key_event()
        if key_event:
            key_event = key_event.sym
            intention = KEY_ACTION_MAP.get(key_event, None)
            if intention is Intention.USE_ABILITY:
                self.shoot(scene)
            elif intention in {
                Intention.STEP_NORTH,
                Intention.STEP_EAST,
                Intention.STEP_WEST,
                Intention.STEP_SOUTH,
            }:
                self._next_enemy(scene)
            elif intention is Intention.BACK:
                self._exit(scene)

    def shoot(self, scene):
        attack = AttackAction(entity=self.entity, target=self.target, damage=1)
        scene.cm.add(attack)

        ability = scene.cm.get_component_by_id(self.shoot_ability)
        ability.count -= 1

        self._exit(scene)

    def _exit(self, scene) -> None:
        # Ensure target highlighting is cleared before restoring the old brain.
        blinker = scene.cm.get_one(
            BlinkerAnimationDefinition, entity=self.target
        )
        if blinker:
            blinker.is_animating = False
            blinker.remove_on_stop = True
        brain_stack.back_out(scene, self)

    def _next_enemy(self, scene):
        next_enemy = self._get_next_enemy(scene)
        old_blinker = scene.cm.get_one(
            BlinkerAnimationDefinition, entity=self.target
        )
        if old_blinker:
            old_blinker.is_animating = False
            old_blinker.remove_on_stop = True
        scene.cm.add(BlinkerAnimationDefinition(entity=next_enemy))
        self.target = next_enemy

    def _get_next_enemy(self, scene):
        current_target = scene.cm.get_one(HordelingTag, entity=self.target)
        all_enemies = scene.cm.get(HordelingTag)
        visible_enemies = [
            e
            for e in all_enemies
            if is_visible(
                scene, scene.cm.get_one(Coordinates, entity=e.entity)
            )
        ]
        enemies = sorted(visible_enemies, key=lambda x: x.id)

        index = enemies.index(current_target)
        next_index = (index + 1) % len(enemies)
        return enemies[next_index].entity


KEY_ACTION_MAP = {
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}
