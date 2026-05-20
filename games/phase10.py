from datetime import datetime, timezone
from games.base import AbstractGame, GameSession, Turn
from ui.base import AbstractUI
from models import Player

class Phase10(AbstractGame):
  def __init__(self) -> None:
    super().__init__()

  @property
  def name(self) -> str: return "Phase10"

  @property
  def game_type(self) -> str: return "phase10"

  def new_session(self, players: list[Player]) -> GameSession: 
    session = GameSession(game_type=self.game_type, players=players, turns=[], 
                          status="in_progress", created_at=datetime.now(timezone.utc).isoformat())
    return session

  def record_turn(self, session: GameSession, turn: Turn) -> GameSession: 
    session.turns.append(turn)
    return session
  
  def get_scores(self, session: GameSession) -> dict[str, tuple[str, int]]: 
    scores = {p.player_id: (p.name, 0) for p in session.players}
    for turn in session.turns:
      scores[turn.player_id] = (scores[turn.player_id][0],
                                scores[turn.player_id][1] + turn.score_delta)
    return scores

  def is_game_over(self, session: GameSession) -> bool: 
    if not self._round_complete(session):
      return False
    return any(
      self._phases_completed(session, p) >= 10 for p in session.players
    )

  def get_winner(self, session: GameSession) -> Player | None: 
    if not self.is_game_over(session):
      return None
    
    scores = self.get_scores(session)
    finishers = [
      p for p in session.players
      if self._phases_completed(session, p) >= 10
    ]

    return min(finishers, key=lambda p: scores[p.player_id])

  def prompt_turn(self, ui: AbstractUI, player: Player, session: GameSession) -> tuple[int, dict]:
    score_delta = None
    while score_delta == None:
      inp = ui.prompt(f"{player.name}'s score this turn:")
      try: score_delta = int(inp)
      except: 
        ui.show_message("Score must be a whole number")
        continue
    
    phase_completed = None
    while phase_completed == None:
      inp = ui.prompt(f"{player.name} completed their phase? (Y/N):").lower()
      if inp != 'y' or inp != 'n': 
        ui.show_message("Enter only Y, y, N, or n")
        continue
      phase_completed = inp

    return (score_delta, {"phase_completed": True if phase_completed == "y" else False})

  def _round_complete(self, session: GameSession) -> bool:
    return len(session.turns) % len(session.players) == 0
  
  def _phases_completed(self, session: GameSession, player: Player) -> int:
    return sum(
      1 for turn in session.turns
      if turn.player_id == player.player_id
      and turn.metadata.get("phase_completed")
    )