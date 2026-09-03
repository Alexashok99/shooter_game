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