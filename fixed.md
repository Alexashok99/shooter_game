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