# Shooter Game

A lightweight 2D shooter-game prototype built with Python and [pygame-ce](https://pyga.me/). The current prototype displays a player and an enemy, supports player movement and jumping, and includes animated sprite frames.

## Features

- 800 x 500 game window
- 60 FPS game loop
- Player idle, running, and jumping animations
- Enemy sprite display
- Gravity and floor collision
- Keyboard movement and jump controls
- Separate folders for sprites, UI images, level data, and audio

## Requirements

- Python 3.13 or a compatible Python 3 version
- `pygame-ce`

## Setup

### 1. Create the virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install the project dependency

```powershell
python -m pip install pygame-ce
```

The dependency is also declared in `pyproject.toml`.

## Run the Game

From the project directory, with the virtual environment activated:

```powershell
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| `A` | Move left |
| `D` | Move right |
| `W` | Jump |
| `Esc` | Quit the game |

You can also close the game window to exit.

## Project Structure

```text
shooter_game/
├── audio/                 # Sound effects and music
├── img/
│   ├── enemy/             # Enemy animation frames
│   ├── player/            # Player animation frames
│   ├── background/        # Background artwork
│   ├── tile/              # Level tiles
│   └── icons/             # UI icons and buttons
├── level1_data.csv        # Level data
├── level2_data.csv        # Level data
├── level3_data.csv        # Level data
├── main.py                # Game entry point
├── pyproject.toml         # Project metadata and dependencies
└── README.md
```

## Animation Assets

The game loads animation frames from these directories for both `player` and `enemy` characters:

```text
img/<character>/Idle/<frame>.png
img/<character>/Run/<frame>.png
img/<character>/Jump/<frame>.png
```

Frame files should use numeric names starting at `0`, such as `0.png`, `1.png`, and `2.png`.

## Development Status

This is an early gameplay prototype. Shooting, enemy behavior, level loading, menus, and audio playback are available as project assets or planned expansion areas but are not yet connected to the main game loop.

## License

No license has been specified yet.
