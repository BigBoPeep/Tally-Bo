from abc import ABC, abstractmethod

class AbstractUI(ABC):
  @abstractmethod
  def show_menu(self, title: str, options: list[str]) -> int: ...

  @abstractmethod
  def prompt(self, message: str) -> str: ...

  @abstractmethod
  def show_scores(self, scores: dict[str, tuple[str, int]]): ...

  @abstractmethod
  def show_message(self, message: str): ...

'''
------------------ New UI Class Boilerplate ------------------


  def show_menu(self, title: str, options: list[str]) -> int: ...

  def prompt(self, message: str) -> str: ...

  def show_scores(self, scores: dict[str, tuple[str, int]]): ...

  def show_message(self, message: str): ...
'''