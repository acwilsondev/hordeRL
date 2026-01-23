# ECS Component Contract

## Purpose

This document defines the **stable, data-only component contract** for the
HordeRL ECS. It clarifies identity, serialization rules, and ownership
boundaries so components remain simple records while systems hold behavior.

## Contract (data-only components)

Components are **plain `@dataclass` records** with no behavior. They should:

- Be defined as `@dataclass` types.
- Carry **identity fields** (`id`, `entity`) as data, not computed properties.
- Remain **flat and serializable** via `dataclasses.asdict` (no custom JSON
  encoding required).
- Avoid side effects, IO, and cross-component logic. Behavior belongs in
  systems.

### Identity and serialization metadata

Serialization uses the existing dataclass-to-dict path. The serializer:

- Calls `dataclasses.asdict(component)`.
- Adds a `"class"` field to the serialized dict to restore the class on load.

**Implications for component definitions**:

- Field values must be JSON-serializable (or otherwise supported by
  `dataclasses.asdict`).
- Avoid computed fields or properties that must be reconstructed at runtime.
- Prefer plain scalar or dataclass fields over references to services, managers,
  or systems.

## ID stability rules

Component and entity IDs are stable across save/load and must not be mutated in
place.

- **Creation**
  - New components receive a unique `id` at creation time (via
    `engine.core.get_id`).
  - `entity` is set by the scene when the component is attached to an entity.

- **Reassignment**
  - Do **not** mutate `id` or `entity` directly on a live component. Changing
    ownership requires removing and re-adding the component so indexes remain
    consistent.

- **Load semantics**
  - Save files persist component `id` and `entity` values.
  - Load restores components by instantiating the dataclass with the persisted
    fields. The default `id` factory should only run for **new** components.
  - Named IDs are restored via `engine.core.set_named_ids` before components are
    instantiated.

## Data-only component design guidance

When adding new components:

- **Prefer dataclasses** with only data fields.
- Keep components **small and focused**; prefer composition over inheritance.
- Add behavior in systems or scene orchestration, not in component methods.
- Event components are **optional**; if used, keep them data-only and
  short-lived.

## Ownership boundaries

The ECS layers are intentionally separated:

- **ECS runtime** (component manager) manages storage, queries, and lifecycle.
- **Serialization** converts dataclass components to/from save data.
- **Scene orchestration** creates entities, assigns components, and invokes
  save/load workflows.

Direct dependencies between ECS and serialization are avoided; the scene
coordinates both as the boundary layer.
