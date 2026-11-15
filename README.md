# ✨ Pixel & Lexicon ✨

A whimsical desktop puzzle sanctuary featuring a 15-puzzle and a 4x4 word builder. Crafted with a Python Tkinter GUI and a C++ backend, it showcases algorithmic integrations including A* Search, Merge Sort solvability verification, and Trie-based DFS pruning.

## 🧩 Features

* **Pixel Mode (15-Puzzle):** A sliding tile puzzle backed by 64-bit bitmask boards that allows users to upload and slice custom images. 
  * **Math Verification:** Mathematically verifies if a shuffled board is solvable using C++ Merge Sort inversion counting.
  * **Auto-Solver:** Instantly solves the puzzle using the A* Search algorithm with a Manhattan Distance heuristic.
* **Lexicon Mode (Word Builder):** A 4x4 word-building grid where valid dictionary words are constructed.
  * **Dual-Layer Validation:** Checks words against a local cache first, then falls back to a public dictionary REST API.
  * **DFS Trie Auto-Solver:** A C++ engine leverages a Trie data structure combined with Depth-First Search (DFS) for aggressive prefix pruning to instantly find all possible words on the board.

## 💻 Tech Stack
* **Frontend:** Python (Tkinter GUI, Pillow for image processing)
* **Backend Engines:** C++ (Compiled to a binary executable for high-performance algorithm execution)
* **Logic & APIs:** Python (`urllib` for dictionary API requests, `heapq` for A* Search)

## 🚀 How to Run
1. Ensure you have Python installed on your system.
2. Download or clone this repository.
3. Run the main application file from your terminal:
   ```bash
   python gui_app.py
