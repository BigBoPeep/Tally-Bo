from datetime import datetime, timezone
from models import GameSession, Player, Turn
from games.base import AbstractGame
from games import list_games, get_game
from storage.base import AbstractSaveBackend
from ui.base import AbstractUI

class AppController:
  def __init__(self, ui: AbstractUI, storage: AbstractSaveBackend) -> None:
    self.ui = ui
    self.storage = storage
    self._running = False

  def run(self) -> None:
    self._running = True
    self.ui.show_message("Welcome to Tally-Bo!")

    while self._running:
      self._main_menu()

  def _main_menu(self) -> None:
    options = ["New Game", "Resume Game", "View Completed Games", "Quit"]
    choice = self.ui.show_menu("Main Menu", options)
    
    match choice:
      case 0: self._new_game()
      case 1: self._resume_game()
      case 2: self._view_completed()
      case 3: self._quit()

  def _new_game(self) -> None:
    available = list_games()
    if not available:
      self.ui.show_message("No games installed")
      return
    
    game_names = [g.name for g in available]
    idx = self.ui.show_menu("Choose a game", game_names)
    game = available[idx]

    players = self._collect_players()
    if not players:
      return
    
    session = game.new_session(players)
    self.storage.save(session)
    self.ui.show_message(f"Starting {game.name} with "
                         f"{', '.join(p.name for p in players)}")
    self._gameplay_loop(game, session)

  def _collect_players(self) -> list[Player]:
    players: list[Player] = []
    
    while True:
      prompt = (f"Enter name for Player #{len(players) + 1} "
                "(or blank to start)")
      name = self.ui.prompt(prompt).strip()

      if not name:
        if(len(players) < 2):
          self.ui.show_message("Need at least 2 players")
          continue
        break

      players.append(Player(name=name))

    return players
  
  def _resume_game(self) -> None:
    sessions = self.storage.list_sessions(status="in_progress")
    if not sessions:
      self.ui.show_message("No games in progress")
      return
    
    options = [str(s) for s in sessions]
    options.append("< Back")
    idx = self.ui.show_menu("Resume which game?", options)

    if idx == len(sessions):
      return
    
    session = sessions[idx]
    game = get_game(session.game_type)

    self.ui.show_message(f"Resuming {session} ({len(session.turns)} "
                         "turns played)")
    
    self._gameplay_loop(game, session)

  def _view_completed(self) -> None:
    sessions = self.storage.list_sessions(status="completed")
    if not sessions:
      self.ui.show_message("No completed games saved")
      return
    
    options = [str(s) for s in sessions]
    options.append("< Back")
    idx = self.ui.show_menu("View which game?", options)

    if idx == len(sessions):
      return
    
    session = sessions[idx]
    game = get_game(session.game_type)
    scores = game.get_scores(session)
    winner = game.get_winner(session)

    self.ui.show_scores(scores)
    if winner:
      self.ui.show_message(f"Winner: {winner.name}")

  def _gameplay_loop(self, game: AbstractGame, session: GameSession) -> None:
    player_map = {p.player_id: p for p in session.players}

    while True:
      scores = game.get_scores(session)
      self.ui.show_scores(scores)

      options = (
        [f"Record turn for {p.name}" for p in session.players] +
        ["Save & Return to Menu"]
      )
      choice = self.ui.show_menu("What next?", options)
      
      if choice == len(session.players):
        self.storage.save(session)
        self.ui.show_message("Game saved.")
        return
      
      player = session.players[choice]
      score_delta, metadata = game.prompt_turn(self.ui, player, session)

      turn = Turn(
        player_id=player.player_id,
        score_delta=score_delta,
        metadata=metadata,
        timestamp=datetime.now(timezone.utc).isoformat()
      )

      session = game.record_turn(session, turn)
      self.storage.save(session)

      if game.is_game_over(session):
        self._end_game(game, session)
        return
      
  def _end_game(self, game: AbstractGame, session: GameSession) -> None:
    session.status = "completed"
    session.completed_at = datetime.now(timezone.utc).isoformat()
    self.storage.save(session)

    self.ui.show_message("Game over!")
    scores = game.get_scores(session)
    self.ui.show_scores(scores)

    winner = game.get_winner(session)
    if winner:
      self.ui.show_message(f"{winner.name} wins!")

  def _quit(self):
    self.ui.show_message("Goodbye!")
    self._running = False