# 01 Changelog & Code Fixes Report

This document outlines the bugs fixed, spelling errors corrected, and structural type-hinting improvements applied to the Pygame code.

## 1. Major Bug Fixes
* **Fixed Gravity Velocity Cap:** In the original `move` function, the gravity limit check was incomplete. `self.vel_y` inside the `if` statement did not assign any value (`if self.vel_y > 10: self.vel_y`). This was fixed to properly cap the downward velocity: `self.vel_y = 10.0`.
* **Corrected Variable Reference Typos:** In the `__init__` constructor, the class instance variable was written as `self.spped = speed` (with a double 'p'). This broke the movement logic inside the `move` function where it called `self.spped`. It has been renamed correctly to `self.speed`.

## 2. Code Quality & Spelling Improvements
* **Class Renaming:** Fixed the class name typo from `Sholdier` to the standard english spelling `Soldier`.
* **Global Constant Rename:** Fixed the global constant typo `WIN_HIGHT` to `WIN_HEIGHT`.
* **Pythonic Conditional Cleanup:** Cleaned up the jump validation conditional statement from `if self.jump == True and self.in_air == False:` to a cleaner, more Pythonic format: `if self.jump and not self.in_air:`.

## 3. Strict Type Hinting Upgrades
* **Advanced Nested Data Types:** Changed the generic `self.animation_list: list = []` hint to a highly descriptive type hint mapping out the exact data structure: `list[list[pygame.surface.Surface]]`.
* **Tuple Restrictions:** Upgraded color constant mappings from generic `tuple` to exact RGB sequence specifications: `tuple[int, int, int]`.
* **Constructor Parameters:** Added missing type-checking protections for dynamic parameters `char_type: str` and `speed: int` inside the initialization framework.
* **Functional Return Types:** Explicitly defined non-returning routines with the `-> None` annotation format across functions like `draw_bg()`, `move()`, `update_animation()`, `draw()`, and `update_action()`.

---

# 02 Changelog & Code Fixes Report

This document outlines the enhancements, new features, and structural improvements applied from 01c.py to 02c.py.

## 1. New Imports & Type Hints
* **Added typing module:** Imported `from typing import Any` to support dynamic parameter handling in the `Bullet` class constructor.

## 2. New Global Variables & Enhanced Parameters
* **Added shoot variable:** Added `shoot: bool = False` global variable to track shooting input state.
* **Added ammo parameter:** Updated `Soldier` class initialization to accept `ammo: int` parameter, enabling ammo tracking.

## 3. Enhanced Soldier Class with New Instance Variables
* **Health System:** Added `health: int = 100` and `max_health: int = self.health` for health tracking.
* **Ammo System:** Added `ammo: int = ammo` and `start_ammo: int = ammo` for ammunition tracking.
* **Shooting Cooldown:** Added `shoot_cooldown: int = 0` to implement firing rate limiting.
* **Enhanced update_time:** Changed from `pygame.time.get_ticks()` to `float(pygame.time.get_ticks())` for proper type consistency.

## 4. New Methods in Soldier Class
* **`update()` method:** Added animation update cycle and cooldown management.
* **`check_alive()` method:** Implemented death detection; sets `alives = False`, freezes movement (`speed = 0`), and switches to Death animation when health reaches 0.
* **`shoot()` method:** Implemented shooting mechanism with cooldown checking, ammo consumption, and bullet spawning at proper offset.

## 5. New Bullet Class Implementation
* **Complete bullet system:** Implemented `Bullet` sprite class with:
  - Directional velocity (`direction: int`)
  - Automatic screen boundary culling (removes bullets when off-screen)
  - Collision detection with both player and enemy
  - Damage application (5 damage to player, 25 damage to enemy)

## 6. Image Loading & Animation Enhancements
* **Added `.convert_alpha()`:** Applied `.convert_alpha()` to all loaded images for better rendering performance and transparency handling.
* **Fixed scale bug:** Corrected the animation scaling from `img.get_width() * scale` for height to properly use `img.get_height() * scale`, fixing distorted animations.
* **Added Death animation:** Extended `animation_type` list to include "Death" animation for character death sequences.
* **Updated animation handling:** Enhanced `update_animation()` to handle Death state where animation loops at final frame instead of resetting.

## 7. Enhanced Input & Game Loop
* **Added shooting input:** Integrated `shoot` key (`pygame.K_SPACE`) into the event handling system with KEYDOWN/KEYUP detection.
* **Integrated bullet group management:** Added `bullet_group.update()` and `bullet_group.draw(screen)` to game loop.
* **Enemy sprite activation:** Enemy sprites now receive `update()` calls and participate in collision detection.
* **Dynamic action handling:** Player actions now include `update_action(3)` for Death state.

