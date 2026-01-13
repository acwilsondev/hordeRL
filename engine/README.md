# HordeRL Engine API Guide

This document summarizes the stable public surface of the `engine` package,
including the scene lifecycle, initialization flow, and recommended imports.

## Initialization

At a minimum, a project needs to:

1. Create a GUI and UI context adapter.
2. Build a `GameSceneController`.
3. Push an initial `GameScene` instance.
4. Call `start()` to enter the scene loop.

```python
from engine import GameSceneController
from engine.ui import Gui, GuiAdapter

# Project-provided configuration, popup factory, and track registry.
config = load_config()
tracks = {"main": "assets/music/main.ogg"}

gui = Gui(width=80, height=50, title="HordeRL", font_path="assets/font.png")
ui_context = GuiAdapter(gui, popup_factory=create_popup)

controller = GameSceneController(
    title="HordeRL",
    config=config,
    gui=gui,
    ui_context=ui_context,
    tracks=tracks,
)
controller.push_scene(TitleScene())
controller.start()
```

If you are swapping out rendering or UI behavior, implement the `UiContext`
protocol and pass that implementation into the controller.

## Scene lifecycle

`GameScene` defines the scene lifecycle hooks in the following order:

1. `on_load()`
2. `before_update(dt)`
3. `update(dt)`
4. `render(dt)`
5. `on_unload()`

Only override lifecycle hooks (`on_load`, `before_update`, `update`, `render`,
`on_unload`). The `load()` method is final and should not be overridden.

## Minimal stable imports

When consuming the engine from downstream code, prefer these imports:

```python
from engine import (
    Actor,
    Component,
    ComponentManager,
    Coordinates,
    EnergyActor,
    Entity,
    GameScene,
    GameSceneController,
    Gui,
    GuiAdapter,
    GuiElement,
    UiContext,
    VerticalAnchor,
)
```

These are the stable, supported entry points. Anything not re-exported from
`engine.__init__` or `engine.ui` should be treated as internal implementation
and may change without notice.

## Module stability notes

- `engine.components` re-exports the component base classes and common
  components. Other modules in that package are internal.
- `engine.ui` re-exports the stable UI primitives and adapters.
- The `engine.sound` package is intended for internal use unless explicitly
  imported by downstream projects.
