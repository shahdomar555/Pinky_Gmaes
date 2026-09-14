import tkinter as tk
import math
import random


# colors
PURPLE = "#5D3FD3"
LIGHT_PURPLE = "#F3D1F4"
PINK = "#D291BC"
DARK_PINK = "#C25BAA"
ACTIVE_PINK = "#B76BA3"
DARKER_PINK = "#9C3C8C"
DARK_GRAY = "#4B4B4B"
TEXT = "#FDE2FF"



# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Pinky Games")
root.geometry("520x650")
root.resizable(False, False)
root.configure(bg=PURPLE)



# Clear Screen


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()



# Home page


def home_page():

    clear_screen()
    root.geometry("520x650")

    title = tk.Label(
        root,
        text="💜 Pinky Games 💜",
        font=("Helvetica", 26, "bold"),
        bg=PURPLE,
        fg=TEXT
    )
    title.pack(pady=(80, 60))

    subtitle = tk.Label(
        root,
        text="Choose Your Game",
        font=("Helvetica", 16, "bold"),
        bg=PURPLE,
        fg="white"
    )
    subtitle.pack(pady=(0, 30))

    # Tic Tac Toe
    tic_button = tk.Button(
        root,
        text="🎀 Tic Tac Toe",
        font=("Helvetica", 14, "bold"),
        bg=PINK,
        fg="white",
        activebackground=ACTIVE_PINK,
        activeforeground="white",
        width=22,
        height=2,
        bd=0,
        command=tic_tac_toe
    )
    tic_button.pack(pady=12)

    # Connect 4
    connect_button = tk.Button(
        root,
        text="💜 Connect 4",
        font=("Helvetica", 14, "bold"),
        bg=PINK,
        fg="white",
        activebackground=ACTIVE_PINK,
        activeforeground="white",
        width=22,
        height=2,
        bd=0,
        command=connect_four
    )
    connect_button.pack(pady=12)

    # Exit
    exit_button = tk.Button(
        root,
        text="Exit",
        font=("Helvetica", 11, "bold"),
        bg=DARK_PINK,
        fg="white",
        activebackground=DARKER_PINK,
        activeforeground="white",
        width=15,
        height=2,
        bd=0,
        command=root.destroy
    )
    exit_button.pack(pady=35)



# Tic Tac Toe


