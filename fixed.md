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