# Ability Systems

This directory contains systems that coordinate ability selection and
ability-driven spawning. It owns the runtime logic for cycling through
abilities and for translating placement-oriented ability actors into
game entities.

**Responsibilities**
- Selecting the active ability for a tracked entity.
- Spawning entities described by placement ability actors.

**Contained systems**
- Ability selection (cycling between abilities).
- Placement spawning (building, hiring, or deploying entities).
