from typing import Dict, List, NewType, Tuple, Type, TypeAlias, TypeVar

from engine.components.component import Component

T = TypeVar("T")
U = TypeVar("U")
EntityId = NewType("EntityId", int)
ComponentType: TypeAlias = Type[Component]
ComponentList: TypeAlias = List[Component]
Entity = NewType("Entity", Tuple[EntityId, List[Component]])
EntityDict: TypeAlias = Dict[ComponentType, List[Component]]
EntityDictIndex: TypeAlias = Dict[EntityId, EntityDict]
ComplexEntity = NewType("ComplexEntity", Tuple[EntityId, List[Entity]])
