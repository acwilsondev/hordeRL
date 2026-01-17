from engine.components.component import Component


class CostMapper(Component):
    """
    Data-only base component for pathfinding cost mapping.

    Systems interpret concrete subclasses to build cost grids.
    """
