from dataclasses import dataclass

from components import Coordinates
from components.actors.seasonal_actor import SeasonalActor
from components.house_structure import HouseStructure
from components.owner import Owner
from content.houses import make_wall

@dataclass
class Rebuilder(SeasonalActor):
    """Rebuilds broken down house walls."""
    def act(self, scene):
        house_link = scene.cm.get_one(Owner, entity=self.entity)
        if not house_link:
            raise NotImplementedError("cannot yet handle rebuilder without parent entity")
        house_id = house_link.owner

        house_structures = [hs for hs in scene.cm.get(HouseStructure) if hs.house_id == house_id]
        assert len(house_structures) == 1, "can only have one house structure"
        house_structure = house_structures.pop()
        coords = scene.cm.get_one(Coordinates, entity=house_structure.entity)
        x = coords.x
        y = coords.y

        upper_left = make_wall(house_id, x - 1, y - 1)
        upper_middle = make_wall(house_id, x, y - 1)
        upper_right = make_wall(house_id, x + 1, y - 1)
        middle_left = make_wall(house_id, x - 1, y)
        middle_right = make_wall(house_id, x + 1, y)
        bottom_left = make_wall(house_id, x - 1, y + 1)
        bottom_middle = make_wall(house_id, x, y + 1)
        bottom_right = make_wall(house_id, x + 1, y + 1)

        house_structure.upper_left = upper_left[0]
        house_structure.upper_middle = upper_middle[0]
        house_structure.upper_right = upper_right[0]
        house_structure.middle_left = middle_left[0]
        house_structure.middle_right = middle_right[0]
        house_structure.bottom_left = bottom_left[0]
        house_structure.bottom_middle = bottom_middle[0]
        house_structure.bottom_right = bottom_right[0]

        for wall in [
            upper_left, upper_middle, upper_right,
            middle_left, middle_right,
            bottom_left, bottom_middle, bottom_right
        ]:
            scene.cm.add(*wall[1])
