"""Minimal engine-only example for HordeRL."""

from engine import ComponentManager, Coordinates, Entity
from engine.core import get_id


def main() -> None:
    """Create a tiny component setup to verify engine-only usage."""
    manager = ComponentManager()
    entity_id = get_id("example-entity")

    entity = Entity(id=entity_id, entity=entity_id, name="Example")
    position = Coordinates(entity=entity_id, x=3, y=7)

    manager.add(entity, position)

    stored_entities = manager.get(Entity)
    stored_positions = manager.get(Coordinates)

    print(
        f"Entities: {[e.get_readable_key() for e in stored_entities]} | "
        f"Positions: {[p.position for p in stored_positions]}"
    )


if __name__ == "__main__":
    main()
