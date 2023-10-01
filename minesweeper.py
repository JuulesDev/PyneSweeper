from random import random
from typing import List
import time


class MinesweeperGame:
  """Just a simple minesweeper implementation in python.
  """
  _MINE_VALUE = -1
  started_timestamp = time.time()
  guesses_counter = 0
  is_game_over = False

  def __init__(self, board_size: (int, int), mines_odds: float = 0.1) -> None:
    """Initialize a game of minesweeper.

    Args:
        board_size (int, int): The size of the board.
        mines_odds (float, optional): The odds a cell has to be a mine. Defaults to 0.1.
    """
    self._width, self._height = board_size
    self._mines_odds = mines_odds
    self._values_board = self._generate_neighbours(self._generate_values_board())
    self._mask_board = [[True for _ in range(self._width)] for _ in range(self._height)]

  def _generate_values_board(self) -> List[List[int]]:
    """Fills the board values. Has mines_odds to be a mine (= self._MINE_VALUE). 
    """
    board = []
    for y in range(self._height):
      row = []
      for x in range(self._width):
        if random() > self._mines_odds:
          row.append(0)
        else:
          row.append(self._MINE_VALUE)
      board.append(row)
    return board

  def get_visible_board(self) -> List[List[int]]:
    """Returns all the values that are visible by the player.

    Returns:
      List[List[int]]: The board, values are either a positive number (the
        number of mines next to this cell), self._MINE_VALUE if the cell is a mine or None
        if the value is hidden.
    """
    result = []
    for y in range(self._height):
      row = []
      for x in range(self._width):
        if self._mask_board[y][x]:
          row.append(None)
        else:
          row.append(self._values_board[y][x])
      result.append(row)
    return result

  def _is_valid_cell(self, cell_x, cell_y) -> bool:
    """Checks if the given cell coordinates are valid.

    Args:
        cell_x (int): The x-coordinate of the cell.
        cell_y (int): The y-coordinate of the cell.

    Returns:
        bool: True if the cell coordinates are valid, False otherwise.
    """
    return 0 <= cell_y < self._height and 0 <= cell_x < self._width

  def _count_neighbours(self, board: List[List[int]], cell_x: int, cell_y: int) -> int:
    """Count the number of neighbours a cell has.

    Args:
        board (List[List[int]]): The board to check the neighbours from, filled with -1's and 0's.
        cell_x (int): The x coordinate of the cell.
        cell_y (int): The y coordinate of the cell.

    Returns:
        int: The number of neighbours of the cell (between 0 and 8).
    """
    n_neighbours = 0
    for offset_y in [-1, 0, 1]:
      for offset_x in [-1, 0, 1]:
        if offset_y == 0 and offset_x == 0: continue
        if not self._is_valid_cell(cell_x + offset_x, cell_y + offset_y): continue

        if board[cell_y + offset_y][cell_x + offset_x] == self._MINE_VALUE:
          n_neighbours += 1
    return n_neighbours

  def _generate_neighbours(self, board: List[List[int]]) -> List[List[int]]:
    """Converts a board filled with 0's and -1's by changing the 0's into the number of -1's next to it.

    Args:
        board (List[List[int]]): The board to convert.

    Returns:
        List[List[int]]: The converted board.
    """
    new_board = board[::]
    for y in range(self._height):
      for x in range(self._width):
        if board[y][x] == self._MINE_VALUE: continue
        new_board[y][x] = self._count_neighbours(board, x, y)       
    return new_board

  def _check_game_over(self) -> bool:
    """Checks if the game is over.

    Returns:
        bool: True if the game is over, else False.
    """
    undiscovered_non_mines = False
    for y in range(self._height):
      for x in range(self._width):
        masked = self._mask_board[y][x]
        is_mine = self._values_board[y][x] == -1 # TODO: Flags.
        if not masked and is_mine: return True
        if masked and not is_mine: undiscovered_non_mines = True
    return not undiscovered_non_mines # All non-mine cells are discovered, and no mine is.7

  def _chain_discovery(self, cell_x: int, cell_y: int) -> None:
    """Unmask cells recursively if they have no mine neighbours.

    Args:
        cell_x (int): The x coordinate of the cell.
        cell_y (int): The y coordinate of the cell.
    """
    for offset_y in [-1, 0, 1]:
      for offset_x in [-1, 0, 1]:
        if offset_y == 0 and offset_x == 0: continue
        # Computes next cell coordinates and checks if its valid
        new_x, new_y = cell_x + offset_x, cell_y + offset_y
        if not self._is_valid_cell(new_x, new_y): continue
        if self._mask_board[new_y][new_x] == False: continue
        # Makes the next cell discovered and 'chain discovers' it.
        self._mask_board[new_y][new_x] = False
        if self._values_board[new_y][new_x] == 0:
          self._chain_discovery(new_x, new_y)

  def play(self, x: int, y: int, is_mine: bool) -> bool:
    """Plays on a specific cell, i.e. the player tries to guess if a cell is a bomb or not.

    Args:
        x (int): The x coordinate where to guess.
        y (int): The y coordinate where to guess.
        is_mine (bool): Whether the player thinks the cell is a mine (True) or not (False).

    Returns:
        bool: If the guess was registered, False can be caused by wrong coordinates or already discovered cell.
    """
    # TODO: Implement flag system.
    if not self._is_valid_cell(x, y): return False
    if self._mask_board[y][x] == False: return False # Cell already discoverd
    self._mask_board[y][x] = False
    if self._values_board[y][x] == 0:
      self._chain_discovery(x, y)
    self.guesses_counter += 1
    self.is_game_over = self._check_game_over()
    return True
