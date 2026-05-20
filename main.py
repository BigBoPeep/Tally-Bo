from games import list_games, get_game
from storage.json_backend import JsonSaveBackend
from ui.console import ConsoleUI
from config import APP_DIR

def main():
  ui = ConsoleUI()
  storage = JsonSaveBackend(app_dir=APP_DIR)

main()