from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Player:
  name: str
  player_id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class Turn:
  player_id: str
  score_delta: int
  metadata: dict
  timestamp: str
  turn_id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class GameSession:
  game_type: str
  players: list[Player]
  turns: list[Turn]
  status: str
  created_at: str
  completed_at: str | None = None
  session_id: str = field(default_factory=lambda: str(uuid4()))

  def __str__(self) -> str:
    player_names = ", ".join(p.name for p in self.players)
    date = self.created_at[:10]
    return f"{self.game_type.title()} – {player_names} ({date})"