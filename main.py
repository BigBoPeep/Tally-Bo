from games import list_games, get_game
from storage.json_backend import JsonSaveBackend
from ui.console import ConsoleUI
from app_controller import AppController
from config import APP_DIR

def main():
  ui = ConsoleUI()
  storage = JsonSaveBackend(APP_DIR)
  controller = AppController(ui, storage)

  controller.run()

main()