## 8. Type Hint Improvements
* **`Any` type support:** Added `*groups: Any` parameter to Bullet constructor for flexible sprite group assignment.
* **Float type consistency:** Applied `float()` conversion to time-related values for strict type consistency.
* **Window parameter typing:** Added `window: pygame.surface.Surface` type hint to `draw()` method.

## 9. Enemy Sprite Implementation
* **Full enemy support:** Enemy sprite now instantiated with ammo parameter (`ammo: 20`) and fully integrated into game loop with health tracking and collision detection.
* **Bidirectional combat:** Both player and enemy can be damaged by bullets and display health values in console.

---

# 03 Changelog & Code Fixes Report

This document outlines the grenade, explosion, multi-enemy, and gameplay integration enhancements added to the Pygame project.

## 1. Grenade System
* **Added grenade state tracking:** Added `grenade` and `grenade_thrown` boolean variables to manage grenade input and prevent repeated throws while the key is held.
* **Added grenade inventory:** Extended `Soldier` with a `grenade` parameter and instance variable so each character can track available grenades.
* **Implemented `Grenade` sprite:** Added a grenade class with directional movement, gravity, floor bouncing, wall collision, decreasing horizontal speed, and a countdown timer.
* **Added grenade input:** Integrated the `Q` key with `KEYDOWN` and `KEYUP` handling to throw grenades and reset the throw state.

## 2. Explosion Effects and Area Damage
* **Added explosion image loading:** Loaded five explosion frames from `img/explosion/exp1.png` through `exp5.png` and scaled them according to the requested size.
* **Implemented `Explosion` sprite:** Added frame-based explosion animation that removes itself after the final frame.
* **Added area damage:** When a grenade timer expires, an explosion is created and nearby players or enemies lose 50 health.

## 3. Sprite Group and Game Loop Integration
* **Added sprite groups:** Created `grenade_group` and `explosion_group` alongside the existing enemy and bullet groups.
* **Integrated updates and drawing:** The main loop now updates and draws grenades and explosions every frame.
* **Added grenade and explosion assets:** Loaded `grenade.png` and used the explosion asset sequence with alpha transparency for rendering.

## 4. Multiple Enemy Support
* **Added a second enemy:** Instantiated `enemy2` at a separate position and added it to `enemy_group`.
* **Expanded enemy processing:** The game loop iterates over all enemies so each enemy is updated and drawn consistently.

## 5. Gameplay and Code Improvements
* **Added tile-size configuration:** Introduced `TILE_SIZE = 40` and used it to define the grenade damage radius.
* **Added grenade-aware constructors:** Updated player and enemy creation to provide grenade ammunition values (`5` for the player and `0` for enemies).
* **Improved sprite initialization:** Used `super().__init__(*groups)` in the new sprite classes to support optional Pygame sprite-group assignment.

---

# 04 Changelog & Code Fixes Report

This document outlines the item pickup system, player HUD improvements, and cross-module dependency fixes added to the Pygame project.

## 1. Item Pickup System
* **Added `ItemBox` sprite:** Implemented a reusable item-box class for collectible health, ammo, and grenade supplies.
* **Added pickup collision detection:** Item boxes now detect collision with the player and remove themselves after collection.
* **Added health pickup:** Health boxes restore 25 health points without allowing the player's health to exceed `max_health`.
* **Added ammo pickup:** Ammo boxes add 15 bullets to the player's ammunition count.
* **Added grenade pickup:** Grenade boxes add 3 grenades to the player's inventory.

## 2. Health Bar and Player HUD
* **Added `HealthBar` class:** Created a reusable health-bar component that displays the current health ratio using background, damage, and remaining-health colors.
* **Added player statistics display:** The game now displays the player's health, ammo, and grenade count on screen.
* **Added grenade inventory icons:** Remaining grenades are represented visually with grenade icons in the HUD.

## 3. Item Assets and Sprite Group Integration
* **Added item images:** Loaded health-box, ammo-box, and grenade-box images from the icon asset folder.
* **Added item image mapping:** Stored item images in an `item_boxes` dictionary keyed by item type.
* **Added item-box group:** Created `item_boxes_group` and integrated item updates and drawing into the main game loop.
* **Added temporary level pickups:** Placed health, ammo, and grenade boxes at separate positions in the level for testing.

## 4. Cross-Module Dependency Fixes
* **Removed undefined global dependencies:** Bullet and grenade classes no longer rely on objects created in `main.py`.
* **Updated bullet constructor:** Bullet images are passed explicitly when bullets are created.
* **Updated bullet updates:** The player and complete enemy group are passed to bullet updates, allowing collision detection with multiple enemies.
* **Updated grenade constructor:** Grenade images are passed explicitly when grenades are created.
* **Updated grenade updates:** The player, enemy group, and explosion group are passed to grenade updates for damage and explosion handling.

