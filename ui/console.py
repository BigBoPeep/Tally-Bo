from typing import Literal
from ui.base import AbstractUI
from config import CONSOLE_UI_HEIGHT, CONSOLE_UI_WIDTH, CONSOLE_X_CHAR, CONSOLE_Y_CHAR, APP_NAME
import os

class ConsoleUI(AbstractUI):
  def __init__(self) -> None:
    super().__init__()
    self._user_message = None
    self._last_nav_choice = None

  def show_menu(self, title: str, options: list[str]) -> int: 
    if len(options) <= CONSOLE_UI_HEIGHT:
      while True:
        inp = self._print_page(title, options, offset=0)
        if inp is not None: return inp
        else:
          self._user_message = "Please enter a valid option"
          continue
    
    page = 0
    total_pages = (len(options) + CONSOLE_UI_HEIGHT - 1) // CONSOLE_UI_HEIGHT

    while True:
      offset = page * CONSOLE_UI_HEIGHT
      items = options[offset:offset + CONSOLE_UI_HEIGHT]

      nav: dict[str, str] = {}
      if page < total_pages - 1: nav['+'] = "Next Page"
      if page > 0: nav['-'] = "Prev Page"

      choice = self._print_page(
        f"{title} ({page + 1}/{total_pages})",
        items,
        offset,
        nav
      )
      
      if choice is not None: return choice
      
      match self._last_nav_choice:
        case "-": page -= 1
        case "+": page += 1
        case _: continue

  def prompt(self, message: str) -> str: 
    return input(message).strip()

  def show_scores(self, scores: dict[str, tuple[str, int]]): 
    score_strs = [f"{n}) {s}" for i, (n, s) in scores]
    if len(score_strs) <= CONSOLE_UI_HEIGHT:
      self._print_scores("Phase10 - Scores", score_strs, 0, {})
    
    page = 0
    total_pages = (len(scores) + CONSOLE_UI_HEIGHT - 1) // CONSOLE_UI_HEIGHT

    while True:
      offset = page * CONSOLE_UI_HEIGHT
      items = score_strs[offset:offset + CONSOLE_UI_HEIGHT]

      nav: dict[str, str] = {'x': "Back"}
      if page < total_pages - 1: nav['+'] = "Next Page"
      if page > 0: nav['-'] = "Prev Page"

      choice = self._print_scores(f"Phase10 - Scores ({page + 1}/{total_pages})",
                                  items, offset, nav)

      match self._last_nav_choice:
        case "x": return
        case "-": page -= 1
        case "+": page += 1
        case _: continue

  def show_message(self, message: str): 
    self._user_message = message

  def collect_players(self, min_players: int = 2) -> list[str]: 
    names: list[str] = []

    while True:
      self._clear()
      self._print_title("Add Players")

      for i, name in enumerate(names):
        print(self._add_border(f"{i + 1}) {name}"))
      for _ in range(CONSOLE_UI_HEIGHT - len(names)):
        print(self._add_border(" "))

      if len(names) >= min_players:
        self._print_footer(["Leave blank to start"])
      else: self._print_footer([f"Need at least {min_players} players"])

      raw = self.prompt(f"Player #{len(names) + 1} name: ").strip()

      if not raw:
        if len(names) < min_players:
          self._user_message = f"Need at least {min_players} players"
          continue
        return names
      
      names.append(raw)

  def _clear(self) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

  def _print_title(self, title: str) -> None:
    print(CONSOLE_Y_CHAR * CONSOLE_UI_WIDTH)
    print(self._add_border(APP_NAME, "center"))
    print(self._add_border(title, "center"))
    if self._user_message != None:
      print(self._add_border(self._user_message, "center"))
      self._user_message = None
    else: print(self._add_border(" "))
    print(CONSOLE_Y_CHAR * CONSOLE_UI_WIDTH)

  def _print_footer(self, options: list[str]):
    if len(options) < 1:
      print(self._add_border(" "))
    else:
      print(self._add_border(", ".join(options)))

  def _print_page(self, title: str, items: list[str], offset: int, nav: dict[str, str] = {}) -> int | None:
    while True:
      self._clear()
      self._print_title(title)

      for i, item in enumerate(items):
        print(self._add_border(f" {i + 1}) {item}"))
      for _ in range(CONSOLE_UI_HEIGHT - len(items)):
        print(self._add_border(" "))

      self._print_footer([f"{k}) {v}" for k, v in nav.items()])

      raw = self.prompt("Option: ").lower()

      if raw in nav:
        self._last_nav_choice = raw
        return None

      if not raw.isdigit():
        self._user_message = "Please enter a valid option!!"
        continue

      choice = int(raw) - 1

      if 0 <= choice < len(items):
        return offset + choice
      
      self._user_message = "Please enter a valid option!"

  def _print_scores(self, title: str, items: list[str], offset: int, nav: dict[str, str] = {}) -> None:
    while True:
      self._clear()
      self._print_title(title)
      
      for score_str in items:
        print(self._add_border(score_str))
      for _ in range(CONSOLE_UI_HEIGHT - len(items)):
        print(self._add_border(" "))

      self._print_footer([f"{k}) {v}" for k, v in nav.items()])

      raw = self.prompt("Option: ").lower()

      if raw in nav:
        self._last_nav_choice = raw
        return None
      
      self._last_nav_choice = None

  def _add_border(self, string: str, alignment: Literal['left', 'right', 'center'] = "left") -> str:
    method_name = "center" if alignment == "center" else ("rjust" if alignment == "right" else "ljust")
    padded = getattr(string, method_name)(CONSOLE_UI_WIDTH - 4)
    return f"{CONSOLE_X_CHAR} {padded} {CONSOLE_X_CHAR}"