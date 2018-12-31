class Board:
    def __init__(self):
        self.width = 7
        self.height = 7
        self.board = self.init_board()
        self.directions = {'N': (0, 1), 'S': (0, -1),
                           'E': (-1, 0), 'W': (1, 0)}
        self.coordIndex = {'N': ("x", 0), 'S': ("x", self.height-1),
                           'E': (self.width-1, "x"), 'W': (0, "x")}
        self.indexes = ["A", "B", "C", "D", "c", "b", "a"]

    def init_board(self):
        filled_board = {}
        for i in xrange(self.width):
            for j in xrange(self.height):
                filled_board[(i, j)] = "E"
        return filled_board

    def print_board(self):
        print("\n         N\n\n    A B C D c b a")
        for y in xrange(self.height):
            if y != self.height/2:
                print("   +-+-+-+-+-+-+-+")
            else:
                print("W  +-+-+-+-+-+-+-+  E")
            to_print = "  "+self.indexes[y]+"|"
            for x in xrange(self.width):
                to_print += self.board[(x, y)] + "|"
            print(to_print+self.indexes[y])
        print("   +-+-+-+-+-+-+-+\n    A B C D c b a\n\n         S\n")

    def push(self, play, mark):
        direction = list(self.directions[play[0]])
        coords = list(self.coordIndex[play[0]])
        length = self.height if coords.index('x') == 0 else self.width
        coords[coords.index('x')] = self.indexes.index(play[1])
        for i in xrange(length):
            self.board[tuple(coords)], mark = mark, self.board[tuple(coords)]
            coords = [coords[0] + direction[0], coords[1] + direction[1]]

    def check_win_condition(self):
        won = self.check_win_condition_smart(False)
        return not won[0], won[1]

    def check_win_condition_smart(self, smart):
        axes = []
        instructions = [[0, 0, 0, 1, 3, 1],
                        [self.height, self.width, self.height-3,
                        self.width-3, self.height, self.width-3],
                        [(0, "a"), ("a", 0), (0, "a"),
                        ("a", 0), (0, "a"), ("a", 6)],
                        [1, 0, 1, 1, 1, 1], [0, 1, 1, 1, -1, -1]]
        for b in xrange(6):  # horizontal, vertical and all 4 diagonals
            for a in xrange(instructions[0][b], instructions[1][b]):
                current = list(instructions[2][b])
                current[current.index('a')] = a
                current = tuple(current)
                check = ""
                while current in self.board:
                    check += self.board[current].upper()
                    current = (current[0] + instructions[3][b],
                               current[1] + instructions[4][b])
                if smart:
                    axes += [check]
                if self.check_string(check)[0]:
                    return self.check_string_smart(check, smart, axes)
        if smart:
            return False, "OX", self.break_up_axes(axes)
        else:
            return False, "OX"

    def check_string_smart(self, string, smart, axes):
        (won, mark) = self.check_string(string)
        if smart:
            return won, mark, self.break_up_axes(axes)
        else:
            return won, mark

    def check_string(self, string):
        return (True, "X") if "XXXX" in string else ((True, "O") if "OOOO" in string else (False, "OX"))

    def break_up_axes(self, axes):
        rAxes = []
        for num in xrange(len(axes)):
            for idx in xrange(len(axes[num])-3):
                rAxes += [axes[num][idx:(idx+4)]]
        return rAxes