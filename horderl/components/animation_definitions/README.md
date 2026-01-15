# Animation Definitions

This directory contains data-only components that describe animation behavior.
Each definition captures the configuration and runtime state required by the
animation controller systems in `horderl/systems`, without embedding any logic.

## Responsibilities

- Store animation timing, parameters, and runtime state.
- Keep animation data separate from the systems that execute animation logic.

## Contents

- Data components for blink, float, path, sequence, and related animations.
- Definitions intended to be composed onto entities that should animate.
