from pprint import pprint

from minesweeper import MinesweeperGame
import cli

def main():
  game = MinesweeperGame((56, 24), 0.2)

  board = game.get_visible_board()
  # pprint(game._board_values)

  cli.print_board(board)


if __name__ == '__main__':
  main()