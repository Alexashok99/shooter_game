# Shooter Game

A side-scrolling action shooter built in Python with [pygame-ce](https://pyga.me/). The project combines a menu system, level-based progression, AI enemies, projectile combat, pickups, parallax backgrounds, and a full game loop in a single playable prototype.

## Overview

This game is a modern 2D platform-shooter prototype inspired by classic side-scrolling action games. Players move through tiled levels, fight enemies, collect supplies, and reach exits to progress to the next stage. The project is structured around CSV-based level loading, sprite animation, world collision, and a clean start/restart flow.

The current codebase in [main.py](main.py) includes a complete playable loop with:

- menu start and exit screens
- level reset and retry flow
- multiple CSV-defined levels
- camera scrolling and parallax background
- enemy AI and combat behavior
- bullets, grenades, and explosions
- pickups for health, ammo, and grenades
- HUD and health tracking

## Features

- 800 x 640 game window
- 60 FPS gameplay loop
- Start menu with clickable Start and Exit buttons
- Retry screen after player death
- Multi-level progression using `level1_data.csv`, `level2_data.csv`, and `level3_data.csv`
- Side-scrolling camera system with world boundary checks
- Parallax background layers for depth
- Player movement, jumping, shooting, and grenade actions
- AI enemies with patrol and vision-based combat
- Bullet collision, wall collision, and life management
- Grenade throwing and area-damage explosion effects
- Health, ammo, and grenade pickups
- HUD with health bar and inventory display
- Background music and sound effects

## Requirements

- Python 3.10+ (project is compatible with modern Python versions)
- `pygame-ce`

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```powershell
python -m pip install pygame-ce
```

The dependency is also declared in `pyproject.toml`.

## Run the Game

From the project root:

```powershell
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| `A` | Move left |
| `D` | Move right |
| `W` | Jump |
| `Space` | Shoot |
| `Q` | Throw grenade |
| `Esc` | Quit the game |

Mouse controls are also used in the menu:

- click Start to begin
- click Exit to close the game
- click Restart after death to reload the current level

## Gameplay Flow

1. The player starts on the menu screen.
2. Clicking Start begins the level.
3. The player moves through the world, avoids enemy fire, and defeats enemies.
4. Collecting item boxes restores health, ammo, or grenades.
5. Reaching the exit triggers the next level load.
6. If the player dies, the restart button reloads the level.

## Project Structure

```text
shooter_game/
├── audio/                  # Background music and sound effects
├── img/                    # Player, enemy, UI, tile, and background assets
│   ├── background/
│   ├── enemy/
│   ├── explosion/
│   ├── icons/
│   ├── player/
│   └── tile/
├── class_based/            # Supporting class-based game modules
├── button.py               # Reusable UI button class
├── level1_data.csv         # Level 1 map data
├── level2_data.csv         # Level 2 map data
├── level3_data.csv         # Level 3 map data
├── main.py                 # Main game entry point and gameplay loop
├── pyproject.toml          # Package metadata and dependency config
├── fixed.md                # Changelog and code-fix notes
├── README.md               # Project documentation
└── shooter_game.egg-info/  # Packaging metadata
```

## Level System

Levels are defined in CSV files and converted into world data during runtime. Each level includes:

- collision tiles
- platform layouts
- player start positions
- enemy positions
- item boxes
- water and decorative objects
- exit tile

The world class processes the tile map and rebuilds the level for each new stage.

## Combat System

The game includes multiple combat mechanics:

- player bullets with damage and wall checks
- enemy shooting based on vision detection
- grenades with gravity and bouncing physics
- explosion damage in a radius around the blast
- health bars for player and enemy sprites

## HUD and User Interface

The HUD displays:

- current health
- remaining ammo
- grenade count
- grenade icons
- health bar overlay on characters

The UI is rendered directly on the screen while the world continues to scroll behind it.

## Audio Assets

The project includes:

- background music
- jump sound effect
- shot sound effect
- grenade explosion sound

These are loaded at runtime from the `audio/` directory.

## Development Notes

This project is a complete gameplay prototype rather than a simple placeholder. It includes actual level progression, menu states, enemy AI, combat systems, item collection, collision handling, and audiovisual polish.

The final architecture reflects a mix of procedural gameplay logic and modular game objects, making it a strong foundation for future refactoring into cleaner model-view-controller patterns.

## Credits

- [pygame-ce](https://pyga.me/) — game development library
- [Grenades 16x16](https://mtk.itch.io/grenades-16x16) — MTK
- [Pixel Platformer](https://erayzesen.itch.io/pixel-platformer) — Eray Zesen
- [Team Wars: Platformer Battle](https://secrethideout.itch.io/team-wars-platformer-battle) — Secret Hideout
- [Bullet Whizzing By](https://soundbible.com/1875-Bullet-Whizzing-By.html) — SoundBible
- [Fantasy/Wonder Music](https://soundimage.org/fantasywonder/) — Soundimage
- [YouTube](https://youtube.com/@codingwithruss?si=t2i5H6jP7oqFncE5) — Code Logic (Coding With Russ)

## License

This project is licensed under the MIT License.
