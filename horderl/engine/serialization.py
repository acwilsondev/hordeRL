import dataclasses
import json
import traceback
from pathlib import Path

from ..components.base_components.component import Component
from . import core
from .logging import get_logger


class EnhancedJSONEncoder(json.JSONEncoder):
    """
    Provide a dataclass encoder.
    """

    def default(self, o):
        if dataclasses.is_dataclass(o):
            data = dataclasses.asdict(o)
            data["class"] = o.__class__.__name__
            return data
        return super().default(o)


def save(components, file, extra=None):
    logger = get_logger(__name__)
    if extra is None:
        extra = {}
    
    object_count = len(components["active_components"])
    file_path = Path(file).resolve()
    
    logger.info(
        "Saving game state",
        extra={
            "action": "save",
            "file_path": str(file_path),
            "object_count": object_count,
            "stashed_count": len(components.get("stashed_components", {})),
            "extra_data": bool(extra)
        }
    )
    
    save_info = {
        "info": {
            "object_count": object_count,
            "extra": extra,
        },
        "named_ids": core.get_named_ids(),
        "objects": components,
    }

    try:
        save_data = json.dumps(save_info, cls=EnhancedJSONEncoder)
        with open(file, "w+") as f:
            f.write(save_data)
        
        logger.debug(
            "Game state successfully saved",
            extra={
                "action": "save_complete",
                "file_path": str(file_path),
                "data_size_bytes": len(save_data)
            }
        )
    except (IOError, json.JSONEncodeError) as e:
        logger.error(
            f"Failed to save game state: {str(e)}",
            extra={
                "action": "save_error",
                "file_path": str(file_path),
                "error": str(e),
                "error_type": e.__class__.__name__,
                "traceback": traceback.format_exc()
            }
        )
        raise


def load(file):
    logger = get_logger(__name__)
    file_path = Path(file).resolve()
    
    logger.info(
        f"Loading game state from {file_path}",
        extra={
            "action": "load",
            "file_path": str(file_path)
        }
    )
    
    # iterate through the modules in the current package
    loadable_classes = _gather_loadable_classes()
    logger.debug(
        f"Gathered {len(loadable_classes)} loadable component classes",
        extra={
            "action": "gather_classes",
            "class_count": len(loadable_classes),
            "classes": list(loadable_classes.keys())
        }
    )

    try:
        with open(file, "r") as f:
            data = json.load(f)
        
        logger.debug(
            "Successfully parsed save file",
            extra={
                "action": "parse_save",
                "file_path": str(file_path)
            }
        )

        core.set_named_ids(data["named_ids"])
        
        active_components = _load_from_data(
            data["objects"]["active_components"], loadable_classes
        )
        expected_count = data["info"]["object_count"]
        real_count = len(active_components)
        
        if real_count != expected_count:
            logger.warning(
                f"Mismatched objects on load expected {expected_count}, found {real_count}",
                extra={
                    "action": "load_mismatch",
                    "expected_count": expected_count,
                    "actual_count": real_count,
                    "difference": expected_count - real_count,
                    "file_path": str(file_path)
                }
            )

        stashed_components = _load_from_data(
            data["objects"]["stashed_components"], loadable_classes
        )
        
        logger.info(
            "Game state successfully loaded",
            extra={
                "action": "load_complete",
                "file_path": str(file_path),
                "active_component_count": real_count,
                "stashed_component_count": len(stashed_components),
                "stashed_entity_count": len(data["objects"]["stashed_entities"])
            }
        )

        loaded_data = {
            "active_components": active_components,
            "stashed_components": stashed_components,
            "stashed_entities": data["objects"]["stashed_entities"],
        }
        return loaded_data
    
    except (IOError, json.JSONDecodeError) as e:
        logger.error(
            f"Failed to load game state: {str(e)}",
            extra={
                "action": "load_error",
                "file_path": str(file_path),
                "error": str(e),
                "error_type": e.__class__.__name__,
                "traceback": traceback.format_exc()
            }
        )
        raise


def _load_from_data(data, loadable_classes):
    """
    Load a set of data from loadable classes.
    """
    logger = get_logger(__name__)
    active_components = {}
    
    logger.debug(
        f"Loading {len(data)} components from data",
        extra={
            "action": "load_component_data",
            "component_count": len(data)
        }
    )
    
    missing_classes = []
    loaded_count = 0
    
    for key, obj in data.items():
        obj_class = obj["class"]
        if obj_class not in loadable_classes:
            missing_classes.append(obj_class)
            logger.error(
                f"Component class not found: {obj_class}",
                extra={
                    "action": "class_not_found",
                    "missing_class": obj_class,
                    "component_id": key,
                    "available_classes": list(loadable_classes.keys())
                }
            )
            raise ValueError(f"class not found: {obj_class}")
        else:
            try:
                del obj["class"]
                clz = loadable_classes[obj_class]
                active_components[key] = clz(**obj)
                loaded_count += 1
            except Exception as e:
                logger.error(
                    f"Failed to instantiate component {obj_class}: {str(e)}",
                    extra={
                        "action": "component_instantiation_error",
                        "component_class": obj_class,
                        "component_id": key,
                        "error": str(e),
                        "error_type": e.__class__.__name__,
                        "traceback": traceback.format_exc()
                    }
                )
                raise
    
    logger.debug(
        f"Successfully loaded {loaded_count} components",
        extra={
            "action": "load_components_complete",
            "component_count": loaded_count
        }
    )
    
    return active_components


def _gather_loadable_classes():
    """
    Read the base_components directory to discover loadable base_components.
    """
    logger = get_logger(__name__)
    
    # Get available component classes
    classes = Component.subclasses
    
    logger.debug(
        f"Found {len(classes)} loadable component classes",
        extra={
            "action": "gather_loadable_classes",
            "class_count": len(classes),
            "classes": list(classes.keys())
        }
    )
    
    return classes
