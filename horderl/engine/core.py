"""
Core utilities and foundational functions for the HordeRL engine.

This module provides essential utility functions that serve as the foundation
for the game engine's operations. It includes functionality for event handling,
time measurement, procedural generation, unique ID management, and performance
monitoring through decorators.

Key features include:
- Keyboard event handling and input processing
- High-precision timing utilities for performance monitoring
- Noise generation for procedural content creation
- Unique ID generation and name-to-ID mapping management
- Decorator utilities for function timing and debug logging
"""

from time import perf_counter_ns

import tcod.event
import tcod.noise

from horderl.engine.logging import get_logger


def time_ms():
    """
    Get the current time in milliseconds.

    This function uses a high-precision performance counter and converts nanoseconds to
    milliseconds. It's useful for timing operations and calculating elapsed time.

    :return: Current time in milliseconds
    :rtype: int

    """
    logger = get_logger("core")
    result = int(perf_counter_ns() / 1000000)
    logger.debug("Time measured", extra={"result_ms": result})
    return result


def timed(ms, module):
    """
    Decorator to log functions that take longer than the specified time to execute.

    This decorator wraps functions to measure their execution time and logs a warning if
    the execution time exceeds the specified threshold. It preserves the return value of
    the wrapped function.

    :param ms: The threshold time in milliseconds
    :type ms: int
    :param module: The module name used for logging
    :type module: str
    :return: A decorator function that wraps the target function
    :rtype: callable

    """

    def outer(func):
        def inner(*args, **kwargs):
            logger = get_logger(module)
            logger.debug(
                "Starting timed function execution",
                extra={
                    "function": func.__name__,
                    "threshold_ms": ms,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs),
                },
            )

            t0 = time_ms()
            result = func(*args, **kwargs)
            t1 = time_ms()
            duration = t1 - t0

            # Always log the duration for performance tracking
            logger.debug(
                "Completed timed function execution",
                extra={
                    "function": func.__name__,
                    "duration_ms": duration,
                    "threshold_ms": ms,
                    "threshold_exceeded": duration > ms,
                },
            )

            # Warn if the threshold is exceeded
            if duration > ms:
                logger.warning(
                    "Function execution exceeded time threshold",
                    extra={
                        "function": func.__name__,
                        "duration_ms": duration,
                        "threshold_ms": ms,
                        "args_count": len(args),
                        "kwargs_count": len(kwargs),
                    },
                )
            return result

        return inner

    return outer


