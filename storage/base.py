from abc import ABC, abstractmethod
from games.base import GameSession
from pathlib import Path

class AbstractSaveBackend(ABC):
  def __init__(self, app_dir: Path) -> None:
    self._save_dir = app_dir / "storage"
    self._save_dir.mkdir(parents=True, exist_ok=True)

  @abstractmethod
  def save(self, session: GameSession) -> None: ...

  @abstractmethod
  def load(self, session_id: str) -> GameSession: ...

  @abstractmethod
  def list_sessions(self, status: str | None = None) -> list[GameSession]: ...

  @abstractmethod
  def delete(self, session_id: str) -> None: ...

'''
------------------ New Storage Class Boilerplate ------------------


  def save(self, session: GameSession) -> None: ...

  def load(self, session_id: str) -> GameSession: ...

  def list_sessions(self, status: str | None = None) -> list[GameSession]: ...

  def delete(self, session_id: str) -> None: ...
'''