## 5. Validation and Environment
* **Resolved missing dependency:** Installed `pygame-ce` in the project's virtual environment as declared in `pyproject.toml`.
* **Verified module compilation:** Confirmed that `main.py`, `bullet.py`, `grenade.py`, and `soldiers.py` compile successfully after the API changes.

---

# 05 Changelog & Code Fixes Report

This document outlines the enemy AI, vision-based combat, patrol behavior, and related gameplay fixes added to the Pygame project.

## 1. Enemy AI System
* **Added AI behavior:** Extended the `Soldier` class with an `ai()` method for controlling enemy movement and combat.
* **Added enemy patrol movement:** Enemies automatically move in their current direction and reverse direction after traveling one tile-size interval.
* **Added random idle behavior:** Enemies occasionally stop and idle for a short period, creating less predictable movement.
* **Added AI state tracking:** Introduced movement, vision, idle, and idle-counter variables to manage enemy behavior across frames.

## 2. Enemy Vision and Combat
* **Added vision rectangle:** Each enemy now has a forward-facing rectangular detection area for locating the player.
* **Added player detection:** Enemies stop moving and switch to the Idle animation when the player enters their vision area.
* **Added enemy shooting:** Detected players are attacked using the existing bullet system and shooting cooldown.
* **Fixed AI shooting error:** Corrected the invalid `player.bullet_group` reference by using the `bullet_group` passed directly to `ai()`.

## 3. Soldier Rendering Improvements
* **Added health indicators:** Soldiers now display a red health bar above their sprite while being drawn.
* **Updated character scaling:** Player and enemy instances use a scale of `1.65` for larger on-screen character sprites.
* **Added different enemy speeds:** The two enemies use separate movement speeds, making their patrol behavior distinct.

## 4. Main Loop Integration
* **Integrated enemy AI updates:** The main game loop now calls `enemy.ai(screen, player, bullet_img, bullet_group)` for every enemy.
* **Preserved multi-enemy support:** All enemies continue to be updated, drawn, and included in bullet collision detection through `enemy_group`.
* **Kept debugging output disabled:** The vision rectangle remains available for debugging but is commented out during normal gameplay.

---

# 06 Changelog & Code Fixes Report

This document outlines the level loading, world collision, dynamic object placement, and multi-target combat improvements added after the 05 revision. It also records the planned MVC refactor for a future project phase.

## 1. Data-Driven Level Loading
* **Added CSV level support:** Level layouts are now loaded from `level1_data.csv`, with the selected level controlled by the `level` variable.
* **Created a default world grid:** The game initializes a `ROWS` by `COLS` tile grid with empty values before importing the CSV data.
* **Added tile validation:** CSV values are converted to integers and only values within the configured world dimensions are written to the level grid.
* **Added missing-player validation:** `World.process_data()` raises a `ValueError` when the level does not contain a player start tile.

## 2. World and Tile Improvements
* **Added the `World` class:** Level processing and world rendering are grouped into reusable `process_data()` and `draw()` methods.
* **Added tile image loading:** All configured tile images are loaded, scaled to `TILE_SIZE`, and stored in `img_list`.
* **Added solid tile collision:** Soldiers now check movement against obstacle rectangles from the loaded level instead of relying on a fixed floor position.
* **Added grenade world collision:** Grenades reverse direction when hitting a wall and stop vertical movement when landing on level geometry.
* **Added bullet wall collision:** Bullets are removed when they hit an obstacle tile, preventing them from passing through level structures.

## 3. Dynamic Level Objects
* **Added tile-based entity placement:** Player, enemies, item boxes, decorations, water, and exits are created from their corresponding tile IDs in the CSV level.
* **Added world sprite groups:** `water_group`, `decorator_group`, and `exit_group` are updated and drawn with the rest of the game objects.
* **Improved item-box construction:** Item boxes now use the shared item image mapping while being positioned directly from level data.

## 4. Multi-Enemy Combat Fix
* **Fixed bullet targeting:** Bullet collision now checks every living enemy in `enemy_group`, rather than checking only one global enemy instance.
* **Added single-hit bullet behavior:** A bullet is removed after damaging its first enemy, preventing one bullet from damaging multiple targets in the same frame.
* **Preserved player combat:** Enemy bullets can still damage the player, while player bullets can damage any enemy loaded from the level.

## 5. Planned MVC Refactor
* **Planned model layer:** Game state such as the player, enemies, level data, inventory, health, and collision rules will be moved into model classes.
* **Planned view layer:** Rendering, HUD elements, animations, and sprite drawing will be separated from gameplay state and rules.
* **Planned controller layer:** Input handling, enemy AI, game-loop coordination, level transitions, and model updates will be handled by controller classes.
* **Refactor goal:** The MVC structure will reduce the current dependency on global variables and make levels, gameplay systems, and future features easier to test and maintain.