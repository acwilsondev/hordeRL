# Combat Systems

This directory owns gameplay systems that resolve combat-specific behavior
triggered by actions (such as attacks). It converts queued combat components
into world state changes like damage, forced movement, and combat animations.

## Responsibilities
- Resolve queued combat effects (knockback, future status effects, etc.).
- Keep combat side effects isolated from action queuing logic.

## Scope
- Effect resolution belongs here.
- Action creation and input handling live elsewhere in `horderl/systems`.
