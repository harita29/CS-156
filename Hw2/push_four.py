from board import Board
from push_four_minmax import MinMax
depth = 3
b = Board()

print("\nWelcome to the Push Four Game!\n\n")
input = raw_input("Would you like to go first (y/n): ")
if input == "y":
    player = "X"
    computer = "O"
else:
    player = "O"
    computer = "X"

player_status = "You, Player "+player+" have not moved yet."
computer_move = ""
if player != "X":
    b, computer_status, computer_move = MinMax(b, computer, depth, "",).play()
else:
    computer_status = "Player "+computer+" has not moved yet."


def print_status():
    print("\n"+player_status+"\n"+computer_status)
    b.print_board()


print_status()
while b.check_win_condition()[0]:
    play = raw_input("Please enter a move (direction letter from N,E,W,S followed by a row or column letter): ")
    if len(play) < 2 or play[0] not in b.directions or play[1] not in b.indexes or \
            (len(computer_move) > 1 and computer_move[1].lower() == play[1].lower()):
        print "SAME LETTER RULE: Violated!"
        continue
    player_status = "You, Player "+player+" played "+play+"."
    b.push(play, player)
    if not b.check_win_condition()[0]:
        print_status()
        break
    b, computer_status, computer_move = MinMax(b, computer, depth, play).play()
    print_status()
won = b.check_win_condition()[1]
print("Player "+won+" Wins! You " + ("Win" if player == won else "Lose") + "!")