def tic_tac_toe():

    clear_screen()
    root.geometry("520x650")

    board = [""] * 9
    buttons = []
    game_over = False

    title = tk.Label(
        root,
        text="💜 Tic Tac Toe 💜",
        font=("Helvetica", 24, "bold"),
        bg=PURPLE,
        fg=TEXT
    )
    title.pack(pady=(25, 10))

    status = tk.Label(
        root,
        text="Player's Turn",
        font=("Helvetica", 13, "bold"),
        bg=PURPLE,
        fg="white"
    )
    status.pack(pady=5)

    # Difficulty
    difficulty_frame = tk.Frame(
        root,
        bg=PURPLE
    )
    difficulty_frame.pack(pady=10)

    difficulty = tk.StringVar(
        value="Medium"
    )

    tk.Label(
        difficulty_frame,
        text="Difficulty:",
        font=("Helvetica", 11, "bold"),
        bg=PURPLE,
        fg="white"
    ).pack(
        side="left",
        padx=5
    )

    for level in ["Easy", "Medium", "Hard"]:

        tk.Radiobutton(
            difficulty_frame,
            text=level,
            variable=difficulty,
            value=level,
            font=("Helvetica", 10),
            bg=PURPLE,
            fg="white",
            selectcolor=DARK_PINK,
            activebackground=PURPLE,
            activeforeground="white"
        ).pack(side="left")

    board_frame = tk.Frame(
        root,
        bg=PURPLE
    )
    board_frame.pack(pady=15)

    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

   
    # Check Winner
    

    def check_winner(b):

        for a, c, d in winning_combinations:

            if (
                b[a] != ""
                and b[a] == b[c] == b[d]
            ):
                return b[a], (a, c, d)

        if all(b):
            return "Tie", ()

        return None, ()

   
    # minimax
    

    def minimax(b, maximizing):

        result, _ = check_winner(b)

        if result == "O":
            return 1

        if result == "X":
            return -1

        if result == "Tie":
            return 0

        if maximizing:

            best_score = -math.inf

            for i in range(9):

                if b[i] == "":

                    b[i] = "O"

                    score = minimax(
                        b,
                        False
                    )

                    b[i] = ""

                    best_score = max(
                        best_score,
                        score
                    )

            return best_score

        else:

            best_score = math.inf

            for i in range(9):

                if b[i] == "":

                    b[i] = "X"

                    score = minimax(
                        b,
                        True
                    )

                    b[i] = ""

                    best_score = min(
                        best_score,
                        score
                    )

            return best_score

    
    # best move
    

    def best_move():

        best_score = -math.inf
        move = None

        for i in range(9):

            if board[i] == "":

                board[i] = "O"

                score = minimax(
                    board,
                    False
                )

                board[i] = ""

                if score > best_score:

                    best_score = score
                    move = i

        return move

   
    # blink winner cells
    

    def blink_winner_cells(
        combo,
        count=0
    ):

        if not combo:
            return

        if count >= 6:

            for i in combo:
                buttons[i].config(
                    bg=LIGHT_PURPLE
                )

            return

        color = (
            DARK_PINK
            if count % 2 == 0
            else LIGHT_PURPLE
        )

        for i in combo:
            buttons[i].config(
                bg=color
            )

        root.after(
            250,
            lambda: blink_winner_cells(
                combo,
                count + 1
            )
        )

    
    # finish

    def finish_game(
        result,
        combo
    ):

        nonlocal game_over

        game_over = True

        if result == "X":

            status.config(
                text="🎉 You Win!"
            )

        elif result == "O":

            status.config(
                text="loser ^^"
            )

        else:

            status.config(
                text="It's a Tie!"
            )

        blink_winner_cells(
            combo
        )

   
    # AI move
   

    def ai_move():

        nonlocal game_over

        if game_over:
            return

        empty = [
            i for i in range(9)
            if board[i] == ""
        ]

        if not empty:
            return

        level = difficulty.get()

        if level == "Easy":

            move = random.choice(
                empty
            )

        elif level == "Medium":

            if random.random() < 0.45:

                move = random.choice(
                    empty
                )

            else:

                move = best_move()

        else:

            move = best_move()

        board[move] = "O"

        buttons[move].config(
            text="O",
            fg=DARK_GRAY
        )

        result, combo = check_winner(
            board
        )

        if result:

            finish_game(
                result,
                combo
            )

        else:

            status.config(
                text="Player's Turn"
            )


    # player move
   

    def player_move(index):

        if game_over:
            return

        if board[index] != "":
            return

        board[index] = "X"

        buttons[index].config(
            text="X",
            fg=DARK_PINK
        )

        result, combo = check_winner(
            board
        )

        if result:

            finish_game(
                result,
                combo
            )

            return

        status.config(
            text="AI's Turn"
        )

        root.after(
            400,
            ai_move
        )

  
    # Create buttons for the Tic Tac Toe board
    

    for i in range(9):

        btn = tk.Button(
            board_frame,
            text="",
            font=("Helvetica", 22, "bold"),
            width=5,
            height=2,
            bg=LIGHT_PURPLE,
            fg=DARK_PINK,
            activebackground=PINK,
            bd=2,
            relief="ridge",
            command=lambda i=i:
            player_move(i)
        )

        btn.grid(
            row=i // 3,
            column=i % 3,
            padx=4,
            pady=4
        )

        buttons.append(btn)

    
    #restart game
    

    def restart():

        nonlocal game_over

        game_over = False

        for i in range(9):

            board[i] = ""

            buttons[i].config(
                text="",
                bg=LIGHT_PURPLE
            )

        status.config(
            text="Player's Turn"
        )

    restart_button = tk.Button(
        root,
        text="Restart",
        font=("Helvetica", 12),
        bg=DARK_PINK,
        fg="white",
        activebackground=DARKER_PINK,
        activeforeground="white",
        width=20,
        height=2,
        bd=0,
        command=restart
    )
    restart_button.pack(
        pady=(15, 8)
    )

    home_button = tk.Button(
        root,
        text="Home",
        font=("Helvetica", 11),
        bg=PINK,
        fg="white",
        activebackground=ACTIVE_PINK,
        activeforeground="white",
        width=20,
        height=2,
        bd=0,
        command=home_page
    )
    home_button.pack()



