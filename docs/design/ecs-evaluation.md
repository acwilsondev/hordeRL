# ECS Redesign + Esper Evaluation

## Why revisit the ECS now

The current entity-component system mixes three competing patterns:

- A component class hierarchy with abstract base classes and specialized subclasses.
- A queryable component manager that already treats components as data records.
- A small set of systems that mutate component state and dispatch events.

This blend has blurred boundaries and made it hard to reason about how data flows
through gameplay. To support fast iteration, we should pivot to a flatter
component model and make systems the primary place for behavior.

## Objectives

- **Flatten the component hierarchy.** Components should be data-only records with
  no behavioral inheritance beyond a single, minimal base type.
- **Centralize behavior in systems.** Systems should orchestrate gameplay by
  reading/writing component data and emitting events.
- **Make component composition explicit.** Entities are just IDs + sets of
  components. Avoid implying “is-a” relationships through inheritance.
- **Keep engine core reusable.** ECS primitives should be stable and reusable for
  other projects, with feature-level gameplay logic living outside the core.

## Current pain points to solve

- **Component inheritance disguises behavior.** Abstract components (e.g. event
  listeners or actors) encourage behavior to be embedded in components rather than
  systems, which complicates testing and reusability.
- **Ambiguous responsibilities.** Component manager handles lifecycle, querying,
  and serialization while components also hold logic and event handlers.
- **Tight coupling to game rules.** Many components encode game-specific
  assumptions that should live in feature-level systems.

## Proposed flat component hierarchy

- **One minimal base class** (`Component`) for serialization, identity, and
  optional lifecycle hooks.
- **Concrete components are simple data carriers** with no inheritance chains.
  Prefer composition of multiple components over specialized subclasses.
- **Behavior lives in systems, period.** Components are not allowed to carry
  gameplay logic or callbacks.
- **System registry defines behavior.** Systems are the primary place for
  iteration, validation, and updates.

## Evaluating `esper` for the ECS layer

`esper` is a lightweight Python ECS library with an emphasis on straightforward
composition and system iteration. It is a plausible fit for a flatter ECS,
provided we can integrate serialization and scene orchestration cleanly.

### Potential benefits

- **Data-first components.** Encourages simple component classes with no
  inheritance and minimal behavior.
- **Clear system execution model.** Systems operate over component tuples,
  reinforcing behavior-in-systems.
- **Built-in world registry.** `esper.World` can replace or simplify the existing
  component manager for lifecycle and query management.
- **Community adoption.** It is a known ECS library with a straightforward API,
  which lowers onboarding cost for contributors.

### Potential risks and gaps

- **Serialization integration boundaries.** ECS and serialization should not
  depend on one another directly. The scene should own both and orchestrate
  object creation, component assignment, and save/load flow.
- **ID stability.** Components already serialize via dataclass <-> dict, so the
  main risk is stable IDs across sessions and reassignment rules when loading.
- **Event handling model.** We should question whether gameplay needs event
  components at all, or whether system logic can express those flows without
  event objects.
- **Performance considerations.** The game is not currently performance-bound, but
  any heavy use of Python reflection in `esper` should be profiled once the
  migration is underway.

## Integration approach (two projects)

**Project A: ECS cleanup (no `esper`)**

1. **Define the flat component contract.** Keep dataclass-based serialization,
   document ID stability rules, and remove behavioral inheritance.
2. **Move behavior into systems.** Event listeners, actors, and callbacks become
   systems. Systems can create entities and assign components via the scene.
3. **Clarify ser/de ownership.** The scene coordinates both ECS and serialization,
   typically via a dedicated ser/de system that creates objects and assigns
   components during load.

**Project B: `esper` integration (optional)**

1. **Introduce an adapter layer** that wraps `esper.World` and provides the query
   ergonomics and lifecycle hooks needed by existing systems.
2. **Port a vertical slice** to validate save/load, entity creation, and system
   ergonomics before committing to a full migration.
3. **Remove the old component manager** once `esper` proves parity.

## Next steps

- Start Project A by inventorying components and classifying:
  - Data-only (safe to migrate quickly).
  - Behavior-heavy (requires system extraction).
- Capture ID stability rules and document ser/de responsibilities in the scene.
- Decide whether to pursue Project B after Project A stabilizes.
