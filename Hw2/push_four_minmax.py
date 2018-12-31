from copy import deepcopy

playA = ["N", "S", "E", "W"]
playB = ["A", "B", "C", "D", "c", "b", "a"]


class MinMax:
    def __init__(self, board, mark, depth, lastmov):
        self.board = board
        self.mark = mark
        self.depth = depth
        self.lastMove = lastmov

    def play(self):
        play = self.alphabeta(self.board, self.depth, float('-inf'), float('inf'), True, self.lastMove)[2]
        while self.lastMove and (play[1].lower() == self.lastMove[1].lower()):
            play = self.alphabeta(self.board, self.depth, float('-inf'), float('inf'), True, self.lastMove)[2]
        self.board.push(play, self.mark)
        return self.board, "Player " + self.mark + " moves " + play, play

    def get_moves(self, last_move, board):
        moves = []
        for a in playA:
            for b in playB:
                if not last_move or last_move[1].lower() != b.lower():
                    temp = deepcopy(board)
                    temp.push((a+b), self.mark)
                    moves += [(temp, (a+b))]
        return moves

    def get_score(self, board):
        score = 0
        (x, y, axes) = board.check_win_condition_smart(True)
        for a in axes:
            score += self.calculate_score(self.mark, a)
        return x, y, score
    
    def calculate_score(self, mark, sequence):
        if not sequence:
            return 0
        num_of_x = sequence.count("X")
        num_of_o = sequence.count("O")
        
        if mark == "X":
           if num_of_o == 4:
              return -1024
           elif num_of_o == 3 and num_of_x == 0:
              return -8
           elif num_of_o == 2 and num_of_x == 0:
              return -4
           elif num_of_o == 1 and num_of_x == 0:
              return -2
           elif num_of_x == 4:
              return 1024
           elif num_of_x == 3 and num_of_o == 0:
              return 8
           elif num_of_x == 2 and num_of_o == 0:
              return 4
           elif num_of_x == 1 and num_of_o == 0:
              return 2
           else:
              return 0

        if mark == "O":
           if num_of_x == 4:
              return -1024
           elif num_of_x == 3 and num_of_o == 0:
              return -8
           elif num_of_x == 2 and num_of_o == 0:
              return -4
           elif num_of_x == 1 and num_of_o == 0:
              return -2
           elif num_of_o == 4:
              return 1024
           elif num_of_o == 3 and num_of_x == 0:
              return 8
           elif num_of_o == 2 and num_of_x == 0:
              return 4
           elif num_of_o == 1 and num_of_x == 0:
              return 2
           else:
              return 0
     
    def alphabeta(self, board, depth, alpha, beta, maxin, last_move):
        (winCondition, whoWon, oldScore) = self.get_score(board)
        if depth == 0 or winCondition:
            return oldScore, board, last_move
        children = self.get_moves(last_move, board)
        if maxin:
            best_move = (float('-inf'), board, last_move)
            for child in children:
                best_move = max(best_move, self.alphabeta(child[0], depth - 1, alpha, beta, False, child[1]))
                alpha = max(alpha, best_move[0])
                if beta <= best_move[0]:
                    return best_move
            return best_move
        else:
            best_move = (float('inf'), board, last_move)
            for child in children:
                best_move = min(best_move, self.alphabeta(child[0], depth - 1, alpha, beta, True, child[1]))
                beta = min(beta, best_move[0])
                if alpha >= best_move[0]:
                    return best_move
            return best_move
