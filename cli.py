
def print_board(board) -> None:
  w, h = len(board[0]), len(board)
  print('+%s+' % ('-' * w))
  for y in range(h):
    row = ""
    for x in range(w):
      val = board[y][x]
      if val == None:
        row += '#'
      elif val == -1:
        row += 'X'
      elif val == 0:
        row += '.'
      else:
        row += str(val)
    print('|%s|' % row)
  print('+%s+' % ('-' * w))