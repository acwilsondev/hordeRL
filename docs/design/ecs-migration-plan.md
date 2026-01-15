# ECS Migration Plan (Phased)

## Goals

- Transition to a flat, data-first component model.
- Move behavior into systems and away from component inheritance.
- Evaluate and optionally adopt `esper` with minimal disruption.
- Preserve save/load integrity throughout the migration.

## Phase 0: Baseline audit and constraints

**Purpose:** Establish a shared understanding of current ECS usage and risk areas.

**Work items**

- Inventory component categories:
  - Data-only components.
  - Behavior-heavy components (event listeners, actors, callbacks).
  - Hybrid components (data + logic).
- Map critical flows:
  - Serialization and loadable component registry.
  - Entity construction entry points (content packs, factories).
  - Event dispatch paths and implicit lifecycle hooks.
- Define non-negotiables:
  - Save/load compatibility requirements.
  - Performance constraints.
  - Migration windows (what can break and when).

**Exit criteria**

- Component inventory document exists and is reviewed.
- High-risk flows are identified with owners.

## Phase 1: Flat component contract + event standardization

**Purpose:** Create a stable, data-only component contract without changing behavior.

**Work items**

- Define a minimal `Component` base that supports:
  - Identity and serialization metadata.
  - Optional lifecycle hooks (with a plan to remove them later).
- Write guidance for data-only component design (dataclasses preferred).
- Standardize event flow:
  - Event components are data-only.
  - Systems consume and clear event components.

**Exit criteria**

- New components follow the flat contract.
- Event components no longer require inheritance for behavior.

## Phase 2: System extraction for behavior-heavy components

**Purpose:** Move behavior out of components and into systems.

**Work items**

- For each behavior-heavy component:
  - Extract logic into a system.
  - Replace the component with a data-only version.
  - Update entity construction to include the data component + system wiring.
- Build “shim” systems if needed to preserve existing API surface.

**Exit criteria**

- Most gameplay behavior is system-driven.
- Component inheritance tree is significantly reduced.

## Phase 3: `esper` prototype and adapter layer

**Purpose:** Validate whether `esper` can replace or wrap the component manager.

**Work items**

- Implement a thin adapter around `esper.World` that exposes:
  - Component registration and query patterns used today.
  - Serialization hooks needed for save/load.
- Port a small vertical slice (e.g., movement + a simple event flow).
- Capture ergonomics and performance notes.

**Exit criteria**

- Prototype demonstrates feature parity for the slice.
- Decision: adopt `esper` or keep custom component manager.

## Phase 4: Migration to target ECS runtime

**Purpose:** Move the core ECS runtime to the target design (esper or custom).

**Work items**

- Migrate component manager responsibilities to the target runtime.
- Update systems to use the new query APIs.
- Maintain save/load parity by validating serialized snapshots.

**Exit criteria**

- Target runtime is the default path.
- Save/load tests pass for existing save files.

## Phase 5: Cleanup and deprecation removal

**Purpose:** Remove legacy ECS constructs and simplify codebase.

**Work items**

- Remove old component inheritance types and deprecated hooks.
- Delete adapter shims and dead code paths.
- Update docs and onboarding guides to reflect the new ECS model.

**Exit criteria**

- Legacy ECS paths removed.
- Documentation reflects the flat component + system-centric design.

## Risk management notes

- Prefer small, reversible migrations (feature slices).
- Keep serialization deterministic; treat save/load as a contract.
- Schedule refactors around gameplay milestones to reduce churn.