def log_debug(module):
    """
    DEPRECATED: Use direct logger calls instead.
    This decorator will be removed in a future version.

    Example of direct logging:
        logger = get_logger("module_name")
        logger.debug("Message", extra={"key": "value"})
    """
    import warnings

    warnings.warn(
        "log_debug decorator is deprecated. Use direct logger.debug() calls"
        " instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    def outer(fn):
        def decorated(*args, **kwargs):
            logger = get_logger(module)
            try:
                start = time_ms()
                logger.debug(
                    "Function entry",
                    extra={
                        "function": fn.__name__,
                        "event": "function_entry",
                        "function_args": str(args),
                        "function_kwargs": str(kwargs),
                    },
                )

                result = fn(*args, **kwargs)

                duration = time_ms() - start
                logger.debug(
                    "Function exit",
                    extra={
                        "function": fn.__name__,
                        "event": "function_exit",
                        "duration_ms": duration,
                        "return_value": str(result),
                    },
                )
                return result
            except Exception as ex:
                logger.error(
                    "Exception encountered",
                    extra={
                        "function": fn.__name__,
                        "event": "function_exception",
                        "exception_type": type(ex).__name__,
                        "exception_message": str(ex),
                    },
                    exc_info=True,
                )
                raise

        return decorated

    return outer


@timed(10, "core")
def get_key_event():
    """
    Handle tcod key events and return keyboard input.

    This function processes all pending events and returns the first KEYDOWN event
    encountered. If no KEYDOWN event is found, returns None.

    :return: The key press event if one occurred
    :rtype: tcod.event.KeyDown or None
    :raises RuntimeError: If a system-level event handling error occurs
    :raises Exception: For any other unexpected errors during event processing
    """

    logger = get_logger("core")
    try:
        poll_start = time_ms()
        logger.debug(
            "Processing pending events",
            extra={"action": "get_key_event", "timestamp": poll_start},
        )
        events = tcod.event.get()
        poll_end = time_ms()
        poll_duration = poll_end - poll_start

        if poll_duration > 5:  # Log if polling takes more than 5ms
            logger.info(
                "Event polling duration exceeded threshold",
                extra={
                    "action": "get_key_event",
                    "poll_duration_ms": poll_duration,
                    "events_count": len(events),
                },
            )

        logger.debug(
            "Retrieved events from event queue",
            extra={
                "action": "get_key_event",
                "events_count": len(events),
                "poll_duration_ms": poll_duration,
            },
        )

        for event in events:
            if event.type == "KEYDOWN":
                logger.debug(
                    "Key event detected",
                    extra={
                        "action": "get_key_event",
                        "event_type": event.type,
                        "sym": event.sym,
                        "scancode": event.scancode,
                    },
                )
                return event
        logger.debug("No key events found", extra={"action": "get_key_event"})
        return None
    except tcod.event.EventError as e:
        logger.error(
            "TCOD event error",
            extra={
                "action": "get_key_event",
                "error_type": "EventError",
                "error_message": str(e),
            },
        )
        raise RuntimeError(f"Error retrieving event: {e}") from e
    except Exception as e:
        logger.error(
            "Unexpected error processing events",
            extra={
                "action": "get_key_event",
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
            exc_info=True,
        )
        raise


def wait_for_char():
    """
    Wait for a character key press and return the corresponding event.

    This function blocks until a key is pressed. It will immediately return when any key
    is pressed, but specifically checks for the Enter/Return key.

    :return: The keyboard event that was triggered
    :rtype: tcod.event.KeyDown
    :raises RuntimeError: If a system-level event handling error occurs
    :raises TimeoutError: If wait times out (when configured with timeout)
    :raises Exception: For any other unexpected errors during event processing

    """
    logger = get_logger("core")
    logger.debug("Waiting for key press", extra={"action": "wait_for_char"})

    try:
        while True:
            for e in tcod.event.wait():
                if e.type == "KEYDOWN":
                    logger.debug(
                        "Key pressed",
                        extra={
                            "action": "wait_for_char",
                            "event_type": e.type,
                            "sym": e.sym,
                            "scancode": e.scancode,
                            "is_return": e.sym == tcod.event.KeySym.RETURN,
                        },
                    )
                    if e.sym == tcod.event.KeySym.RETURN:
                        return e
                    return e
    except tcod.event.EventError as e:
        logger.error(
            "TCOD event error while waiting for input",
            extra={
                "action": "wait_for_char",
                "error_type": "EventError",
                "error_message": str(e),
            },
        )
        raise RuntimeError(f"Error waiting for event: {e}") from e
    except Exception as e:
        logger.error(
            "Unexpected error while waiting for input",
            extra={
                "action": "wait_for_char",
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
            exc_info=True,
        )
        raise


def get_noise_generator(dimensions=3):
    """
    Create and return a noise generator with the specified dimensions.

    This function creates a tcod noise generator that can be used for procedural
    generation of terrain, textures, or other game elements.

    :param dimensions: The number of dimensions for the noise generator
    :type dimensions: int
    :return: A configured noise generator object with 32 octaves
    :rtype: tcod.noise.Noise

    """
    logger = get_logger("core")
    start = time_ms()
    logger.debug("Creating noise generator", extra={"dimensions": dimensions})
    result = tcod.noise.Noise(dimensions=dimensions, octaves=32)
    logger.debug(
        "Noise generator created", extra={"duration_ms": time_ms() - start}
    )
    return result


def get_id(name=None):
    """
    Generate or retrieve a unique ID, optionally associated with a name.

    This function either generates a new sequential ID or retrieves a previously created
    ID associated with the given name. If a name is provided and has not been seen
    before, a new ID will be created and associated with that name for future reference.

    :param name: A name to associate with the ID
    :type name: str or None
    :return: A unique identifier, either newly generated or retrieved from the mapping
    :rtype: int

    """
    global ID_SEQ
    global NAME_ID_MAP
    logger = get_logger("core")

    start = time_ms()
    logger.debug(
        "Function entry",
        extra={
            "function": "get_id",
            "function_args": name,
            "function_kwargs": "{}",
        },
    )

    if not name:
        ID_SEQ += 1
        logger.debug(
            "Generated new anonymous ID",
            extra={"action": "get_id", "id_value": ID_SEQ},
        )
        # Log function exit with return value
        duration = time_ms() - start
        logger.debug(
            "Function exit",
            extra={
                "function": "get_id",
                "duration_ms": duration,
                "return_value": str(ID_SEQ),
            },
        )
        return ID_SEQ
    if name in NAME_ID_MAP:
        logger.debug(
            "Retrieved existing named ID",
            extra={
                "action": "get_id",
                "name": name,
                "id_value": NAME_ID_MAP[name],
            },
        )

        # Log function exit with return value
        duration = time_ms() - start
        logger.debug(
            "Function exit",
            extra={
                "function": "get_id",
                "event": "function_exit",
                "duration_ms": duration,
                "return_value": str(NAME_ID_MAP[name]),
            },
        )
        return NAME_ID_MAP[name]
    else:
        new_id = get_id()
        NAME_ID_MAP[name] = new_id
        logger.debug(
            "Created new ID mapping",
            extra={"action": "get_id", "name": name, "id_value": new_id},
        )

        # Log function exit with return value
        duration = time_ms() - start
        logger.debug(
            "Function exit",
            extra={
                "function": "get_id",
                "event": "function_exit",
                "duration_ms": duration,
                "return_value": str(new_id),
            },
        )
        return new_id


ID_SEQ = 100
NAME_ID_MAP = {}


def get_named_ids():
    """
    Get the dictionary mapping names to their associated unique IDs.

    This function returns the current global mapping between names and their
    corresponding unique identifiers.

    :return: A dictionary where keys are names and values are their associated IDs
    :rtype: dict[str, int]

    """
    logger = get_logger("core")
    logger.debug("Retrieving named IDs", extra={"map_size": len(NAME_ID_MAP)})
    return NAME_ID_MAP


@timed(5, "core")
def set_named_ids(new_mapping):
    """
    Set the name-to-ID mapping to a new dictionary.

    This function is typically used for loading saved ID mappings from a persisted
    state, such as when loading a saved game.

    :param new_mapping: A dictionary mapping names to IDs to replace the current mapping
    :type new_mapping: dict[str, int]
    :return: None
    :rtype: None

    """
    global NAME_ID_MAP
    logger = get_logger("core")
    logger.info(
        "ID mapping loaded",
        extra={"action": "set_named_ids", "mapping_size": len(new_mapping)},
    )
    NAME_ID_MAP = new_mapping