# CONNECT 4


def connect_four():

    clear_screen()

    root.geometry("520x700")

    PLAYER = 1
    AI = 2
    EMPTY = 0

    ROWS = 6
    COLUMNS = 7

    board = [
        [EMPTY for _ in range(COLUMNS)]
        for _ in range(ROWS)
    ]

    buttons = []
    cells = []

    game_over = False

   
    # Check winner
    

    def check_winner(
        board,
        player
    ):

        # Horizontal
        for r in range(ROWS):

            for c in range(
                COLUMNS - 3
            ):

                if all(
                    board[r][c + i]
                    == player
                    for i in range(4)
                ):
                    return True

        # Vertical
        for r in range(
            ROWS - 3
        ):

            for c in range(
                COLUMNS
            ):

                if all(
                    board[r + i][c]
                    == player
                    for i in range(4)
                ):
                    return True

        # Diagonal down
        for r in range(
            ROWS - 3
        ):

            for c in range(
                COLUMNS - 3
            ):

                if all(
                    board[r + i][c + i]
                    == player
                    for i in range(4)
                ):
                    return True

        # Diagonal up
        for r in range(
            3,
            ROWS
        ):

            for c in range(
                COLUMNS - 3
            ):

                if all(
                    board[r - i][c + i]
                    == player
                    for i in range(4)
                ):
                    return True

        return False

  
    # full board check
    

    def is_full(board):

        return all(
            board[0][c] != EMPTY
            for c in range(COLUMNS)
        )

    # -----------------------------------------------------
    # EVALUATE
    # -----------------------------------------------------

    def evaluate(board):

        if check_winner(
            board,
            AI
        ):
            return 100

        if check_winner(
            board,
            PLAYER
        ):
            return -100

        return 0

    # -----------------------------------------------------
    # MINIMAX
    # -----------------------------------------------------

    def minimax(
        board,
        depth,
        alpha,
        beta,
        maximizing
    ):

        score = evaluate(
            board
        )

        if (
            depth == 0
            or score != 0
            or is_full(board)
        ):
            return score

        if maximizing:

            max_eval = -math.inf

            for col in range(
                COLUMNS
            ):

                if board[0][col] == EMPTY:

                    for row in range(
                        ROWS - 1,
                        -1,
                        -1
                    ):

                        if board[row][col] == EMPTY:

                            board[row][col] = AI

                            eval_score = minimax(
                                board,
                                depth - 1,
                                alpha,
                                beta,
                                False
                            )

                            board[row][col] = EMPTY

                            max_eval = max(
                                max_eval,
                                eval_score
                            )

                            alpha = max(
                                alpha,
                                eval_score
                            )

                            break

                if beta <= alpha:
                    break

            return max_eval

        else:

            min_eval = math.inf

            for col in range(
                COLUMNS
            ):

                if board[0][col] == EMPTY:

                    for row in range(
                        ROWS - 1,
                        -1,
                        -1
                    ):

                        if board[row][col] == EMPTY:

                            board[row][col] = PLAYER

                            eval_score = minimax(
                                board,
                                depth - 1,
                                alpha,
                                beta,
                                True
                            )

                            board[row][col] = EMPTY

                            min_eval = min(
                                min_eval,
                                eval_score
                            )

                            beta = min(
                                beta,
                                eval_score
                            )

                            break

                if beta <= alpha:
                    break

            return min_eval

    # -----------------------------------------------------
    # AI MOVE
    # -----------------------------------------------------

    def ai_move():

        nonlocal game_over

        if game_over:
            return

        best_score = -math.inf
        best_col = None

        for col in range(
            COLUMNS
        ):

            if board[0][col] == EMPTY:

                for row in range(
                    ROWS - 1,
                    -1,
                    -1
                ):

                    if board[row][col] == EMPTY:

                        board[row][col] = AI

                        score = minimax(
                            board,
                            4,
                            -math.inf,
                            math.inf,
                            False
                        )

                        board[row][col] = EMPTY

                        if score > best_score:

                            best_score = score
                            best_col = col

                        break

        if best_col is not None:

            drop_piece(
                best_col,
                AI
            )

    # -----------------------------------------------------
    # DROP PIECE
    # FULL COLORED SQUARE
    # -----------------------------------------------------

    def drop_piece(
        col,
        player
    ):

        nonlocal game_over

        target_row = None

        # Find final row
        for row in range(
            ROWS - 1,
            -1,
            -1
        ):

            if board[row][col] == EMPTY:

                target_row = row
                break

        if target_row is None:
            return

        # Start animation
        animate_piece(
            col,
            target_row,
            player,
            0
        )

    # -----------------------------------------------------
    # ANIMATE FALLING SQUARE
    # -----------------------------------------------------

    def animate_piece(
        col,
        target_row,
        player,
        current_row
    ):

        if game_over:
            return

        # Player color
        piece_color = (
            DARK_PINK
            if player == PLAYER
            else DARK_GRAY
        )

        # Clear temporary previous positions
        for r in range(ROWS):

            if (
                board[r][col]
                == EMPTY
                and r != current_row
            ):

                cells[r][col].config(
                    bg=LIGHT_PURPLE
                )

        # FULL CELL becomes colored
        cells[current_row][col].config(
            bg=piece_color
        )

        # Continue falling
        if current_row < target_row:

            root.after(
                80,
                lambda:
                move_piece(
                    col,
                    target_row,
                    player,
                    current_row
                )
            )

        else:

            # Final position
            board[target_row][col] = player

            cells[target_row][col].config(
                bg=piece_color
            )

            check_after_move(
                target_row,
                col,
                player
            )

  #Animation
    def move_piece(
        col,
        target_row,
        player,
        current_row
    ):

        # Clear current temporary position
        if board[current_row][col] == EMPTY:

            cells[current_row][col].config(
                bg=LIGHT_PURPLE
            )

        next_row = current_row + 1

        animate_piece(
            col,
            target_row,
            player,
            next_row
        )

    #check after move

    def check_after_move(
        row,
        col,
        player
    ):

        nonlocal game_over

        if check_winner(
            board,
            player
        ):

            game_over = True

            if player == PLAYER:

                status.config(
                    text="🎉 You Win!"
                )

            else:

                status.config(
                    text="loser ^^"
                )

            blink_winner_cells(
                row,
                col,
                player
            )

        elif is_full(board):

            game_over = True

            status.config(
                text="It's a Tie!"
            )

        else:

            if player == PLAYER:

                status.config(
                    text="AI's Turn"
                )

                root.after(
                    500,
                    ai_move
                )

            else:

                status.config(
                    text="Player's Turn"
                )

   #player move

    def player_move(col):

        if game_over:
            return

        if board[0][col] != EMPTY:
            return

        drop_piece(
            col,
            PLAYER
        )

   #blink winner

    def blink_winner_cells(
        row,
        col,
        player,
        count=0
    ):

        winning_cells = []

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dr, dc in directions:

            line = [
                (row, col)
            ]

            r = row + dr
            c = col + dc

            while (
                0 <= r < ROWS
                and
                0 <= c < COLUMNS
                and
                board[r][c] == player
            ):

                line.append(
                    (r, c)
                )

                r += dr
                c += dc

            r = row - dr
            c = col - dc

            while (
                0 <= r < ROWS
                and
                0 <= c < COLUMNS
                and
                board[r][c] == player
            ):

                line.append(
                    (r, c)
                )

                r -= dr
                c -= dc

            if len(line) >= 4:

                winning_cells = line
                break

        if not winning_cells:
            return

        if count >= 6:

            for r, c in winning_cells:

                cells[r][c].config(
                    bg=(
                        DARK_PINK
                        if player == PLAYER
                        else DARK_GRAY
                    )
                )

            return

        color = (
            LIGHT_PURPLE
            if count % 2 == 0
            else (
                DARK_PINK
                if player == PLAYER
                else DARK_GRAY
            )
        )

        for r, c in winning_cells:

            cells[r][c].config(
                bg=color
            )

        root.after(
            250,
            lambda:
            blink_winner_cells(
                row,
                col,
                player,
                count + 1
            )
        )

    #title

    title = tk.Label(
        root,
        text="💜 Connect 4 💜",
        font=("Helvetica", 24, "bold"),
        bg=PURPLE,
        fg=TEXT
    )
    title.pack(
        pady=(20, 10)
    )

    #colum botton

    button_frame = tk.Frame(
        root,
        bg=PURPLE
    )

    button_frame.pack()

    for c in range(COLUMNS):

        btn = tk.Button(
            button_frame,
            text="↓",
            font=("Helvetica", 14, "bold"),
            bg=PINK,
            fg="white",
            activebackground=ACTIVE_PINK,
            activeforeground="white",
            width=5,
            height=2,
            bd=0,
            command=lambda c=c:
            player_move(c)
        )

        btn.grid(
            row=0,
            column=c,
            padx=2,
            pady=5
        )

        buttons.append(btn)

    
    # Board
  

    board_frame = tk.Frame(
        root,
        bg=PURPLE
    )

    board_frame.pack()

    for r in range(ROWS):

        row_cells = []

        for c in range(COLUMNS):

            cell = tk.Label(
                board_frame,
                text="",
                width=5,
                height=2,
                bg=LIGHT_PURPLE,
                bd=2,
                relief="ridge",
                font=("Helvetica", 16)
            )

            cell.grid(
                row=r,
                column=c,
                padx=2,
                pady=2
            )

            row_cells.append(cell)

        cells.append(row_cells)

    
    # Status
    

    status = tk.Label(
        root,
        text="Player's Turn",
        font=("Helvetica", 13, "bold"),
        bg=PURPLE,
        fg="white"
    )

    status.pack(
        pady=10
    )

    
    # restart
   

    def restart():

        nonlocal game_over

        game_over = False

        for r in range(ROWS):

            for c in range(COLUMNS):

                board[r][c] = EMPTY

                cells[r][c].config(
                    bg=LIGHT_PURPLE
                )

        status.config(
            text="your turn"
        )

    restart_button = tk.Button(
        root,
        text="Restart",
        font=("Helvetica", 12),
        bg=DARK_PINK,
        fg="white",
        activebackground=DARKER_PINK,
        activeforeground="white",
        width=20,
        height=2,
        bd=0,
        command=restart
    )

    restart_button.pack(
        pady=(8, 5)
    )

    
    # home
    

    home_button = tk.Button(
        root,
        text="Home",
        font=("Helvetica", 11),
        bg=PINK,
        fg="white",
        activebackground=ACTIVE_PINK,
        activeforeground="white",
        width=20,
        height=2,
        bd=0,
        command=home_page
    )

    home_button.pack()



# start

home_page()

root.mainloop()