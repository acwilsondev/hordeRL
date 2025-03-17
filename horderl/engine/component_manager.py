import logging
from collections import defaultdict
from typing import Callable, Dict, Generic, Iterable, List, Set, Type

from ..components.base_components.component import Component
from ..engine import constants
from ..engine.core import log_debug
from ..engine.types import (
    ComponentList,
    ComponentType,
    EntityDict,
    EntityDictIndex,
    T,
    U,
)


class ComponentManager(object):
    """
    Manage game entities and their components within the entity-component system.

    The ComponentManager serves as the central repository for all game entities and their
    associated components. It provides methods for creating, retrieving, modifying and
    deleting entities and components. The class maintains several indexes to enable
    efficient access patterns:

    1. Components by type - Access all components of a certain type
    2. Components by entity - Access all components belonging to a specific entity
    3. Components by ID - Direct access to individual components by their unique ID

    The class also provides stashing functionality to temporarily remove entities or
    components from the active game state without destroying them, allowing them to be
    restored later.

    """

    def __init__(self):
        """
        Initialize a new ComponentManager with empty component collections.

        Creates the following data structures:
        - components: Maps component types to lists of components
        - components_by_entity: Maps entity IDs to dictionaries of components by type
        - components_by_id: Maps component IDs to component instances
        - component_types: List of all registered component types
        - stashed_components: Holds components that have been temporarily removed
        - stashed_entities: Maps entity IDs to sets of stashed component IDs

        """
        self.components: Dict[ComponentType, ComponentList] = defaultdict(list)
        self.components_by_entity: EntityDictIndex = defaultdict(
            lambda: defaultdict(list)
        )
        self.components_by_id: Dict[int, Component] = {}
        self.component_types: List[ComponentType] = []
        self.stashed_components: Dict[int, Component] = {}

        # A mapping from the entity id to the related stashed base_components
        self.stashed_entities: Dict[int, Set[int]] = {}

    # properties
    # properties
    @property
    def entities(self) -> Set[int]:
        """
        Get a set of all entity IDs currently tracked by the component manager.

        :return: A set containing the unique ID of each entity in the system
        :rtype: Set[int]

        """
        return set(k for k in self.components_by_entity.keys())

    def _add_component_to_indexes(self, component: T, component_type: Type[T]) -> None:
        """
        Add a component to ComponentManager's indexes.

        Updates the internal indexes to include the given component under its entity and
        component type.

        :param component: The component instance to add to the indexes
        :type component: T
        :param component_type: The type of the component
        :type component_type: Type[T]
        :return: None

        """
        entity_component_dict = self.components_by_entity[component.entity]
        components = entity_component_dict[component_type]
        components.append(component)
        self.components_by_id[component.id] = component

    @log_debug(__name__)
    def clear(self) -> None:
        """
        Clear all active components and entities from the component manager.

        Resets all component collections to their initial empty state. Note that this
        doesn't have any impact on persistence.

        :return: None

        """
        self.components = defaultdict(list)
        self.components_by_entity = defaultdict(lambda: defaultdict(list))
        self.components_by_id = {}
        self.component_types = []
        self.stashed_components = {}

    # data manipulation methods
    def add(self, component: Component, *components: Component) -> None:
        """
        Add one or more components to the ComponentManager.

        Each component is added to all relevant indexes in the component manager, making
        it accessible through various query methods.

        :param component: The first component to add
        :type component: Component
        :param components: Additional components to add
        :type components: Component
        :return: None

        """
        self._add(component)
        for component in components:
            self._add(component)

    def get(
        self,
        component_type: T,
        query: Callable[[T], bool] = lambda x: True,
        project: Callable[[T], U] = lambda x: x,
    ) -> List[U]:
        """
        Get all components of a given type, filtered and transformed as specified.

        Retrieves components of the specified type, applies a filtering function, and
        then transforms each result with a projection function.

        :param component_type: The component type to select
        :type component_type: T
        :param query: A boolean function to filter the components
        :type query: Callable[[T], bool]
        :param project: A transformation function applied to each selected component
        :type project: Callable[[T], U]
        :return: A list of transformed components that pass the query filter
        :rtype: List[U]

        """
        return [project(x) for x in self.components[component_type] if query(x)]

    def get_entity(self, entity: int) -> EntityDict:
        """
        Get a dictionary representing all components attached to an entity.

        Returns a dictionary mapping component types to lists of component instances
        that belong to the specified entity.

        :param entity: The ID of the entity to query
        :type entity: int
        :return: A dictionary mapping component types to lists of components
        :rtype: EntityDict

        """
        return self.components_by_entity[entity]

    def get_all(self, component_type: Type[T], entity: int) -> List[T]:
        """
        Get all components of a given type for a given entity.

        Retrieves all components of the specified type that are attached to the
        specified entity.

        :param component_type: The type of components to retrieve
        :type component_type: Type[T]
        :param entity: The ID of the entity to query
        :type entity: int
        :return: A list of components of the specified type attached to the entity
        :rtype: List[T]

        """
        return self.components_by_entity[entity][component_type]

    # TODO consider whether we really want to support this.
    def get_one(self, component_type: Type[T], entity: int) -> Generic[T]:
        """
        Get a single component of a given type for a given entity.

        Retrieves the first component of the specified type that is attached to the
        specified entity. If no such component exists, returns None.

        :param component_type: The type of component to retrieve
        :type component_type: Type[T]
        :param entity: The ID of the entity to query
        :type entity: int
        :return: The first component of the specified type, or None if none exists
        :rtype: T or None

        """
        output = self.components_by_entity[entity][component_type]
        if output:
            return output[0]
        return None

    def get_component_by_id(self, cid: int) -> Component:
        """
        Get a specific component by its unique component ID.

        Directly retrieves a component instance using its unique identifier.

        :param cid: The unique ID of the component to retrieve
        :type cid: int
        :return: The component with the specified ID
        :rtype: Component
        :raises KeyError: If no component with the specified ID exists

        """
        return self.components_by_id[cid]

    def delete(self, entity: int) -> None:
        """
        Delete an entity and all its components from the component manager.

        Removes all components attached to the specified entity and removes the entity
        itself from the component manager's indexes. Does not delete any references to
        the entity or its components that might exist elsewhere in the game.

        :param entity: The ID of the entity to delete
        :type entity: int
        :return: None
        :raises ValueError: If the provided entity is not an integer

        """
        if not isinstance(entity, int):
            raise ValueError(
                f"Cannot delete entity {entity}. Did you mean delete_component?"
            )

        logging.debug(f"System::ComponentManager deleting entity {entity}")
        components = self.get_entity(entity)

        for _, component_list in components.items():
            for component in component_list:
                self.delete_component(component)
        if entity in self.entities:
            self._delete_entity_from_indexes(entity)

    def delete_all(self, entities: Iterable[int]) -> None:
        """
        Delete multiple entities and all their components.

        Iterates through the provided collection of entity IDs and deletes each one
        along with its components.

        :param entities: An iterable collection of entity IDs to delete
        :type entities: Iterable[int]
        :return: None

        """
        for entity in entities:
            self.delete(entity)

    def _delete_entity_from_indexes(self, entity: int) -> None:
        """
        Remove an entity from all component manager indexes.

        Removes the specified entity from the internal indexes without affecting the
        individual components themselves.

        :param entity: The ID of the entity to remove from indexes
        :type entity: int
        :return: None

        """
        components = self.components_by_entity[entity]
        for component_type, components in components.items():
            for component in components:
                self.components[component_type].remove(component)
        del self.components_by_entity[entity]

    def delete_component(self, component: Component) -> None:
        """
        Delete a single component from the component manager.

        Removes the component from all indexes in the component manager. Does not delete
        any references to the component that might exist elsewhere.

        :param component: The component to delete
        :type component: Component
        :return: None
        :raises ValueError: If the component is None

        """
        logging.debug(f"System::ComponentManager deleting component {component}")
        if not component:
            raise ValueError("Cannot delete None.")
        entity = component.entity

        component.on_component_delete(self)

        if entity in self.entities:
            component_types = type(component).mro()
            for component_type in component_types:
                if component in self.components[component_type]:
                    self.components[component_type].remove(component)
                if (
                    component
                    in self.components_by_entity[component.entity][component_type]
                ):
                    self.components_by_entity[component.entity][component_type].remove(
                        component
                    )
            if component.id in self.components_by_id:
                del self.components_by_id[component.id]

    def delete_components(self, component_type: ComponentType) -> None:
        components_to_delete = [c for c in self.components[component_type]]
        for component in components_to_delete:
            self.delete_component(component)

    # stashing
    def stash_component(self, cid: int):
        assert isinstance(cid, int), "cid must be an int"

        # todo can leak stashed base_components if the managing entity is destroyed before the stash is recalled
        logging.debug(f"System::ComponentManager attempting to stash component {cid}")
        component = self.get_component_by_id(cid)
        logging.debug(f"System::ComponentManager stashing component {component}")
        self.stashed_components[cid] = component
        self.delete_component(component)

    def unstash_component(self, cid: int):
        assert isinstance(cid, int), "cid must be an int"

        logging.debug(f"System::ComponentManager attempting to unstash component {cid}")
        component = self.stashed_components[cid]
        self.add(component)
        del self.stashed_components[cid]
        return component

    def stash_entity(self, eid: int):
        """
        Move an entire entity to the stash.

        Temporarily removes an entity and all its components from the active game state
        and places them in the stash for later retrieval.

        :param eid: The ID of the entity to stash
        :type eid: int
        :return: None

        """
        assert isinstance(eid, int), "eid must be an int"
        logging.debug(f"System::ComponentManager attempting to stash entity {eid}")
        components = self.get_entity(eid)

        component_ids = set()

        for _, component_list in components.items():
            for component in component_list:
                component_ids.add(component.id)
                self.stash_component(component.id)

        self.stashed_entities[eid] = component_ids
        logging.debug(f"System::ComponentManager completed stash {component_ids}")

    def unstash_entity(self, eid):
        logging.debug(f"System::ComponentManager attempting to unstash entity {eid}")
        component_ids = list(self.stashed_entities[eid])
        for component_id in component_ids:
            self.unstash_component(component_id)

        del self.stashed_entities[eid]
        logging.debug(f"System::ComponentManager completed unstash")

    def drop_stashed_entity(self, eid):
        """
        Forget about a stashed entity.
        """
        logging.debug(
            f"System::ComponentManager attempting to drop stashed entity {eid}"
        )
        self.unstash_entity(eid)
        self.delete(eid)
        logging.debug(f"System::ComponentManager completed stash drop")

    # serialization functions
    def get_serial_form(self):
        return {
            "active_components": self.components_by_id,
            "stashed_entities": self.stashed_entities,
            "stashed_components": self.stashed_components,
        }

    def from_data(self, loaded_data):
        active_components = [v for k, v in loaded_data["active_components"].items()]
        for _, obj in [item for item in self.components_by_id.items()]:
            self.delete_component(obj)
        self.add(*active_components)

        self.stashed_entities = loaded_data["stashed_entities"]
        self.stashed_components = loaded_data["stashed_components"]

    # private methods
    def _add(self, component: Component) -> None:
        """
        Add a component to the component manager.

        Adds the component to all relevant indexes in the component manager, organizing
        it by type, entity, and component ID.

        :param component: The component to add to the component manager
        :type component: Component
        :return: None
        :raises AssertionError: If the component has an invalid entity ID

        """
        entity = component.entity
        assert (
            entity != constants.INVALID
        ), f"Invalid entity id! {component}. Did you forget to set the owning entity?"
        component_classes = type(component).mro()
        for component_class in component_classes:
            self.components_by_entity[entity][component_class].append(component)
            self.components[component_class].append(component)
        self.components_by_id[component.id] = component
