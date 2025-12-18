# ❄️ Frostbound Run

Frostbound Run is a 2D platformer game built using **Python** and **Pygame**, where you play as a sorcerer trapped in a frozen world. Navigate icy platforms, collect gems, defeat roaming enemies using fireball magic, and reach the exit gate to progress through handcrafted levels.

---

## 🎮 Gameplay Overview

- Play as a **sorcerer** in a frostbound realm
- Jump across **ground and floating platforms**
- Fight **roaming enemies** using **fireball spells**
- Enemies roam blindly and do not track the player
- Collect **gems** to increase score
- Reach the **exit gate** to complete a level
- Lose lives when colliding with living enemies
- Win the game after completing all levels

---

## ✨ Features

- Smooth 2D platformer physics
- Sprite-based animations (idle, walk, jump)
- Fireball projectile combat system
- Enemy AI with patrol behavior
- Enemy death animation and state handling
- Multiple levels loaded from JSON files
- Camera scrolling system
- Lives, score, and level tracking
- Level complete and win screens
- Cross-platform deployment (macOS & Windows)

---

## 🕹 Controls

| Key | Action |
|---|---|
| `A` | Move Left |
| `D` | Move Right |
| `SPACE` | Jump |
| `F` | Cast Fireball |
| `R` | Restart (after Game Over / Win) |

---

## 🧱 Project Structure

Frostbound-run/
│
├── main.py
├── utils.py
├── player.py
├── enemy.py
├── fireball.py
├── level_loader.py
├── tiles.py
│
├── assets/
│ ├── images/
│ ├── player/
│ ├── enemy/
│ └── tiles/
│
├── levels/
│ ├── level1.json
│ ├── level2.json
│ ├── level3.json
│ ├── level4.json
│ └── level5.json
│
└── README.md

---

## 🧠 Technical Highlights

- Object-oriented design for Player, Enemy, and Projectiles
- Enemy state machine (`alive → dying → dead`)
- Collision handling from all sides (top, bottom, left, right)
- Level data driven by JSON files
- Asset loading compatible with PyInstaller using a shared `resource_path()` utility
- Clean separation of game logic, rendering, and data

---

## 🛠 Installation (Run from Source)

### Prerequisites
- Python 3.10+
- Pygame

### Install dependencies
```bash
pip install pygame

## Run the game
```bash
Run the game
