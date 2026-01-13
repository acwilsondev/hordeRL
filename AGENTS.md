# AGENTS

## Architecture

- **Prefer SOLID object-oriented design.**
  - **S — Single Responsibility:** each class/module does one job; avoid “god objects.”
  - **O — Open/Closed:** extend via new classes/composition over modifying existing logic.
  - **L — Liskov Substitution:** subclasses must be drop-in compatible with their base types.
  - **I — Interface Segregation:** small, focused interfaces over wide, do-everything ones.
  - **D — Dependency Inversion:** depend on abstractions; inject dependencies instead of hard-coding them.

- **Prefer composition over inheritance.**
  - Use inheritance only when there’s a real “is-a” relationship and shared behavior is stable.

- **Keep boundaries explicit.**
  - Core logic should not depend on UI/rendering/IO details.
  - Side effects live at the edges (files, network, rendering, time).

- **Organize the project into four layers (strict-ish boundaries).**
  1. **Engine level core**
     - Hardened, platform-grade code.
     - Target: **80–90% test coverage**.
     - **In-depth documentation**.
     - Keep complexity low: **Radon CC A+**.
     - Should encapsulate TCOD.
     - Aggressively gate what belongs here:
       - Only systems that make sense for **multiple game projects**.
       - Prefer small, stable primitives and boring APIs.

  2. **Middleware**
     - Shared abstractions used across multiple features.
     - Target: **60–80% test coverage**.
     - Documentation:
       - Public APIs: docstrings required.
       - Private APIs: comment-level notes for gotchas.
     - Keep complexity low-moderate: **Radon CC B+**
     - **May depend on Engine core.**
     - “Reusable across roguelikes” is a nice-to-have, not a requirement.

  3. **Feature layer**
     - Game rules + gameplay implementation built on Middleware + Engine.
     - Allowed to be pragmatic / quick.
     - Target: **40–60% test coverage**.
     - Documentation:
       - Public APIs: docstrings required.
       - Private APIs: not required.
     - May depend on Middleware and Engine Core.
     - **Radon CC C+**

  4. **Game Design layer**
     - Prefer **data-driven design** (configs, tables, content packs).
     - Implemented/validated by Feature layer code.

## Documentation

- **All classes must have docstrings describing their purpose.**
  - Focus on what the class is responsible for (and what it is not).

- **Public methods/functions must have comprehensive docstrings.**
  - Include:
    - intent / behavior
    - parameters + expected types/shape
    - return value
    - side effects (state changes, IO, timing)
    - raised errors (if relevant)
    - invariants / constraints (if relevant)

- **Private methods/functions should use “comment-style” notes for gotchas.**
  - Keep it short and practical:
    - assumptions
    - edge cases
    - “why this is weird”
    - performance footguns
    - ordering constraints

- **New code areas (directories) require a README.**
  - Must briefly explain:
    - the domain this directory owns
    - core responsibilities and key concepts
    - feature verticals contained within it (what lives here vs elsewhere)
  - Keep it short: a quick orientation, not a full spec.

## Testing

- **New files require tests.**
  - If you add a new module/class/function with meaningful behavior, add tests for it.
  - “New file” includes refactors that split logic into a new file.

- **Changes to existing files without tests do not require adding tests.**
  - If the file already has no tests, you may ship changes without creating new test coverage.
  - If the file already has tests, keep them passing and update them when behavior changes.

- **Prefer tests when risk is non-trivial.**
  - Add/adjust tests when changing core logic, edge cases, parsing, state transitions, or anything likely to regress.
  - Skip tests for pure formatting, comments, or trivial renames.

## Committing

- **Use Conventional Commits whenever possible.**
  - Format: `type(scope): short summary`
  - Examples:
    - `feat(ui): add biome picker`
    - `fix(engine): prevent scheduler drift`
    - `refactor(map): split tile rendering`
    - `test(engine): add timed actor tests`
    - `docs: update agent rules`

- **Keep commits small and intention-revealing.**
  - One change theme per commit.
  - Avoid bundling drive-by refactors with behavior changes unless necessary.
