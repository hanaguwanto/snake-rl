# Snake AI Project 🐍

This repository contains multiple iterations of my Snake game development, including the integration of Reinforcement Learning (RL). Each version reflects incremental improvements in game mechanics and AI behavior.

---

## 📂 Version: snake-2026-04-11

This version captures several stages of development in a short time span.

### 🔹 Stage 1: Basic Snake Mechanics

* Snake can move (up, down, left, right)
* Apple consumption is implemented
* No wall collision (snake does not die when hitting boundaries)
* No Reinforcement Learning yet

---

### 🔹 Stage 2: Initial RL Integration

* Reinforcement Learning introduced
* Agent focuses on eating apples
* Snake can die when hitting walls
* Collision between agents is not properly handled (overlapping possible)

---

### 🔹 Stage 3: Collision Fix

* Snake can no longer overlap with other agents
* Death occurs when the head collides with any part of the opponent

---

### 🔹 Stage 4: RL Reward Adjustment

* RL retrained with additional reward:

  * Higher reward when the opponent crashes into the agent’s body
* Training results are still not optimal

---

## 🧠 Notes

This project is part of my learning process in:

* Game development using Python
* Reinforcement Learning implementation
* Multi-agent interaction and environment design

The focus is on experimentation and iterative improvement rather than polished final results.

---

## 🚀 Future Improvements

* Improve RL training stability and performance
* Better reward shaping
* More advanced opponent behavior
* Optimization of game logic

---

## 📌 Disclaimer

This repository is an archive of development progress and may contain unfinished or experimental features.
