import numpy as np
import pygame
import sys
import random
import time 

class TicTacToe:
    def __init__(self):
        pygame.init()

        self.WIDTH = 600
        self.HEIGHT = 600
        self.LINE_WIDTH = 15
        self.WIN_LINE_WIDTH = 15
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.SQUARE_SIZE = 200
        self.CIRCLE_RADIUS = 60
        self.CIRCLE_WIDTH = 15
        self.CROSS_WIDTH = 25
        self.SPACE = 55

        self.RED = (255, 0, 0)
        self.BG_COLOR = (28, 170, 156)
        self.LINE_COLOR = (23, 145, 135)
        self.CIRCLE_COLOR = (239, 231, 200)
        self.CROSS_COLOR = (66, 66, 66)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('TIC TAC TOE')
        self.screen.fill(self.BG_COLOR)

        self.board = [[None for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]

        self.player = random.choice(["X", "O"])
        self.game_over = False
        self.winner= None
        self.draw_lines()
        self.q_table = {}

    def draw_lines(self):
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, self.SQUARE_SIZE), (self.WIDTH, self.SQUARE_SIZE), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0, 2 * self.SQUARE_SIZE), (self.WIDTH, 2 * self.SQUARE_SIZE), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (self.SQUARE_SIZE, 0), (self.SQUARE_SIZE, self.HEIGHT), self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (2 * self.SQUARE_SIZE, 0), (2 * self.SQUARE_SIZE, self.HEIGHT), self.LINE_WIDTH)

    def draw_figures(self):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == 'X':
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (col * self.SQUARE_SIZE + self.SPACE, row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE), (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE, row * self.SQUARE_SIZE + self.SPACE), self.CROSS_WIDTH)
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (col * self.SQUARE_SIZE + self.SPACE, row * self.SQUARE_SIZE + self.SPACE), (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE, row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE), self.CROSS_WIDTH)
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (int(col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), int(row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)), self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)

    def mark_square(self, row, col, player):
        self.board[row][col] = player

    def check_win(self, player):
        for col in range(self.BOARD_COLS):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                return True
        for row in range(self.BOARD_ROWS):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                return True
        if self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
            return True
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        return False

    def check_draw(self):
        if self.check_win('X') or self.check_win('O'):
            return False
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] is None:
                    return False
        return True

    def restart(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_lines()
        self.player = "X"
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                self.board[row][col] = None

    def display_winner(self, player):
        font = pygame.font.Font(None, 50)
        if player == 'X':
            text = font.render('Player X wins!', True, (0, 255, 0))
            print("Player X wins!")
            self.winner = 'X'
        else:
            text = font.render('Player O wins!', True, (0, 255, 0))
            print("Player O wins!")
            self.winner = 'O'
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update() 
        time.sleep(0.5)


    def ai_move(self):
        # Check for winning move
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] is None:
                    self.board[row][col] = 'O'
                    if self.check_win('O'):
                        return
                    self.board[row][col] = None

        # Check for blocking move
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] is None:
                    self.board[row][col] = 'X'
                    if self.check_win('X'):
                        self.board[row][col] = 'O'
                        return
                    self.board[row][col] = None

        # Make a random move
        while True:
            row = random.randint(0, self.BOARD_ROWS - 1)
            col = random.randint(0, self.BOARD_COLS - 1)
            if self.board[row][col] is None:
                self.board[row][col] = 'O'
                return


    def minimax(self, depth, is_maximizing):
        if self.check_win('O'):
            return {'score': 1, 'row': None, 'col': None}
            
        elif self.check_win('X'):
            return {'score': -1, 'row': None, 'col': None}
        elif self.check_draw():
            return {'score': 0, 'row': None, 'col': None}

        if is_maximizing:
            best_score = {'score': -float('inf'), 'row': None, 'col': None}
            symbol = 'O'
        else:
            best_score = {'score': float('inf'), 'row': None, 'col': None}
            symbol = 'X'

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] is None:
                    self.board[row][col] = symbol
                    current_score = self.minimax(depth + 1, not is_maximizing)
                    self.board[row][col] = None
                    current_score['row'] = row
                    current_score['col'] = col

                    if is_maximizing and current_score['score'] > best_score['score']:
                        best_score = current_score
                    elif not is_maximizing and current_score['score'] < best_score['score']:
                        best_score = current_score

        return best_score
        
    def get_state(self):
        return ''.join(str(e) if e is not None else '0' for row in self.board for e in row)
    
    def q_learning(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        state = self.get_state()
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.BOARD_ROWS * self.BOARD_COLS)

        q_values = self.q_table[state]

        if np.random.uniform(0, 1) < epsilon:
            # Explore: select a random action
            while True:
                action = np.random.randint(0, self.BOARD_ROWS * self.BOARD_COLS)
                row = action // self.BOARD_COLS
                col = action % self.BOARD_COLS
                if self.board[row][col] is None:
                    break
        else:
            # Exploit: select the action with max value (future reward)
            while True:
                indices = np.where(q_values == np.max(q_values))[0]
                action = np.random.choice(indices)
                row = action // self.BOARD_COLS
                col = action % self.BOARD_COLS
                if self.board[row][col] is None:
                    break

        # Perform the action and get the reward
        self.board[row][col] = 'O'
        reward = 0
        if self.check_win('O'):
            reward = 1
        elif self.check_draw():
            reward = 0
        else:
            reward = -0.01

        # Update Q-table for Q(s, a)
        next_state = self.get_state()
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.BOARD_ROWS * self.BOARD_COLS)

        next_q_values = self.q_table[next_state]
        max_next_q_value = np.max(next_q_values)

        q_values[action] = q_values[action] + alpha * (reward + gamma * max_next_q_value - q_values[action])

        return row, col

    
    def minimax_alpha_beta(self, depth, is_maximizing, alpha, beta):
        if self.check_win('O'):
            return {'score': 1, 'row': None, 'col': None}
        elif self.check_win('X'):
            return {'score': -1, 'row': None, 'col': None}
        elif self.check_draw():
            return {'score': 0, 'row': None, 'col': None}

        if is_maximizing:
            best_score = {'score': -float('inf'), 'row': None, 'col': None}
            symbol = 'O'
        else:
            best_score = {'score': float('inf'), 'row': None, 'col': None}
            symbol = 'X'

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] is None:
                    self.board[row][col] = symbol
                    current_score = self.minimax_alpha_beta(depth + 1, not is_maximizing, alpha, beta)
                    self.board[row][col] = None
                    current_score['row'] = row
                    current_score['col'] = col

                    if is_maximizing:
                        if current_score['score'] > best_score['score']:
                            best_score = current_score
                        alpha = max(alpha, best_score['score'])
                        if beta <= alpha:
                            return best_score
                    else:
                        if current_score['score'] < best_score['score']:
                            best_score = current_score
                        beta = min(beta, best_score['score'])
                        if beta <= alpha:
                            return best_score

        return best_score

    def game_loop(self):
        while True:
            # for event in pygame.event.get():
                # if event.type == pygame.QUIT:
                #     sys.exit()
            #     # ==================
            # if self.player == 'O' and not self.game_over:
            #     self.ai_move()
            #     if self.check_win(self.player):
            #         self.game_over = True
            #         self.draw_figures()
            #         self.display_winner(self.player)
            #         break
            #     self.player = 'X'
            #     self.draw_figures()
            # pygame.display.update()
                #    ===================================================         # 
            # if self.player == 'X' and not self.game_over:
            #     move = self.minimax(0, False)
            #     if move['row'] is not None and move['col'] is not None:
            #         self.board[move['row']][move['col']] = 'X'
            #     if self.check_win(self.player):
            #         self.game_over = True
            #         self.draw_figures()
            #         self.display_winner(self.player)
            #         break
            #     self.player = 'O'
            #     self.draw_figures()
            # pygame.display.update() 


            if self.player == 'O' and not self.game_over:
                row, col = self.q_learning()
                if self.check_win(self.player):
                    self.game_over = True
                    self.draw_figures()
                    self.display_winner(self.player)
                    break
                self.player = 'X'
                self.draw_figures()   
            pygame.display.update() 
            time.sleep(0.5)

            if self.player == 'X' and not self.game_over:
                move = self.minimax_alpha_beta(0, True, -float('inf'), float('inf'))
                if move['row'] is not None and move['col'] is not None:
                    self.board[move['row']][move['col']] = 'X'
                if self.check_win(self.player):
                    self.game_over = True
                    self.draw_figures()
                    self.display_winner(self.player)
                    break
                self.player = 'O'
                self.draw_figures()
            pygame.display.update()
            time.sleep(0.5)

                # if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                #     mouseX = event.pos[0]
                #     mouseY = event.pos[1]
                #     clicked_row = int(mouseY // self.SQUARE_SIZE)
                #     clicked_col = int(mouseX // self.SQUARE_SIZE)

                #     if self.board[clicked_row][clicked_col] is None:
                #         if self.player == 'X':
                #             self.mark_square(clicked_row, clicked_col, 'X')
                #             if self.check_win(self.player):
                #                 self.game_over = True
                #                 self.draw_figures()
                #                 self.display_winner(self.player)
                #                 break
                #             self.player = 'O'
                #         elif self.player == 'O':
                #             self.mark_square(clicked_row, clicked_col, 'O')
                #             if self.check_win(self.player):
                #                 self.game_over = True
                #                 self.draw_figures()
                #                 self.display_winner(self.player)
                #                 break
                #             self.player = 'X'
                #         self.draw_figures()

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_r:
                #         self.restart()
                #         self.game_over = False

            if self.check_draw():
                font = pygame.font.Font(None, 50)
                text = font.render('Draw!', True, (0, 255, 0))
                self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))
                break

            if self.game_over:
                self.display_winner(self.player)
                time.sleep(3)
                break

            pygame.display.update()
            time.sleep(0.5)
        return self.winner

if __name__ == "__main__":
    winner = []
    for _ in range(5):
        # TicTacToe().game_loop()
        winner.append(TicTacToe().game_loop())

    print(winner)