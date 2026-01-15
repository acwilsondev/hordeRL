# ECS Phase 0 Audit

## Purpose

Document the current ECS surface area, categorize components by behavior, and
highlight critical flows that must remain stable during migration.

## Non-negotiables (Phase 0 constraints)

- **Save/load compatibility:** none required (alpha-stage game).
- **Performance constraints:** baseline now; revisit after CM indexing removal.
- **Migration window:** each phase should complete with a stable, playable game.

## Component inventory

Classification notes:
- **Data-only** = no methods defined in the component class.
- **Hybrid** = helper methods but no direct actor/update/event lifecycle.
- **Behavior-heavy** = has `act`, `update`, or explicit event/listener hooks.

This inventory is derived from a static scan of component class definitions and
should be refined as migration proceeds.

### Data-only components

- `ThwackAction` (horderl/components/actions/thwack_action.py)
- `Attributes` (horderl/components/attributes.py)
- `CryForHelp` (horderl/components/cry_for_help.py)
- `Diggable` (horderl/components/diggable.py)
- `Edible` (horderl/components/edible.py)
- `ChargeAbilityEvent` (horderl/components/events/chargeabilityevent.py)
- `StartSpawningEvent` (horderl/components/events/start_spawning_event.py)
- `TurnEvent` (horderl/components/events/turn_event.py)
- `Faction` (horderl/components/faction.py)
- `Floodable` (horderl/components/floodable.py)
- `Flooder` (horderl/components/flooder.py)
- `Material` (horderl/components/material.py)
- `Move` (horderl/components/movement/move.py)
- `Options` (horderl/components/options.py)
- `PathNode` (horderl/components/path_node.py)
- `PathfinderCost` (horderl/components/pathfinder_cost.py)
- `Breadcrumb` (horderl/components/pathfinding/breadcrumb.py)
- `GoldPickup` (horderl/components/pickup_gold.py)
- `FarmedBy` (horderl/components/relationships/farmed_by.py)
- `Owner` (horderl/components/relationships/owner.py)
- `Residence` (horderl/components/relationships/residence.py)
- `Sellable` (horderl/components/sellable.py)
- `Senses` (horderl/components/senses.py)
- `DifficultTerrain` (horderl/components/states/move_cost_affectors.py)
- `EasyTerrain` (horderl/components/states/move_cost_affectors.py)
- `Haste` (horderl/components/states/move_cost_affectors.py)
- `Hindered` (horderl/components/states/move_cost_affectors.py)
- `Structure` (horderl/components/structure.py)
- `CropInfo` (horderl/components/tags/crop_info.py)
- `RoadMarker` (horderl/components/tags/road_marker.py)
- `Tag` (horderl/components/tags/tag.py)
- `TownCenterFlag` (horderl/components/tags/town_center_flag.py)
- `TargetValue` (horderl/components/target_value.py)
- `TaxValue` (horderl/components/tax_value.py)

### Hybrid components

- `Coordinates` (engine/components/coordinates.py)
- `Entity` (engine/components/entity.py)
- `Appearance` (horderl/components/appearance.py)
- `Attack` (horderl/components/attacks/attack.py)
- `HouseStructure` (horderl/components/house_structure.py)
- `CostMapper` (horderl/components/pathfinding/cost_mapper.py)
- `Pathfinder` (horderl/components/pathfinding/pathfinder.py)
- `TargetEvaluator` (horderl/components/pathfinding/target_evaluation/target_evaluator.py)
- `WorldParameters` (horderl/components/world_building/world_parameters.py)

### Behavior-heavy components

