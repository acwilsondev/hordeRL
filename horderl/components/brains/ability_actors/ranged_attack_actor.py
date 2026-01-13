from dataclasses import dataclass

import tcod

from horderl.components.actions.attack_action import AttackAction
from horderl.components.actors.energy_actor import EnergyActor
from horderl.components.animation_effects.blinker import AnimationBlinker
from horderl.components.brains.brain import Brain
from horderl.components.enums import Intention
from horderl.components.tags.hordeling_tag import HordelingTag
from engine import constants, core
from engine.utilities import is_visible


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
                self.back_out(scene)

    def shoot(self, scene):
        attack = AttackAction(entity=self.entity, target=self.target, damage=1)
        scene.cm.add(attack)

        ability = scene.cm.get_component_by_id(self.shoot_ability)
        ability.count -= 1

        self.back_out(scene)

    def back_out(self, scene):
        old_actor = scene.cm.unstash_component(self.old_brain)
        blinker = scene.cm.get_one(AnimationBlinker, entity=self.target)
        blinker.stop(scene)
        scene.cm.delete_component(blinker)
        scene.cm.delete_component(self)
        return old_actor

    def _next_enemy(self, scene):
        next_enemy = self._get_next_enemy(scene)
        old_blinker = scene.cm.get_one(AnimationBlinker, entity=self.target)
        old_blinker.stop(scene)
        scene.cm.delete_component(old_blinker)
        scene.cm.add(AnimationBlinker(entity=next_enemy))
        self.target = next_enemy

    def _get_next_enemy(self, scene):
        current_target = scene.cm.get_one(HordelingTag, entity=self.target)
        all_enemies = scene.cm.get(HordelingTag)
        visible_enemies = [
            e for e in all_enemies if is_visible(scene, e.entity)
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
