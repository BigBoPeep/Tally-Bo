import importlib, pkgutil
from games.base import AbstractGame

_registry: dict[str, AbstractGame] = {}

def register(game: AbstractGame):
  _registry[game.game_type] = game

def get_game(game_type: str) -> AbstractGame:
  return _registry[game_type]

def list_games() -> list[AbstractGame]:
  return list(_registry.values())

for _, module_name, _ in pkgutil.iter_modules(__path__):
  if module_name != "base":
    importlib.import_module(f"games.{module_name}")