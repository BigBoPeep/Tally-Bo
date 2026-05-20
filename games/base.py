from abc import abstractmethod, ABC
from models import Player, GameSession, Turn
from ui.base import AbstractUI

class AbstractGame(ABC):
  @property
  @abstractmethod
  def name(self) -> str: ...

  @property
  @abstractmethod
  def game_type(self) -> str: ...

  @property
  @abstractmethod
  def min_players(self) -> int: ...

  @abstractmethod
  def new_session(self, players: list[Player]) -> GameSession: ...

  @abstractmethod
  def record_turn(self, session: GameSession, turn: Turn) -> GameSession: 
    ...
  
  @abstractmethod
  def get_scores(self, session: GameSession) -> dict[str, tuple[str, int]]: ...

  @abstractmethod
  def is_game_over(self, session: GameSession) -> bool: ...

  @abstractmethod
  def get_winner(self, session: GameSession) -> Player | None: ...

  @abstractmethod
  def prompt_turn(self, ui: AbstractUI, player: Player, session: GameSession) -> tuple[int, dict]:
    ...

'''
------------------ New Game Class Boilerplate ------------------


  @property
  def name(self) -> str: ...

  @property
  def game_type(self) -> str: ...

  @property
  def min_players(self) -> int: ...

  def new_session(self, players: list[Player]) -> GameSession: ...

  def record_turn(self, session: GameSession, turn: Turn) -> GameSession: 
    ...
  
  def get_scores(self, session: GameSession) -> dict[str, tuple[str, int]]: ...

  def is_game_over(self, session: GameSession) -> bool: ...

  def get_winner(self, session: GameSession) -> Player | None: ...

  def prompt_turn(self, ui: AbstractUI, player: Player, session: GameSession) -> tuple[int, dict]:
    ...
'''