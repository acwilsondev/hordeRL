import tracery

"""
Procedural town name generator for the game.

This module uses the tracery library to generate random town names based on
predefined linguistic patterns and combinations of syllables. These names
are used for procedurally generated settlements and locations in the game world.
"""

rules = {
    "origin": "#first##second#",
    "first": [
        "Spur",
        "Churl",
        "Whim",
        "Gale",
        "River",
        "Ton",
        "Gil",
        "Hel",
        "Bur",
        "Turl",
        "Fon",
        "Fil",
        "Til",
        "Shim",
        "To",
        "Cod",
        "Lin",
    ],
    "second": ["burg", "ham", "ton", "hill", "shim", "cod", "ling", "mont", "bog"],
}
"""
Dictionary of tracery grammar rules for town name generation.

Contains patterns and word parts used to construct town names:
- 'origin': The pattern combining first and second parts
- 'first': Prefixes or first parts of town names
- 'second': Suffixes or second parts of town names
"""


def get_file_name():
    """
    Generate a file-system friendly town name.
    
    Returns:
        str: A procedurally generated town name with spaces replaced by hyphens,
             suitable for use in filenames.
    """
    name = get_name()
    return name.replace(" ", "-")


def get_name():
    """
    Generate a random town name using tracery grammar rules.
    
    Creates a procedural town name by combining prefixes and suffixes
    according to the patterns defined in the rules dictionary.
    
    Returns:
        str: A procedurally generated town name.
    """
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")
