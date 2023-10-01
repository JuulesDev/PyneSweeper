from random import randint
import time

from minesweeper import MinesweeperGame
import cli

def main():
  # For testing purposes. Not fully working.
  W, H = 18, 11 
  game = MinesweeperGame((W, H), 0.1)

  while not game.is_game_over:
    board = game.get_visible_board()
    cli.print_board(board)
    game.play(randint(0, W), randint(0, H), True)
    time.sleep(.5)

  board = game.get_visible_board()
  cli.print_board(board)


if __name__ == '__main__':
  main()