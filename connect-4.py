import pygame
import sys
import numpy as np
import math
import random


class ConnectFour:
    def __init__(self):
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7

        self.BLUE = (0,0,255)
        self.RED = (255,0,0)
        self.YELLOW = (255,255,0)
        self.BLACK = (0,0,0)

        self.SQUARESIZE = 100
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT+1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.RADIUS = int(self.SQUARESIZE/2 - 5)

        self.screen = pygame.display.set_mode(self.size)
       
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.board = self.create_board()
        self.game_over = False
        self.turn = 0
        self.draw_board(self.board)
        pygame.display.update()

    def create_board(self):
        board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[self.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):        
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board[r][c] == 2: 
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()

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
            
    
    
    def play(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BLACK, (0,0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == 0:
                        pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                    else: 
                        pygame.draw.circle(self.screen, self.YELLOW, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.BLACK, (0,0, self.width, self.SQUARESIZE))

                    # Ask for Player 1 Input
                    if self.turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, 1)

                            if self.winning_move(self.board, 1):
                                label = self.myfont.render("Player 1 wins!!", 1, self.RED)
                                self.screen.blit(label, (40,10))
                                self.game_over = True

                    # Ask for Player 2 Input
                    else:               
                        col = self.get_best_move(self.board, 2)

                        if self.is_valid_location(self.board, col):
                            row = self.get_next_open_row(self.board, col)
                            self.drop_piece(self.board, row, col, 2)

                            if self.winning_move(self.board, 2):
                                label = self.myfont.render("Player 2 wins!!", 1, self.YELLOW)
                                self.screen.blit(label, (40,10))
                                self.game_over = True

                    self.draw_board(self.board)

                    self.turn += 1
                    self.turn = self.turn % 2

                    if self.game_over:
                        pygame.time.wait(3000)

if __name__ == "__main__":
    game = ConnectFour()
    game.play()