from typing import Dict, List, NewType, Tuple, Type, TypeVar

from components.base_components.component import Component

T = TypeVar("T")
U = TypeVar("U")
EntityId = NewType("EntityId", int)
ComponentType = NewType("ComponentType", Type[T])
ComponentList = NewType("ComponentList", List[ComponentType])
Entity = NewType("Entity", Tuple[EntityId, List[Component]])
EntityDict = NewType("EntityDict", Dict[ComponentType, List[Component]])
EntityDictIndex = NewType("EntityIndex", Dict[EntityId, EntityDict])
ComplexEntity = NewType("ComplexEntity", Tuple[EntityId, List[Entity]])
