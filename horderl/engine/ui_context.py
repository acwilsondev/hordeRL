from typing import Any, Protocol


class UiContext(Protocol):
    @property
    def gui(self) -> Any:
        ...

    def clear_root(self) -> None:
        ...

    def render_element(self, element: Any) -> None:
        ...

    def render_single_shot(self, element: Any) -> None:
        ...

    def create_popup(self, message: str, config: Any) -> Any:
        ...
