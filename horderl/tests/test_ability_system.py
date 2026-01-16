from engine import serialization
from engine.component_manager import ComponentManager
from engine.components import Coordinates
from engine.components.entity import Entity
from horderl.components.abilities.build_wall_ability import BuildWallAbility
from horderl.components.abilities.debug_ability import DebugAbility
from horderl.components.abilities.thwack_ability import ThwackAbility
from horderl.components.wants_to_show_debug import WantsToShowDebug
from horderl.i18n import t
from horderl.systems.ability_system import apply_ability, run as run_ability


class DummyScene:
    """Provide minimal scene hooks needed by ability system tests."""

    def __init__(self) -> None:
        self.cm = ComponentManager()
        self.gold = 0
        self.warnings: list[str] = []

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def test_apply_ability_blocks_without_gold() -> None:
    scene = DummyScene()
    player_id = 1
    scene.cm.add(
        Entity(entity=player_id, name="player"),
        Coordinates(entity=player_id, x=2, y=3),
    )
    ability = BuildWallAbility(entity=player_id)
    scene.cm.add(ability)

    apply_ability(scene, dispatcher_id=99, ability=ability)

    assert scene.warnings == [t("warning.no_money")]
    animations = scene.cm.get(
        Entity, query=lambda ent: ent.name == "no_money_animation"
    )
    assert animations


def test_apply_ability_dispatches_debug() -> None:
    scene = DummyScene()
    scene.gold = 1
    ability = DebugAbility(entity=10)
    scene.cm.add(ability)

    apply_ability(scene, dispatcher_id=123, ability=ability)

    assert scene.cm.get_one(WantsToShowDebug, entity=ability.entity)


def test_run_recharges_thwack_ability() -> None:
    scene = DummyScene()
    ability = ThwackAbility(
        entity=3,
        count=1,
        max=3,
        energy=0,
        is_recharging=True,
    )
    scene.cm.add(ability)

    run_ability(scene)

    assert ability.count == 2
    assert ability.is_recharging is True
    assert ability.energy < 0


def test_control_mode_ability_serializes(tmp_path) -> None:
    scene = DummyScene()
    ability = BuildWallAbility(entity=42)
    scene.cm.add(ability)
    save_path = tmp_path / "save.json"

    serialization.save(scene.cm.get_serial_form(), save_path)

    loaded = serialization.load(save_path)
    loaded_ability = next(
        comp
        for comp in loaded["active_components"].values()
        if isinstance(comp, BuildWallAbility)
    )

    assert loaded_ability.control_mode_key == "place_stone_wall"
