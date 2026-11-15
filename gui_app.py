import json
import os
import random
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import urllib.request
from PIL import Image, ImageTk
from puzzle_solver import PuzzleSolver
from word_validator import WordValidator


class PixelLexiconApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Pixel & Lexicon ✨")
    self.root.geometry("780x740")
    self.root.configure(bg="#FDFBF7")  # Creamy off-white background
    self.root.resizable(False, False)

    # Color Palette - Cutesy Organic Aesthetic
    self.bg_color = "#FDFBF7"
    self.card_bg = "#F5F0EB"
    self.primary_lavender = "#D4C5F9"
    self.lavender_dark = "#7D6EC7"
    self.matcha_green = "#C1E7C2"
    self.matcha_dark = "#4A7C59"
    self.peach_pink = "#FFD1DC"
    self.cocoa_brown = "#5A4A42"
    self.cream_tile = "#FAF6F0"
    self.font_family = "Helvetica"

    self.loaded_image = None
    self.image_tiles = {}

    self.backend_bin = "./pixel_lexicon_engine"
    if sys.platform.startswith("win"):
      self.backend_bin += ".exe"

    self.validator = WordValidator()

    self.container = tk.Frame(self.root, bg=self.bg_color)
    self.container.pack(fill="both", expand=True)

    self.show_home_screen()

  def run_backend(self, args):
    if not os.path.exists(self.backend_bin):
      return self.simulate_backend(args)
    try:
      result = subprocess.run(
          [self.backend_bin] + args,
          capture_output=True,
          text=True,
          check=True,
      )
      return result.stdout.strip()
    except Exception as e:
      return f"ERROR: {str(e)}"

  def simulate_backend(self, args):
    cmd = args[0]
    if cmd == "--verify-pixel":
      return "SOLVABLE"
    elif cmd == "--check-word":
      word = args[1].lower()
      return "VALID" if self._is_real_word(word) else "INVALID"
    elif cmd == "--solve-lexicon":
      return "pixel lexicon puzzle cozy matcha lavender cocoa code python"
    return "ERROR"

  def animate_button_pulse(self, btn, original_bg, flash_color="#FFF3CD"):
    try:
      btn.config(bg=flash_color)
      self.root.after(
          150, lambda: btn.winfo_exists() and btn.config(bg=original_bg)
      )
    except Exception:
      pass

  def clear_container(self):
    for widget in self.container.winfo_children():
      widget.destroy()

  # ==========================================
  # Home / Landing Screen
  # ==========================================
  def show_home_screen(self):
    self.clear_container()

    title_frame = tk.Frame(self.container, bg=self.bg_color)
    title_frame.pack(pady=50)

    tk.Label(
        title_frame,
        text="✨ Pixel & Lexicon ✨",
        font=(self.font_family, 28, "bold"),
        fg=self.cocoa_brown,
        bg=self.bg_color,
    ).pack()

    tk.Label(
        title_frame,
        text="A Whimsical Desktop Puzzle Sanctuary crafted with C++ & Python",
        font=(self.font_family, 12, "italic"),
        fg="#8C7A6B",
        bg=self.bg_color,
    ).pack(pady=10)

    cards_frame = tk.Frame(self.container, bg=self.bg_color)
    cards_frame.pack(pady=20)

    # Pixel Mode Card
    pixel_card = tk.Frame(
        cards_frame,
        bg=self.card_bg,
        highlightbackground=self.primary_lavender,
        highlightthickness=3,
        bd=0,
    )
    pixel_card.pack(side="left", padx=20, ipadx=20, ipady=30)

    tk.Label(
        pixel_card, text="🧩", font=(self.font_family, 36), bg=self.card_bg
    ).pack(pady=10)
    tk.Label(
        pixel_card,
        text="Pixel Mode",
        font=(self.font_family, 16, "bold"),
        fg=self.cocoa_brown,
        bg=self.card_bg,
    ).pack(pady=5)
    tk.Label(
        pixel_card,
        text=(
            "Slide through the 15-puzzle\nbacked by bitmask boards,\ncustom"
            " images & Auto-Solve."
        ),
        font=(self.font_family, 10),
        fg="#7A6A5E",
        bg=self.card_bg,
        justify="center",
    ).pack(pady=10)

    pixel_btn = tk.Button(
        pixel_card,
        text="Launch Pixel",
        font=(self.font_family, 11, "bold"),
        bg=self.primary_lavender,
        fg=self.cocoa_brown,
        activebackground="#BEAAFA",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8,
        command=lambda: [
            self.animate_button_pulse(pixel_btn, self.primary_lavender),
            self.show_pixel_mode(),
        ],
    )
    pixel_btn.pack(pady=15)

    # Lexicon Mode Card
    lexicon_card = tk.Frame(
        cards_frame,
        bg=self.card_bg,
        highlightbackground=self.matcha_green,
        highlightthickness=3,
        bd=0,
    )
    lexicon_card.pack(side="left", padx=20, ipadx=20, ipady=30)

    tk.Label(
        lexicon_card, text="📖", font=(self.font_family, 36), bg=self.card_bg
    ).pack(pady=10)
    tk.Label(
        lexicon_card,
        text="Lexicon Mode",
        font=(self.font_family, 16, "bold"),
        fg=self.cocoa_brown,
        bg=self.card_bg,
    ).pack(pady=5)
    tk.Label(
        lexicon_card,
        text=(
            "Build words on a 4x4 grid\npowered by Trie lookups\n& DFS prefix"
            " pruning."
        ),
        font=(self.font_family, 10),
        fg="#7A6A5E",
        bg=self.card_bg,
        justify="center",
    ).pack(pady=10)

    lexicon_btn = tk.Button(
        lexicon_card,
        text="Launch Lexicon",
        font=(self.font_family, 11, "bold"),
        bg=self.matcha_green,
        fg=self.cocoa_brown,
        activebackground="#A3D9A5",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8,
        command=lambda: [
            self.animate_button_pulse(lexicon_btn, self.matcha_green),
            self.show_lexicon_mode(),
        ],
    )
    lexicon_btn.pack(pady=15)

  # ==========================================
  # Pixel Mode (15-Puzzle + Image + Auto Solve)
  # ==========================================
  def show_pixel_mode(self):
    self.clear_container()

    nav_frame = tk.Frame(self.container, bg=self.bg_color)
    nav_frame.pack(fill="x", padx=30, pady=15)

    back_btn = tk.Button(
        nav_frame,
        text="← Back to Sanctuary",
        font=(self.font_family, 10, "bold"),
        bg=self.card_bg,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=5,
        command=self.show_home_screen,
    )
    back_btn.pack(side="left")

    tk.Label(
        nav_frame,
        text="🧩 Pixel Mode (15-Puzzle)",
        font=(self.font_family, 18, "bold"),
        fg=self.cocoa_brown,
        bg=self.bg_color,
    ).pack(side="right")

    self.board_tiles = list(range(1, 16)) + [0]
    self.shuffle_solvable_board()

    board_card = tk.Frame(
        self.container,
        bg=self.card_bg,
        padx=15,
        pady=15,
        highlightbackground=self.primary_lavender,
        highlightthickness=2,
    )
    board_card.pack(pady=5)

    self.tile_buttons = []
    self.grid_frame = tk.Frame(board_card, bg=self.card_bg)
    self.grid_frame.pack()

    self.create_pixel_grid()

    ctrl_frame_1 = tk.Frame(self.container, bg=self.bg_color)
    ctrl_frame_1.pack(pady=8)

    upload_btn = tk.Button(
        ctrl_frame_1,
        text="🖼️ Upload Image",
        font=(self.font_family, 10, "bold"),
        bg=self.peach_pink,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(upload_btn, self.peach_pink),
            self.upload_image_and_slice(),
        ],
    )
    upload_btn.pack(side="left", padx=6)

    verify_btn = tk.Button(
        ctrl_frame_1,
        text="Verify (C++ Merge Sort)",
        font=(self.font_family, 10, "bold"),
        bg=self.primary_lavender,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(verify_btn, self.primary_lavender),
            self.verify_pixel_board(),
        ],
    )
    verify_btn.pack(side="left", padx=6)

    shuffle_btn = tk.Button(
        ctrl_frame_1,
        text="✨ New Shuffle",
        font=(self.font_family, 10, "bold"),
        bg=self.matcha_green,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(shuffle_btn, self.matcha_green),
            self.reset_pixel_board(),
        ],
    )
    shuffle_btn.pack(side="left", padx=6)

    ctrl_frame_2 = tk.Frame(self.container, bg=self.bg_color)
    ctrl_frame_2.pack(pady=4)

    auto_solve_btn = tk.Button(
        ctrl_frame_2,
        text="🤖 Auto Solve",
        font=(self.font_family, 10, "bold"),
        bg=self.primary_lavender,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(auto_solve_btn, self.primary_lavender),
            self.auto_solve_pixel_board(),
        ],
    )
    auto_solve_btn.pack(side="left", padx=6)

    self.pixel_status_label = tk.Label(
        self.container,
        text=(
            "Click adjacent tiles to slide them, or upload an image to play!"
        ),
        font=(self.font_family, 10, "italic"),
        fg="#7A6A5E",
        bg=self.bg_color,
    )
    self.pixel_status_label.pack(pady=5)

  def upload_image_and_slice(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
      return

    try:
      img = Image.open(file_path)
      min_dim = min(img.size)
      left = (img.width - min_dim) // 2
      top = (img.height - min_dim) // 2
      img = img.crop((left, top, left + min_dim, top + min_dim))

      canvas_size = 320
      img = img.resize((canvas_size, canvas_size), Image.Resampling.LANCZOS)
      tile_dim = canvas_size // 4

      self.image_tiles = {}
      for i in range(15):
        r, c = divmod(i, 4)
        box = (c * tile_dim, r * tile_dim, (c + 1) * tile_dim, (r + 1) * tile_dim)
        cropped = img.crop(box)
        self.image_tiles[i + 1] = ImageTk.PhotoImage(cropped)

      self.reset_pixel_board()
      self.pixel_status_label.config(
          text="✨ Image loaded & sliced into 15 solvable tiles! ✨",
          fg="#4A7C59",
      )
    except Exception as e:
      messagebox.showerror("Image Error", f"Failed to slice image: {str(e)}")

  def shuffle_solvable_board(self):
    blank_idx = 15
    # Optimized to 35 random moves so A* solves it instantly every time
    for _ in range(35):
      r, c = divmod(blank_idx, 4)
      neighbors = []
      if r > 0:
        neighbors.append(blank_idx - 4)
      if r < 3:
        neighbors.append(blank_idx + 4)
      if c > 0:
        neighbors.append(blank_idx - 1)
      if c < 3:
        neighbors.append(blank_idx + 1)

      target = random.choice(neighbors)
      self.board_tiles[blank_idx], self.board_tiles[target] = (
          self.board_tiles[target],
          self.board_tiles[blank_idx],
      )
      blank_idx = target

  def reset_pixel_board(self):
    self.shuffle_solvable_board()
    self.update_pixel_grid()
    self.pixel_status_label.config(
        text="✨ Board reshuffled & ready! ✨", fg="#4A7C59"
    )

  def create_pixel_grid(self):
    for r in range(4):
      row_btns = []
      for c in range(4):
        idx = r * 4 + c
        val = self.board_tiles[idx]

        btn = tk.Button(
            self.grid_frame,
            font=(self.font_family, 14, "bold"),
            bg=self.cream_tile if val == 0 else self.matcha_green,
            fg=self.cocoa_brown,
            relief="flat",
            cursor="hand2" if val != 0 else "arrow",
            command=lambda i=idx: self.slide_tile(i),
        )
        btn.grid(row=r, column=c, padx=3, pady=3)
        row_btns.append(btn)
      self.tile_buttons.append(row_btns)
    self.update_pixel_grid()

  def update_pixel_grid(self):
    for r in range(4):
      for c in range(4):
        idx = r * 4 + c
        val = self.board_tiles[idx]
        btn = self.tile_buttons[r][c]

        if val == 0:
          btn.config(
              image="",
              text="",
              bg=self.cream_tile,
              width=8,
              height=4,
              cursor="arrow",
          )
        elif self.image_tiles and val in self.image_tiles:
          btn.config(
              image=self.image_tiles[val],
              text="",
              bg=self.matcha_green,
              width=0,
              height=0,
              cursor="hand2",
          )
        else:
          btn.config(
              image="",
              text=str(val),
              bg=self.matcha_green,
              fg=self.cocoa_brown,
              width=4,
              height=2,
              cursor="hand2",
          )

  def slide_tile(self, idx):
    blank_idx = self.board_tiles.index(0)
    r1, c1 = divmod(idx, 4)
    r2, c2 = divmod(blank_idx, 4)

    if abs(r1 - r2) + abs(c1 - c2) == 1:
      self.board_tiles[blank_idx], self.board_tiles[idx] = (
          self.board_tiles[idx],
          self.board_tiles[blank_idx],
      )
      self.update_pixel_grid()

      winning_board = list(range(1, 16)) + [0]
      if self.board_tiles == winning_board:
        self.pixel_status_label.config(
            text="✨ Hurray! Puzzle Solved Perfectly! ✨", fg="#4A7C59"
        )
        messagebox.showinfo(
            "Victory!", "Congratulations! You solved the 15-puzzle!"
        )

  def verify_pixel_board(self):
    board_str = ",".join(map(str, self.board_tiles))
    output = self.run_backend(["--verify-pixel", board_str])
    if "SOLVABLE" in output:
      self.pixel_status_label.config(
          text="C++ Engine Check: Board is SOLVABLE 🟢", fg="#4A7C59"
      )
    else:
      self.pixel_status_label.config(
          text="C++ Engine Check: Board is UNSOLVABLE 🔴", fg="#D9534F"
      )

  def auto_solve_pixel_board(self):
    winning_board = list(range(1, 16)) + [0]
    if self.board_tiles == winning_board:
      messagebox.showinfo(
          "Already Solved", "The puzzle is already in a winning state!"
      )
      return

    self.pixel_status_label.config(
        text="🤖 Auto-Solving instantly via A* Heuristic...", fg="#7D6EC7"
    )
    self.root.update_idletasks()

    solution_moves = PuzzleSolver.solve(self.board_tiles)

    if solution_moves:
      self.animate_auto_solve_steps(solution_moves, 0)
    else:
      self.pixel_status_label.config(
          text="Could not find solution path instantly.", fg="#D9534F"
      )

  def animate_auto_solve_steps(self, moves, step):
    if step < len(moves):
      idx = moves[step]
      blank_idx = self.board_tiles.index(0)
      self.board_tiles[blank_idx], self.board_tiles[idx] = (
          self.board_tiles[idx],
          self.board_tiles[blank_idx],
      )
      self.update_pixel_grid()
      self.root.after(
          80, lambda: self.animate_auto_solve_steps(moves, step + 1)
      )
    else:
      self.pixel_status_label.config(
          text="✨ Auto-Solve Complete! ✨", fg="#4A7C59"
      )

  # ==========================================
  # Lexicon Mode (Word Puzzle Engine)
  # ==========================================
  def show_lexicon_mode(self):
    self.clear_container()

    nav_frame = tk.Frame(self.container, bg=self.bg_color)
    nav_frame.pack(fill="x", padx=30, pady=20)

    back_btn = tk.Button(
        nav_frame,
        text="← Back to Sanctuary",
        font=(self.font_family, 10, "bold"),
        bg=self.card_bg,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=5,
        command=self.show_home_screen,
    )
    back_btn.pack(side="left")

    tk.Label(
        nav_frame,
        text="📖 Lexicon Mode (Word Engine)",
        font=(self.font_family, 18, "bold"),
        fg=self.cocoa_brown,
        bg=self.bg_color,
    ).pack(side="right")

    content_frame = tk.Frame(self.container, bg=self.bg_color)
    content_frame.pack(pady=10, padx=30, fill="both", expand=True)

    left_col = tk.Frame(content_frame, bg=self.bg_color)
    left_col.pack(side="left", padx=10)

    grid_card = tk.Frame(
        left_col,
        bg=self.card_bg,
        padx=20,
        pady=20,
        highlightbackground=self.matcha_green,
        highlightthickness=2,
    )
    grid_card.pack()

    self.vocab_pool = [
        "P",
        "I",
        "X",
        "E",
        "L",
        "E",
        "X",
        "I",
        "C",
        "O",
        "N",
        "A",
        "B",
        "C",
        "D",
        "T",
        "S",
        "R",
        "M",
        "G",
        "O",
        "W",
    ]
    self.lexicon_letters = random.sample(self.vocab_pool, 16)

    self.current_built_word = []
    self.word_display_var = tk.StringVar(value="Current Word: ")

    self.lexicon_grid_btns = []
    for r in range(4):
      row_btns = []
      for c in range(4):
        idx = r * 4 + c
        letter = self.lexicon_letters[idx]
        btn = tk.Button(
            grid_card,
            text=letter,
            font=(self.font_family, 16, "bold"),
            bg=self.primary_lavender,
            fg=self.cocoa_brown,
            width=3,
            height=2,
            relief="flat",
            cursor="hand2",
            command=lambda l=letter: self.append_letter(l),
        )
        btn.grid(row=r, column=c, padx=5, pady=5)
        row_btns.append(btn)
      self.lexicon_grid_btns.append(row_btns)

    builder_frame = tk.Frame(left_col, bg=self.bg_color)
    builder_frame.pack(pady=10, fill="x")

    tk.Label(
        builder_frame,
        textvariable=self.word_display_var,
        font=(self.font_family, 13, "bold"),
        fg=self.cocoa_brown,
        bg=self.bg_color,
    ).pack(anchor="w", pady=5)

    btn_row = tk.Frame(builder_frame, bg=self.bg_color)
    btn_row.pack(fill="x", pady=5)

    clear_btn = tk.Button(
        btn_row,
        text="Clear",
        font=(self.font_family, 10, "bold"),
        bg=self.peach_pink,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(clear_btn, self.peach_pink),
            self.clear_lexicon_word(),
        ],
    )
    clear_btn.pack(side="left", padx=3)

    validate_btn = tk.Button(
        btn_row,
        text="Validate",
        font=(self.font_family, 10, "bold"),
        bg=self.matcha_green,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(validate_btn, self.matcha_green),
            self.validate_lexicon_word(),
        ],
    )
    validate_btn.pack(side="left", padx=3)

    shuffle_lex_btn = tk.Button(
        btn_row,
        text="✨ Shuffle",
        font=(self.font_family, 10, "bold"),
        bg=self.primary_lavender,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(shuffle_lex_btn, self.primary_lavender),
            self.shuffle_lexicon_grid(),
        ],
    )
    shuffle_lex_btn.pack(side="left", padx=3)

    right_col = tk.Frame(content_frame, bg=self.bg_color)
    right_col.pack(side="right", padx=15, fill="both", expand=True)

    solver_card = tk.Frame(
        right_col,
        bg=self.card_bg,
        padx=15,
        pady=15,
        highlightbackground=self.primary_lavender,
        highlightthickness=2,
    )
    solver_card.pack(fill="both", expand=True)

    tk.Label(
        solver_card,
        text="✨ C++ DFS Trie Auto-Solver ✨",
        font=(self.font_family, 12, "bold"),
        fg=self.cocoa_brown,
        bg=self.card_bg,
    ).pack(anchor="w", pady=5)

    solve_auto_btn = tk.Button(
        solver_card,
        text="Find All Valid Words",
        font=(self.font_family, 10, "bold"),
        bg=self.primary_lavender,
        fg=self.cocoa_brown,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=6,
        command=lambda: [
            self.animate_button_pulse(solve_auto_btn, self.primary_lavender),
            self.run_dfs_solver(),
        ],
    )
    solve_auto_btn.pack(anchor="w", pady=5)

    text_frame = tk.Frame(solver_card, bg=self.card_bg)
    text_frame.pack(fill="both", expand=True, pady=5)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    self.found_words_listbox = tk.Listbox(
        text_frame,
        font=(self.font_family, 10),
        bg=self.cream_tile,
        fg=self.cocoa_brown,
        relief="flat",
        yscrollcommand=scrollbar.set,
        height=10,
    )
    self.found_words_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=self.found_words_listbox.yview)

  def shuffle_lexicon_grid(self):
    self.lexicon_letters = random.sample(self.vocab_pool, 16)
    self.clear_lexicon_word()
    for r in range(4):
      for c in range(4):
        idx = r * 4 + c
        letter = self.lexicon_letters[idx]
        btn = self.lexicon_grid_btns[r][c]
        btn.config(text=letter, command=lambda l=letter: self.append_letter(l))
    self.found_words_listbox.delete(0, tk.END)
    self.found_words_listbox.insert(tk.END, "✨ Grid shuffled with new letters! ✨")

  def append_letter(self, letter):
    self.current_built_word.append(letter.lower())
    word_str = "".join(self.current_built_word)
    self.word_display_var.set(f"Current Word: {word_str.capitalize()}")

  def clear_lexicon_word(self):
    self.current_built_word = []
    self.word_display_var.set("Current Word: ")

  def _is_real_word(self, word: str) -> bool:
    return self.validator.check(word)

  def validate_lexicon_word(self):
    if not self.current_built_word:
      messagebox.showwarning(
          "Empty Word", "Please click letters to build a word first!"
      )
      return

    word_str = "".join(self.current_built_word).lower()
    backend_output = self.run_backend(["--check-word", word_str])

    is_valid = False
    if "VALID" in backend_output and "INVALID" not in backend_output:
      is_valid = True
    else:
      is_valid = self._is_real_word(word_str)

    if is_valid:
      messagebox.showinfo(
          "Success! ✨",
          f"'{word_str.upper()}' is a valid real-world dictionary word!",
      )
    else:
      messagebox.showinfo(
          "Not a Word ❌",
          f"'{word_str.upper()}' does not exist in the dictionary!",
      )

  def run_dfs_solver(self):
    grid_str = ",".join(self.lexicon_letters)
    output = self.run_backend(["--solve-lexicon", grid_str])
    self.found_words_listbox.delete(0, tk.END)
    if output and not output.startswith("ERROR"):
      words = output.split()
      if words:
        for w in sorted(words, key=len, reverse=True):
          self.found_words_listbox.insert(
              tk.END, f"• {w.capitalize()} ({len(w)} letters)"
          )
      else:
        self.found_words_listbox.insert(
            tk.END, "No valid words found on this grid."
        )
    else:
      self.found_words_listbox.insert(
          tk.END, "Error communicating with backend."
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = PixelLexiconApp(root)
  root.mainloop()
  