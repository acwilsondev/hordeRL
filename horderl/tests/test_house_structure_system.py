from horderl.components.house_structure import HouseStructure
from horderl.systems.house_structure_system import get_house_structure_tiles


def test_get_house_structure_tiles_orders_tiles() -> None:
    house_structure = HouseStructure(
        upper_left=1,
        upper_middle=2,
        upper_right=3,
        middle_left=4,
        middle_right=5,
        bottom_left=6,
        bottom_middle=7,
        bottom_right=8,
    )

    assert get_house_structure_tiles(house_structure) == [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
    ]
