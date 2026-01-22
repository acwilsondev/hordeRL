# World Building Systems

This directory owns systems that assemble world-building parameters used during
procedural generation. It houses small factories and helpers that translate
configuration inputs into `WorldParameters` values consumed by world-building
systems.

Key concepts:
- Parameter factories for biome presets.
- Seed selection logic that isolates randomness from data components.

Feature verticals:
- Parameter construction for biomes lives here.
- Data-only components remain in `horderl/components/world_building`.
