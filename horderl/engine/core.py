import logging
from time import perf_counter_ns

import tcod.event
import tcod.noise


def get_key_event():
    """
    Handle tcod key events and return keyboard input.

    This function processes all pending events and returns the first KEYDOWN event
    encountered. If no KEYDOWN event is found, returns None.

    :return: The key press event if one occurred
    :rtype: tcod.event.KeyDown or None

    """
    for event in tcod.event.get():
        if event.type == "KEYDOWN":
            return event


def wait_for_char():
    """
    Wait for a character key press and return the corresponding event.

    This function blocks until a key is pressed. It will immediately return when any key
    is pressed, but specifically checks for the Enter/Return key.

    :return: The keyboard event that was triggered
    :rtype: tcod.event.KeyDown

    """
    while True:
        for e in tcod.event.wait():
            if e.type == "KEYDOWN":
                if e.sym == tcod.event.KeySym.RETURN:
                    return e
                return e


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
    return tcod.noise.Noise(dimensions=dimensions, octaves=32)


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

    if not name:
        ID_SEQ += 1
        return ID_SEQ

    if name in NAME_ID_MAP:
        return NAME_ID_MAP[name]
    else:
        NAME_ID_MAP[name] = get_id()
        return get_id(name)


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
    return NAME_ID_MAP


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
    logging.info("Core::set_named_ids id mapping loaded")
    NAME_ID_MAP = new_mapping


def time_ms():
    """
    Get the current time in milliseconds.

    This function uses a high-precision performance counter and converts nanoseconds to
    milliseconds. It's useful for timing operations and calculating elapsed time.

    :return: Current time in milliseconds
    :rtype: int

    """
    return int(perf_counter_ns() / 1000000)


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
            logger = logging.getLogger(module)

            t0 = time_ms()
            result = func(*args, **kwargs)
            t1 = time_ms()
            if t1 - t0 > ms:
                logger.warning(f"call to {func} took {t1-t0}ms (>{ms}ms)")
            return result

        return inner

    return outer


def log_debug(module):
    """
    Decorator to add debug logging to a function.

    This decorator logs the function call with its arguments, execution time, and return
    value. It also catches and logs any exceptions that occur during execution. The
    decorator preserves the original function's signature and return value.

    :param module: The module name used for logging
    :type module: str
    :return: A decorator function that wraps the target function with debug logging
    :rtype: callable

    """

    def outer(fn):
        def decorated(*args, **kwargs):
            logger = logging.getLogger(module)

            try:
                start = time_ms()
                logger.debug(f" {fn.__name__} => {args} - {kwargs}")
                result = fn(*args, **kwargs)
                logger.debug(
                    f" {fn.__name__} {time_ms() - start}ms <= {result}"
                )
                return result
            except Exception as ex:
                logger.debug("Exception {0}".format(ex))
                raise ex

        return decorated

    return outer
