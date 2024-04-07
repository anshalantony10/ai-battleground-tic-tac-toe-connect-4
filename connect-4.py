import pygame
import sys
import numpy as np
import math
import random

class ConnectFour:
    def __init__(self):
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7

        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0, 0, 0)

        self.SQUARESIZE = 100
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)

        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.board = self.create_board()
        self.game_over = False
        self.turn = 0
        self.draw_board(self.board)
        pygame.display.update()

    def create_board(self):
        board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()

    def get_valid_columns(self, board):
        valid_columns = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_columns.append(col)
        return valid_columns

    def evaluate_board(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative sloped diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = 1
        if piece == 1:
            opponent_piece = 2
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2
        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.game_over:
            if self.game_over:
                if self.winning_move(board, 2):
                    return (None, 100000000000000)
                elif self.winning_move(board, 1):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.evaluate_board(board, 2))

        if maximizing_player:
            value = -math.inf
            column = random.choice(self.get_valid_columns(board))
            for col in self.get_valid_columns(board):
                row = self.get_next_open_row(board, col)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, col, 2)
                new_score = self.minimax(temp_board, depth - 1, False, alpha, beta)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:  # Minimizing player
            value = math.inf
            column = random.choice(self.get_valid_columns(board))
            for col in self.get_valid_columns(board):
                row = self.get_next_open_row(board, col)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, col, 1)
                new_score = self.minimax(temp_board, depth - 1, True, alpha, beta)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
        
    def get_best_move(self, board, piece):
        for col in range(self.COLUMN_COUNT):
            temp_board = board.copy()
            if self.is_valid_location(temp_board, col):
                row = self.get_next_open_row(temp_board, col)
                self.drop_piece(temp_board, row, col, piece)
                if self.winning_move(temp_board, piece):
                    return col

        for col in range(self.COLUMN_COUNT):
            temp_board = board.copy()
            if self.is_valid_location(temp_board, col):
                row = self.get_next_open_row(temp_board, col)
                self.drop_piece(temp_board, row, col, 3 - piece)
                if self.winning_move(temp_board, 3 - piece):
                    return col

        while True:
            col = random.randint(0, self.COLUMN_COUNT - 1)
            if self.is_valid_location(board, col):
                return col
            
    def q_learning(game, num_iterations, learning_rate, discount_factor, exploration_rate, max_depth):
        # Initialize Q-table with zeros
        Q_table = np.zeros([game.state_space, game.action_space])

        for i in range(num_iterations):
            # Reset the game state
            state = game.reset()
            done = False
            depth = 0

            while not done and depth < max_depth:
                # Choose action: either explore or exploit
                if np.random.uniform(0, 1) < exploration_rate:
                    # Explore: select a random action
                    action = game.sample_action()
                else:
                    # Exploit: select the action with max value (greedy policy)
                    action = np.argmax(Q_table[state, :])

                # Perform the action and get the new state and reward
                new_state, reward, done = game.step(action)

                # Update Q-table
                Q_table[state, action] = Q_table[state, action] + learning_rate * (reward + discount_factor * np.max(Q_table[new_state, :]) - Q_table[state, action])

                # Update the current state
                state = new_state
                depth += 1

        return Q_table

    def play(self):
        while not self.game_over:
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()

            #     if event.type == pygame.MOUSEMOTION:
            #         pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
            #         posx = event.pos[0]
            #         if self.turn == 0:
            #             pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
            #         else:
            #             pygame.draw.circle(self.screen, self.YELLOW, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
            #         pygame.display.update()

            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))

                    # Player 1's move
                    if self.turn == 0:
                        # posx = event.pos[0]
                        # col = int(math.floor(posx / self.SQUARESIZE))
                        col = self.get_best_move(self.board, 2)

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, 1)

                            if self.winning_move(self.board, 1):
                                self.game_over = True
                                self.draw_board(self.board)
                                self.show_message("Player 1 wins!!", self.RED)
                                pygame.time.wait(3000)
                                pygame.quit()
                                sys.exit()

                    # Player 2's move
                    else:
                        col, _ = self.minimax(self.board, 4, True, -math.inf, math.inf)

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, 2)

                            if self.winning_move(self.board, 2):
                                self.game_over = True
                                self.draw_board(self.board)
                                self.show_message("Player 2 wins!!", self.YELLOW)
                                pygame.time.wait(3000)
                                pygame.quit()
                                sys.exit()

                    self.draw_board(self.board)
                    self.turn += 1
                    self.turn = self.turn % 2

                    if self.turn == 1:
                        pygame.time.wait(500)
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))

                    if self.game_over:
                        pygame.time.wait(3000)
                        pygame.quit()
                        sys.exit()

    def show_message(self, message, color):
        label = self.myfont.render(message, 1, color)
        self.screen.blit(label, (40, 10))
        pygame.display.update()

if __name__ == "__main__":
    game = ConnectFour()
    game.play()