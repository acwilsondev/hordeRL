"""
Component management system for the HordeRL entity-component architecture.

This module provides the ComponentManager class, which serves as the central
repository for all game entities and their associated components. It manages
the lifecycle of components, provides efficient access to components through
multiple indexing strategies, and supports operations such as:

- Adding and retrieving components by type, entity, or unique ID
- Removing components and entities from the game world
- Temporarily stashing and later unstashing components or entire entities
- Querying and filtering components based on custom criteria
- Serializing component state for save/load functionality

The entity-component system allows for flexible game object composition without
deep inheritance hierarchies, enabling behavior to be added or removed at runtime.
"""

from collections import defaultdict
from typing import Callable, Dict, Generic, Iterable, List, Set, Type

from engine import constants
from engine.components.component import Component
from engine.logging import get_logger
from engine.types import (
    ComponentList,
    ComponentType,
    EntityDict,
    EntityDictIndex,
    T,
    U,
)


class ComponentManager:
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
        self.logger = get_logger(__name__)
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
    @property
    def entities(self) -> Set[int]:
        """
        Get a set of all entity IDs currently tracked by the component manager.

        :return: A set containing the unique ID of each entity in the system
        :rtype: Set[int]

        """
        return set(k for k in self.components_by_entity.keys())

    def _add_component_to_indexes(
        self, component: T, component_type: Type[T]
    ) -> None:
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

    def clear(self) -> None:
        """
        Clear all active components and entities from the component manager.

        Resets all component collections to their initial empty state. Note that this
        doesn't have any impact on persistence.

        :return: None

        """
        self.logger.debug("Clearing component manager")
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
        it accessible through various query methods. All inputs are validated to ensure
        they are proper Component instances.

        :param component: The first component to add
        :type component: Component
        :param components: Additional components to add
        :type components: Component
        :return: None
        :raises TypeError: If any input is not a Component instance
        :raises ValueError: If any component has an invalid entity ID

        """
        if not isinstance(component, Component):
            self.logger.error(
                "Invalid component type provided",
                extra={
                    "expected": "Component",
                    "received": type(component).__name__,
                },
            )
            raise TypeError(
                f"Expected Component instance, got {type(component).__name__}"
            )

        self._add(component)

        for comp in components:
            if not isinstance(comp, Component):
                self.logger.error(
                    "Invalid component type provided in additional components",
                    extra={
                        "expected": "Component",
                        "received": type(comp).__name__,
                    },
                )
                raise TypeError(
                    f"Expected Component instance, got {type(comp).__name__}"
                )

            self._add(comp)

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
        return [
            project(x) for x in self.components[component_type] if query(x)
        ]

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

        If the entity also has stashed components, those are deleted as well to prevent
        stashed component leaks.

        :param entity: The ID of the entity to delete
        :type entity: int
        :return: None
        :raises ValueError: If the provided entity is not an integer

        """
        if not isinstance(entity, int):
            raise ValueError(
                f"Cannot delete entity {entity}. Did you mean"
                " delete_component?"
            )

        self.logger.debug(
            "Deleting entity",
            extra={"entity_id": entity, "operation": "delete_entity"},
        )

        # Clean up any stashed components belonging to this entity
        if entity in self.stashed_entities:
            self.logger.debug(
                "Entity has stashed components that will be removed",
                extra={
                    "entity_id": entity,
                    "stashed_component_count": len(
                        self.stashed_entities[entity]
                    ),
                },
            )
            # Remove the stashed components to prevent leaks
            self.drop_stashed_entity(entity)

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
        self.logger.debug(
            "Deleting component",
            extra={
                "component_id": component.id if component else None,
                "component_type": (
                    type(component).__name__ if component else None
                ),
                "entity_id": component.entity if component else None,
            },
        )
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
                    in self.components_by_entity[component.entity][
                        component_type
                    ]
                ):
                    self.components_by_entity[component.entity][
                        component_type
                    ].remove(component)
            if component.id in self.components_by_id:
                del self.components_by_id[component.id]

    def delete_components(self, component_type: ComponentType) -> None:
        components_to_delete = [c for c in self.components[component_type]]
        for component in components_to_delete:
            self.delete_component(component)

    # stashing
    def stash_component(self, cid: int) -> None:
        """
        Move a component to the stash.

        Temporarily removes a component from the active game state and places it in the stash
        for later retrieval.

        :param cid: The ID of the component to stash
        :type cid: int
        :return: None
        :raises ValueError: If the component ID is not an integer
        :raises KeyError: If the component ID does not exist
        """
        if not isinstance(cid, int):
            raise ValueError(
                f"Component ID must be an integer, got {type(cid).__name__}"
            )

        # todo can leak stashed base_components if the managing entity is destroyed before the stash is recalled
        self.logger.debug(
            "Attempting to stash component", extra={"component_id": cid}
        )

        try:
            component = self.components_by_id[cid]
        except KeyError:
            self.logger.error(
                "Failed to stash component: component not found",
                extra={"component_id": cid},
            )
            raise KeyError(f"Component with ID {cid} not found")

        if cid in self.stashed_components:
            self.logger.warning(
                "Component is already stashed",
                extra={
                    "component_id": cid,
                    "component_type": type(component).__name__,
                    "entity_id": component.entity,
                },
            )
            return

        self.logger.debug(
            "Stashing component",
            extra={
                "component_id": component.id,
                "component_type": type(component).__name__,
                "entity_id": component.entity,
                "operation": "stash",
            },
        )
        self.stashed_components[cid] = component
        self.delete_component(component)

    def unstash_component(self, cid: int) -> Component:
        """
        Retrieve a component from the stash and return it to the active game state.

        Moves a previously stashed component back into the active component manager.

        :param cid: The ID of the component to unstash
        :type cid: int
        :return: The unstashed component
        :rtype: Component
        :raises ValueError: If the component ID is not an integer
        :raises KeyError: If the component ID is not in the stash
        """
        if not isinstance(cid, int):
            raise ValueError(
                f"Component ID must be an integer, got {type(cid).__name__}"
            )

        self.logger.debug(
            "Attempting to unstash component", extra={"component_id": cid}
        )

        try:
            component = self.stashed_components[cid]
        except KeyError:
            self.logger.error(
                "Failed to unstash component: component not found in stash",
                extra={"component_id": cid},
            )
            raise KeyError(f"Component with ID {cid} not found in stash")

        self.logger.debug(
            "Unstashing component",
            extra={
                "component_id": component.id,
                "component_type": type(component).__name__,
                "entity_id": component.entity,
                "operation": "unstash",
            },
        )

        self.add(component)
        del self.stashed_components[cid]
        return component

    def stash_entity(self, eid: int) -> None:
        """
        Move an entire entity to the stash.

        Temporarily removes an entity and all its components from the active game state
        and places them in the stash for later retrieval. If the entity is already
        stashed, this will log a warning and do nothing.

        :param eid: The ID of the entity to stash
        :type eid: int
        :return: None
        :raises ValueError: If eid is not an integer
        :raises ValueError: If entity has no components
        """
        if not isinstance(eid, int):
            self.logger.error(
                "Invalid entity ID type provided",
                extra={
                    "expected": "int",
                    "received": type(eid).__name__,
                    "entity_id": str(eid),
                },
            )
            raise ValueError(
                f"Entity ID must be an integer, got {type(eid).__name__}"
            )

        if eid in self.stashed_entities:
            self.logger.warning(
                "Entity is already stashed", extra={"entity_id": eid}
            )
            return

        self.logger.debug(
            "Attempting to stash entity",
            extra={"entity_id": eid, "operation": "stash_entity"},
        )

        components = self.get_entity(eid)
        component_ids = set()

        # Check if the entity has any components
        has_components = False
        for _, component_list in components.items():
            if component_list:
                has_components = True
                break

        if not has_components:
            self.logger.warning(
                "No components found for entity", extra={"entity_id": eid}
            )

        # Process components
        for _, component_list in components.items():
            for component in component_list:
                component_ids.add(component.id)
                self.stash_component(component.id)

        self.stashed_entities[eid] = component_ids
        self.logger.info(
            "Completed entity stash",
            extra={
                "entity_id": eid,
                "component_count": len(component_ids),
                "component_ids": list(component_ids),
                "operation": "stash_entity_complete",
            },
        )

    def unstash_entity(self, eid: int) -> None:
        """
        Retrieve a stashed entity and return it to the active game state.

        Moves a previously stashed entity and all its components back into the active
        component manager.

        :param eid: The ID of the entity to unstash
        :type eid: int
        :return: None
        :raises ValueError: If eid is not an integer
        :raises KeyError: If the entity ID is not in the stash
        """
        if not isinstance(eid, int):
            self.logger.error(
                "Invalid entity ID type provided",
                extra={
                    "expected": "int",
                    "received": type(eid).__name__,
                    "entity_id": str(eid),
                },
            )
            raise ValueError(
                f"Entity ID must be an integer, got {type(eid).__name__}"
            )

        self.logger.debug(
            "Attempting to unstash entity",
            extra={"entity_id": eid, "operation": "unstash_entity"},
        )

        if eid not in self.stashed_entities:
            self.logger.error(
                "Failed to unstash entity: entity not found in stash",
                extra={"entity_id": eid},
            )
            raise KeyError(f"Entity with ID {eid} not found in stash")

        component_ids = list(self.stashed_entities[eid])
        unstashed_count = 0

        for component_id in component_ids:
            try:
                self.unstash_component(component_id)
                unstashed_count += 1
            except KeyError:
                self.logger.warning(
                    "Component in stashed entity not found in stash",
                    extra={"entity_id": eid, "component_id": component_id},
                )

        del self.stashed_entities[eid]
        self.logger.info(
            "Completed entity unstash",
            extra={
                "entity_id": eid,
                "component_count": len(component_ids),
                "unstashed_count": unstashed_count,
                "operation": "unstash_entity_complete",
            },
        )

    def drop_stashed_entity(self, eid: int) -> None:
        """
        Permanently remove a stashed entity and its components.

        This method cleanly removes an entity from the stash without returning it to the
        active game state. This helps prevent stashed component leaks by ensuring all
        components associated with the entity are properly cleaned up and removed.

        :param eid: The ID of the entity to drop from the stash
        :type eid: int
        :return: None
        :raises ValueError: If eid is not an integer
        :raises KeyError: If the entity ID is not in the stash
        """
        if not isinstance(eid, int):
            self.logger.error(
                "Invalid entity ID type provided",
                extra={
                    "expected": "int",
                    "received": type(eid).__name__,
                    "entity_id": str(eid),
                },
            )
            raise ValueError(
                f"Entity ID must be an integer, got {type(eid).__name__}"
            )

        self.logger.debug(
            "Attempting to drop stashed entity",
            extra={"entity_id": eid, "operation": "drop_stashed_entity"},
        )

        if eid not in self.stashed_entities:
            self.logger.error(
                "Failed to drop stashed entity: entity not found in stash",
                extra={"entity_id": eid},
            )
            raise KeyError(f"Entity with ID {eid} not found in stash")

        # Directly remove components from stash instead of unstashing them
        component_ids = list(self.stashed_entities[eid])
        self.logger.debug(
            "Removing stashed components",
            extra={
                "entity_id": eid,
                "component_count": len(component_ids),
                "component_ids": component_ids,
            },
        )

        for component_id in component_ids:
            if component_id in self.stashed_components:
                del self.stashed_components[component_id]

        # Remove the entity from stashed entities
        del self.stashed_entities[eid]

        self.logger.info(
            "Completed stashed entity drop",
            extra={
                "entity_id": eid,
                "component_count": len(component_ids),
                "operation": "drop_stashed_entity_complete",
            },
        )

    # serialization functions
    def get_serial_form(self):
        return {
            "active_components": self.components_by_id,
            "stashed_entities": self.stashed_entities,
            "stashed_components": self.stashed_components,
        }

    def from_data(self, loaded_data):
        active_components = [
            v for k, v in loaded_data["active_components"].items()
        ]
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
        it by type, entity, and component ID. Validates that the component has a valid
        entity ID before adding it to the system.

        :param component: The component to add to the component manager
        :type component: Component
        :return: None
        :raises ValueError: If the component has an invalid entity ID
        :raises TypeError: If the input is not a Component instance

        """
        if not isinstance(component, Component):
            self.logger.error(
                "Invalid component type provided to _add",
                extra={
                    "expected": "Component",
                    "received": type(component).__name__,
                },
            )
            raise TypeError(
                f"Expected Component instance, got {type(component).__name__}"
            )

        entity = component.entity
        if entity == constants.INVALID:
            self.logger.error(
                "Component has invalid entity ID",
                extra={
                    "component_id": getattr(component, "id", None),
                    "component_type": type(component).__name__,
                    "entity_id": entity,
                },
            )
            raise ValueError(
                f"Invalid entity ID! {component}. Did you forget to set the"
                " owning entity?"
            )

        self.logger.debug(
            "Adding component",
            extra={
                "component_id": component.id,
                "component_type": type(component).__name__,
                "entity_id": entity,
                "operation": "add",
            },
        )

        component_classes = type(component).mro()
        for component_class in component_classes:
            self.components_by_entity[entity][component_class].append(
                component
            )
            self.components[component_class].append(component)
        self.components_by_id[component.id] = component
