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
- **Event components are data-only.** Event processing moves to systems and
  dispatchers instead of component subclasses.
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

- **Serialization integration.** Current save/load workflows expect explicit
  control over component registry and instantiation; we need to ensure `esper`
  can provide the same or an adaptation layer can be built.
- **Custom component hooks.** If we rely on component callbacks today, those would
  need to move into systems or an adapter layer.
- **Event handling model.** `esper` does not provide a first-class event bus; we
  should define a consistent event system (e.g., event components + system that
  drains them).
- **Performance considerations.** The game is not currently performance-bound, but
  any heavy use of Python reflection in `esper` should be profiled once the
  migration is underway.

## Integration approach (if we adopt `esper`)

1. **Introduce an adapter layer** in the engine core that wraps `esper.World` and
   provides the current component manager API where needed.
2. **Define a serialization contract** for components (data-only, ideally
   dataclasses) so save/load stays deterministic.
3. **Move behavior out of components** by migrating event listeners and actor
   subclasses into systems.
4. **Deprecate component inheritance** by creating data-only replacements and
   migrating entity construction.
5. **Remove the old component manager** once systems and entity creation are fully
   migrated.

## Next steps

- Prototype a thin `esper` adapter in a branch and validate:
  - Component registration and queries.
  - Save/load integration for a limited subset of components.
  - Event dispatch via event components + system drain.
- Inventory existing components and classify:
  - Data-only (safe to migrate quickly).
  - Behavior-heavy (requires system extraction).
- Decide go/no-go based on serialization and ergonomics after the prototype.
