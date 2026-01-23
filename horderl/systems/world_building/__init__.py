"""Systems that manage world-building setup and parameter construction."""


def format_world_filename(world_name: str) -> str:
    """
    Format a world name into a filename-friendly string.

    Args:
        world_name: Display name for the world, typically entered by the user.

    Returns:
        A filename-safe string with spaces replaced by hyphens.

    Side effects:
        None.

    Raised errors:
        None.

    Invariants:
        - The returned string preserves the original characters except for
          replacing spaces with hyphens.
    """
    return world_name.replace(" ", "-")
