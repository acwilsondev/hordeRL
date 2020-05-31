import tcod.event

from components import Coordinates
from components.abilities.thwack_ability import ThwackAbility
from components.events.chargeabilityevent import ChargeAbilityEvent
from components.actions.thwack_action import ThwackAction
from components.brain import Brain
from components.enums import Intention, ControlMode
from components.events.turn_event import TurnEvent
from components.states.dizzy_state import DizzyState
from content.states import dizzy_animation
from engine import core, PLAYER_ID
from systems.utilities import set_intention


def run(scene) -> None:
    turn = scene.cm.get_one(TurnEvent, entity=PLAYER_ID)
    if turn:
        brain = scene.cm.get_one(Brain, entity=PLAYER_ID)
        do_take_turn(scene, brain)


def do_take_turn(scene, brain: Brain) -> None:
    if brain and brain.control_mode is ControlMode.PLAYER:
        dizzy = scene.cm.get_one(DizzyState, entity=brain.entity)
        if dizzy:
            core.get_key_event()
            if core.time_ms() > dizzy.next_turn:
                set_intention(scene, brain.entity, None, Intention.DALLY)
                scene.cm.add(ChargeAbilityEvent(entity=brain.entity))
                dizzy.next_turn = core.time_ms() + 500
                dizzy.duration -= 1

                coords = scene.cm.get_one(Coordinates, entity=brain.entity)
                scene.cm.add(*dizzy_animation(brain.entity, coords.x, coords.y)[1])

                if dizzy.duration <= 0:
                    scene.cm.delete_component(dizzy)
        else:
            handle_key_event(scene, brain.entity, KEY_ACTION_MAP)
    if brain and brain.control_mode is ControlMode.DEAD_PLAYER:
        handle_key_event(scene, brain.entity, DEAD_KEY_ACTION_MAP)


def handle_key_event(scene, entity_id, action_map):
    key_event = core.get_key_event()
    if key_event:
        key_event = key_event.sym
        intention = action_map.get(key_event, None)
        if intention is not None:
            set_intention(scene, entity_id, None, intention)
        else:
            # new event-based actions
            if key_event is tcod.event.K_SPACE:
                ability = scene.cm.get_one(ThwackAbility, entity=entity_id)
                if ability:
                    scene.cm.add(ThwackAction(entity=entity_id))
        scene.cm.add(ChargeAbilityEvent(entity=entity_id))


DEAD_KEY_ACTION_MAP = {
    tcod.event.K_l: Intention.ACTIVATE_CURSOR,
    tcod.event.K_BACKQUOTE: Intention.SHOW_DEBUG_SCREEN,
    tcod.event.K_ESCAPE: Intention.QUIT_GAME
}


KEY_ACTION_MAP = {
    tcod.event.K_KP_1: Intention.STEP_SOUTH_WEST,
    tcod.event.K_KP_2: Intention.STEP_SOUTH,
    tcod.event.K_KP_3: Intention.STEP_SOUTH_EAST,
    tcod.event.K_KP_4: Intention.STEP_WEST,
    tcod.event.K_KP_5: Intention.DALLY,
    tcod.event.K_KP_6: Intention.STEP_EAST,
    tcod.event.K_KP_7: Intention.STEP_NORTH_WEST,
    tcod.event.K_KP_8: Intention.STEP_NORTH,
    tcod.event.K_KP_9: Intention.STEP_NORTH_EAST,

    tcod.event.K_z: Intention.STEP_SOUTH_WEST,
    tcod.event.K_x: Intention.STEP_SOUTH,
    tcod.event.K_c: Intention.STEP_SOUTH_EAST,
    tcod.event.K_a: Intention.STEP_WEST,
    tcod.event.K_s: Intention.DALLY,
    tcod.event.K_d: Intention.STEP_EAST,
    tcod.event.K_q: Intention.STEP_NORTH_WEST,
    tcod.event.K_w: Intention.STEP_NORTH,
    tcod.event.K_e: Intention.STEP_NORTH_EAST,

    tcod.event.K_UP: Intention.STEP_NORTH,
    tcod.event.K_DOWN: Intention.STEP_SOUTH,
    tcod.event.K_RIGHT: Intention.STEP_EAST,
    tcod.event.K_LEFT: Intention.STEP_WEST,

    tcod.event.K_l: Intention.ACTIVATE_CURSOR,
    tcod.event.K_BACKQUOTE: Intention.SHOW_DEBUG_SCREEN,
    tcod.event.K_ESCAPE: Intention.QUIT_GAME
}
