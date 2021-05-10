import random


class TicTacToe:

    def __init__(self):
        self.board = [None]*9

    def make_move(self, row: int, col: int, player):
        position = col*3 + row
        self.board[position] = player
        return

    def make_random_move(self, player):
        available_squares = []
        for i in range(9):
            if self.board[i] is None:
                available_squares.append(i)
        position = random.choice(available_squares)
        self.board[position] = player
        return

    def _get_position(self, row, col):
        return col*3 + row

    def _get_board_state(self, row, col):
        position = self._get_position(row, col)
        return self.board[position]

    def _check_diagonal_win(self):
        center_square = self._get_board_state(1, 1)
        if not center_square:
            return None

        if ((center_square == self._get_board_state(0, 0)) and
                (center_square == self._get_board_state(2, 2))):
            return center_square
        elif ((center_square == self._get_board_state(0, 2)) and
              (center_square == self._get_board_state(2, 0))):
            return center_square

        return None

    def _check_row_win(self):
        for row in (0, 1, 2):
            if (self._get_board_state(row, 0) ==
                self._get_board_state(row, 1) ==
                    self._get_board_state(row, 2)):
                return self._get_board_state(row, 0)

        return None

    def _check_col_win(self):
        for col in (0, 1, 2):
            if (self._get_board_state(0, col) ==
                self._get_board_state(1, col) ==
                    self._get_board_state(2, col)):
                return self._get_board_state(0, col)

        return None

    def check_win(self):
        for check_winner in (self._check_diagonal_win,
                             self._check_row_win,
                             self._check_col_win):
            winner = check_winner()
            if winner:
                return winner

        return None

    def display_board(self):
        board = [square or ' ' for square in self.board]

        template = f"""
          {board[0]} | {board[1]} | {board[2]}
         --- --- ---
          {board[3]} | {board[4]} | {board[5]}    
         --- --- ---
          {board[6]} | {board[7]} | {board[8]}    
        """

        print(template)

        return


def main():
    ttt = TicTacToe()

    while True:
        ttt.display_board()
        print("Player X, choose your next move!")
        row, col = [int(square) for square in input().split(',')]
        ttt.make_move(row, col, 'X')
        winner = ttt.check_win()
        if winner:
            print(f"Player {winner} has won!")
            break

        ttt.make_random_move('O')
        winner = ttt.check_win()
        if winner:
            print(f"Player {winner} has won!")
            break

    return


if __name__ == '__main__':
    main()