- `Actor` (engine/components/actor.py)
- `AnimationController` (engine/components/animation_controller.py)
- `LoadClassListener` (engine/components/class_register.py)
- `LoadClasses` (engine/components/class_register.py)
- `EnergyActor` (engine/components/energy_actor.py)
- `Event` (engine/components/events.py)
- `Updateable` (engine/components/updateable.py)
- `Ability` (horderl/components/abilities/ability.py)
- `ThwackAbility` (horderl/components/abilities/thwack_ability.py)
- `AttackAction` (horderl/components/actions/attack_action.py)
- `EatAction` (horderl/components/actions/eat_action.py)
- `TunnelToPoint` (horderl/components/actions/tunnel_to_point.py)
- `BombActor` (horderl/components/actors/bomb_actor.py)
- `Calendar` (horderl/components/actors/calendar_actor.py)
- `HordelingSpawner` (horderl/components/actors/hordeling_spawner.py)
- `BlinkerAnimationController` (horderl/components/animation_controllers/blinker_animation_controller.py)
- `FloatAnimationController` (horderl/components/animation_controllers/float_animation_controller.py)
- `PathAnimationController` (horderl/components/animation_controllers/path_animation_controller.py)
- `RandomizedBlinkerAnimationController` (horderl/components/animation_controllers/randomized_blinker_animation_controller.py)
- `SequenceAnimationController` (horderl/components/animation_controllers/sequence_animation_controller.py)
- `AttackEffect` (horderl/components/attacks/attack_effects/attack_effect.py)
- `Brain` (horderl/components/brains/brain.py)
- `AttackFinished` (horderl/components/events/attack_events.py)
- `OnAttackFinishedListener` (horderl/components/events/attack_events.py)
- `AttackStartListener` (horderl/components/events/attack_started_events.py)
- `AttackStarted` (horderl/components/events/attack_started_events.py)
- `BuildWorld` (horderl/components/events/build_world_events.py)
- `BuildWorldListener` (horderl/components/events/build_world_events.py)
- `DallyEvent` (horderl/components/events/dally_event.py)
- `DallyListener` (horderl/components/events/dally_event.py)
- `Delete` (horderl/components/events/delete_event.py)
- `DeleteListener` (horderl/components/events/delete_event.py)
- `DeathListener` (horderl/components/events/die_events.py)
- `Die` (horderl/components/events/die_events.py)
- `FastForward` (horderl/components/events/fast_forward.py)
- `HoleDug` (horderl/components/events/hole_dug_events.py)
- `HoleDugListener` (horderl/components/events/hole_dug_events.py)
- `DayBegan` (horderl/components/events/new_day_event.py)
- `DayBeganListener` (horderl/components/events/new_day_event.py)
- `PeasantAdded` (horderl/components/events/peasant_events.py)
- `PeasantAddedListener` (horderl/components/events/peasant_events.py)
- `PeasantDied` (horderl/components/events/peasant_events.py)
- `PeasantDiedListener` (horderl/components/events/peasant_events.py)
- `QuitGame` (horderl/components/events/quit_game_events.py)
- `QuitGameListener` (horderl/components/events/quit_game_events.py)
- `ShowHelpDialogue` (horderl/components/events/show_help_dialogue.py)
- `GameStartListener` (horderl/components/events/start_game_events.py)
- `StartGame` (horderl/components/events/start_game_events.py)
- `EnterEvent` (horderl/components/events/step_event.py)
- `EnterListener` (horderl/components/events/step_event.py)
- `StepEvent` (horderl/components/events/step_event.py)
- `StepListener` (horderl/components/events/step_event.py)
- `TerrainChangedEvent` (horderl/components/events/terrain_changed_event.py)
- `TerrainChangedListener` (horderl/components/events/terrain_changed_event.py)
- `TreeCutEvent` (horderl/components/events/tree_cut_event.py)
- `TreeCutListener` (horderl/components/events/tree_cut_event.py)
- `FloodHolesSystem` (horderl/components/flood_nearby_holes.py)
- `BreadcrumbTracker` (horderl/components/pathfinding/breadcrumb_tracker.py)
- `ResetSeason` (horderl/components/season_reset_listeners/reset_season.py)
- `SeasonResetListener` (horderl/components/season_reset_listeners/seasonal_actor.py)
- `LoadGame` (horderl/components/serialization/load_game.py)
- `SaveGame` (horderl/components/serialization/save_game.py)
- `ShowDebug` (horderl/components/show_debug.py)
- `FreezeWater` (horderl/components/weather/freeze_water.py)
- `SnowFall` (horderl/components/weather/snow_fall.py)
- `SelectBiome` (horderl/components/world_building/set_worldbuilder_params.py)
- `WrathEffect` (horderl/components/wrath_effect.py)

## Critical flows

### Serialization + loadable component registry

- **Component registry:** `Component` subclasses self-register in
  `Component.subclasses`, and `engine.serialization._gather_loadable_classes`
  consumes that registry during load.
- **Save path:** `GameScene.save_game` → `engine.serialization.save`, typically
  triggered by the `SaveGame` EnergyActor component.
- **Load path:** `GameScene.load_game` → `engine.serialization.load` →
  `ComponentManager.from_data`, typically triggered by the `LoadGame` EnergyActor.
- **Component manager serialization:** `ComponentManager.get_serial_form` returns
  `active_components`, `stashed_components`, and `stashed_entities`, which the
  serialization layer persists.

### Entity construction entry points

- **Content factories:** `horderl/content/*` modules construct tuples of
  `(entity_id, [components...])` for enemies, allies, terrain, and world builders.
- **World builder flow:** `horderl/content/world_builder.make_world_build` emits
  the world-builder entity and a sequence of `BuildWorld`/step events.
- **Scene initialization:** `DefendScene.on_load` seeds core systems (world
  selection, calendar, physics, music, etc.) by adding components into the CM.

### Event dispatch + lifecycle hooks

- **Update loop:** `DefendScene.update` runs all `Updateable` components before
  legacy systems (`act`, `move`, `control_turns`).
- **Actor dispatch:** `horderl/systems/act.run` iterates `Actor` components and
  calls `act` when `can_act` passes.
- **Event flow:** `Event.act` locates listeners via `scene.cm.get(self.listener_type())`,
  calls `notify`, then deletes itself from the CM. `Move` system emits `StepEvent`
  components, which follow the same event dispatch path.

## High-risk flows + owners

- **Serialization registry & load pipeline** (Owner: Engine Core)
  - Risks: missing class registration, dataclass changes, stashed entity handling.
- **Entity construction factories** (Owner: Gameplay/Content)
  - Risks: component contract changes breaking prefab construction, world-builder
    sequencing.
- **Event dispatch and update ordering** (Owner: Gameplay Systems)
  - Risks: behavior relocation breaking event triggers, update ordering changes.
