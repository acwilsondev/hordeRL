# Oh No! It's THE HORDE!

Oh No! It's THE HORDE is a classic fantasy roguelike with tower defense elements.

Protect your village by killing all of the hordelings.

## About the Game

Oh No! It's THE HORDE! combines traditional roguelike gameplay with tower defense mechanics. Navigate through procedurally generated levels, strategically position defenses, and fight off waves of hordelings to protect your village.
## Setup and Running the Game

### Steps to Set Up with Poetry

1. Install Python 3.8.1-3.11.x. The game requires Python >=3.8.1,<3.12.
2. Install Poetry by following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).
3. Install the dependencies:

    ```sh
    poetry install
    ```

### Running the Game

To run the game, use one of the following commands:

```sh
poetry run python ./hordeRL.py
```

```sh
poetry run horderl
```

### Command-Line Options

The game supports several command-line options to customize your experience:

```sh
poetry run python ./hordeRL.py [options]
```

Available options (run `poetry run horderl --help` to see the full list):

| Option | Description |
|--------|-------------|
| `--prof` | Profile the game performance (outputs to prof.txt) |
| `--debug` | Allow exceptions to crash the game (useful for development) |
| `--options-path PATH` | Path to the options.yaml file (defaults to horderl/options.yaml and will be created if missing) |
| `--character-name NAME` | Override the player character name |
| `--seed SEED` | Override the world seed |
| `--torch-radius INT` | Override the torch radius |
| `--grass-density FLOAT` | Override the grass density |
| `--autosave/--no-autosave` | Enable or disable autosave |
| `--music/--no-music` | Enable or disable music |
| `-l, --log LEVEL` | Set logging level (INFO, WARNING, CRITICAL, ERROR, DEBUG) |
| `-t, --terminal_log` | Display logs in the terminal instead of writing to .log file |

Examples:

```sh
# Run with debug logging to the terminal
poetry run python ./hordeRL.py --terminal_log --log DEBUG

# Run with profiling enabled
poetry run python ./hordeRL.py --prof
```

## Gameplay

### Controls

- Arrow keys: Move the player
- Space: Attack
- `q`: Quit the game

### Objective

The objective of Oh No! It's THE HORDE! is to defend your village against waves of enemy hordelings. You must:

1. Explore the procedurally generated world
2. Collect resources and items to strengthen your character
3. Set up defensive structures to protect key locations
4. Eliminate all hordelings in each wave
5. Survive as long as possible against increasingly difficult enemies

## Contributing

Interested in contributing to the development of Oh No! It's THE HORDE!? Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to set up the development environment, coding standards, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
