import random
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    symbols = {'X': '\033[94mX\033[0m', 'O': '\033[91mO\033[0m', ' ': ' '}
    print("      1   2   3")
    for i, row in enumerate(board):
        print("   " + f"{i+1}  " + " | ".join(symbols[cell] for cell in row))
        if i < 2:
            print("     ---+---+---")
    print()

def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]): return True
        if all([board[j][i] == player for j in range(3)]): return True
    if all([board[i][i] == player for i in range(3)]): return True
    if all([board[i][2-i] == player for i in range(3)]): return True
    return False

def get_free_positions(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def player_move(board, player_name, symbol):
    while True:
        try:
            move = input(f"{player_name} ({symbol}), enter your move as row,col (e.g., 2,3): ")
            row, col = [int(x)-1 for x in move.split(",")]
            if board[row][col] == " ":
                board[row][col] = symbol
                break
            else:
                print("\033[93mCell already taken. Try again.\033[0m")
        except (ValueError, IndexError):
            print("\033[93mInvalid input. Enter as row,col (e.g., 2,3).\033[0m")

def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if not get_free_positions(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for (i, j) in get_free_positions(board):
            board[i][j] = "O"
            score = minimax(board, depth + 1, False)
            board[i][j] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for (i, j) in get_free_positions(board):
            board[i][j] = "X"
            score = minimax(board, depth + 1, True)
            board[i][j] = " "
            best_score = min(score, best_score)
        return best_score

def computer_move(board):
    print("\033[95mComputer is thinking...\033[0m")
    time.sleep(1)
    best_score = -float('inf')
    best_move = None
    for (i, j) in get_free_positions(board):
        board[i][j] = "O"
        score = minimax(board, 0, False)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = "O"
        print(f"\033[91mComputer chose position: row {best_move[0]+1}, col {best_move[1]+1}\033[0m")
    else:
        # Should never happen, but just in case
        move = random.choice(get_free_positions(board))
        board[move[0]][move[1]] = "O"
    time.sleep(0.5)

def print_intro():
    print("\033[96m" + "="*30)
    print("  WELCOME TO TIC TAC TOE!")
    print("="*30 + "\033[0m \n")
    print("\033[94mYou are X\033[0m, \033[91mComputer or Player 2 is O\033[0m.")

def print_score(user1, user2, user1_score, user2_score, draw_score):
    print(f"\n\033[93mScoreboard:\033[0m")
    print(f"\033[94m{user1}: {user1_score}\033[0m | \033[91m{user2}: {user2_score}\033[0m | Draws: {draw_score}\n")

def print_result(winner, user1, user2):
    if winner == "X":
        print(f"\033[92mCongratulations {user1}! YOU WIN! 🎉\033[0m")
    elif winner == "O":
        print(f"\033[91mCongratulations {user2}! YOU WIN! 🎉\033[0m")
    else:
        print("\033[93mIt's a draw! 😐\033[0m")

def play_game(user1, user2, mode):
    board = [[" " for _ in range(3)] for _ in range(3)]
    clear_screen()
    print_intro()
    print_board(board)
    for turn in range(9):
        if turn % 2 == 0:
            player_move(board, user1, "X")
        else:
            if mode == "C":
                computer_move(board)
            else:
                player_move(board, user2, "O")
        clear_screen()
        print_intro()
        print_board(board)
        if check_winner(board, "X"):
            print_result("X", user1, user2)
            return "X"
        if check_winner(board, "O"):
            print_result("O", user1, user2)
            return "O"
    print_result(None, user1, user2)
    return "D"

def main():
    clear_screen()
    print("\033[96m" + "="*30)
    print("   WELCOME TO TIC TAC TOE!")
    print("="*30 + "\033[0m \n")
    print("Choose mode:\n1. Play with Computer\n2. Play with Human")
    while True:
        mode = input("Enter 1 or 2: ").strip()
        if mode == "1":
            mode = "C"
            user1 = input("Please enter your name: ")
            user2 = "Computer"
            break
        elif mode == "2":
            mode = "H"
            user1 = input("Player 1, enter your name: ")
            user2 = input("Player 2, enter your name: ")
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

    user1_score = 0
    user2_score = 0
    draw_score = 0
    while True:
        winner = play_game(user1, user2, mode)
        if winner == "X":
            user1_score += 1
        elif winner == "O":
            user2_score += 1
        else:
            draw_score += 1
        print_score(user1, user2, user1_score, user2_score, draw_score)
        again = input("Do you want to play again? (Y/N): ").strip().upper()
        if again != 'Y':
            print("\n\033[95mThanks for playing, have a wonderful day!\033[0m\n")
            break
        clear_screen()

if __name__ == "__main__":
    main()
