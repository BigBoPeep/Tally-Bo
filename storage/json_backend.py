from dataclasses import asdict
from models import GameSession
from pathlib import Path
from storage.base import AbstractSaveBackend
import json

class JsonSaveBackend(AbstractSaveBackend):
  def __init__(self, app_dir: Path) -> None:
    super().__init__(app_dir)

  def save(self, session: GameSession) -> None: 
    path = self._path(session)
    path.write_text(json.dumps(asdict(session), indent=2))

  def load(self, session_id: str) -> GameSession: 
    matches = list(self._save_dir.glob(f"*_{session_id[:8]}.json"))
    if not matches:
      raise FileNotFoundError(f"No session found for id {session_id}")
    data = json.loads(matches[0].read_text())
    return GameSession(**data)

  def list_sessions(self, status: str | None = None) -> list[GameSession]: 
    sessions = [
      GameSession(**json.loads(p.read_text()))
      for p in sorted(self._save_dir.glob("*.json"))
    ]
    if status:
      sessions = [s for s in sessions if s.status == status]
    return sessions

  def delete(self, session_id: str) -> None: 
    matches = list(self._save_dir.glob(f"*_{session_id[:8]}.json"))
    if matches:
      matches[0].unlink()

  def _path(self, session: GameSession) -> Path:
    date = session.created_at[:10]
    return self._save_dir / f"{session.game_type}_{date}_{session.session_id[:8]}.json"