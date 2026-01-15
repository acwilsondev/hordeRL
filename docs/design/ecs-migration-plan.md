# ECS Migration Plan (Phased)

## Goals

- Transition to a flat, data-first component model.
- Move behavior into systems and away from component inheritance.
- Evaluate and optionally adopt `esper` with minimal disruption.
- Preserve save/load integrity throughout the migration.

## DONE Phase 0: Baseline audit and constraints

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

Done: [doc](./ecs-phase0-audit.md)

## Phase 1: Flat component contract + boundaries

**Purpose:** Create a stable, data-only component contract without changing behavior.

**Work items**

- Define the component contract as plain `@dataclass` records:
  - Identity and serialization metadata (dataclass <-> dict stays intact).
  - Reference: [ECS component contract](./ecs-component-contract.md).
- Document ID stability rules (creation, reassignment, and load semantics).
- Write guidance for data-only component design (dataclasses preferred).
- Confirm ownership boundaries:
  - ECS and serialization do not directly depend on one another.
  - The scene orchestrates creation, component assignment, and ser/de.

**Exit criteria**

- New components follow the flat contract.
- Behavior lives in systems; event components are optional, not required.

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

## Phase 3: Project split decision

**Purpose:** Decide when to pursue `esper` after the ECS cleanup stabilizes.

**Work items**

- Review Project A outcomes (flat components + system-first behavior).
- Decide whether `esper` integration is still needed.

**Exit criteria**

- Decision documented: proceed with Project B or stay with the custom manager.

## Phase 4: Project B (optional) `esper` adapter + slice

**Purpose:** Validate whether `esper` can replace or wrap the component manager.

**Work items**

- Implement a thin adapter around `esper.World` that exposes:
  - Component registration and query patterns used today.
  - Lifecycle hooks needed by existing systems.
- Port a small vertical slice (e.g., movement + a simple event flow).
- Capture ergonomics, serialization integration, and performance notes.

**Exit criteria**

- Prototype demonstrates feature parity for the slice.
- Decision: adopt `esper` or keep custom component manager.

## Phase 5: Migration to target ECS runtime (if adopting `esper`)

**Purpose:** Move the core ECS runtime to the target design (esper or custom).

**Work items**

- Migrate component manager responsibilities to the target runtime.
- Update systems to use the new query APIs.
- Maintain save/load parity by validating serialized snapshots.

**Exit criteria**

- Target runtime is the default path.
- Save/load tests pass for existing save files.

## Phase 6: Cleanup and deprecation removal

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
