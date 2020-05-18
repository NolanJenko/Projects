import pygame
import math
import numpy as np
import random


pygame.init()
screen = pygame.display.set_mode((800, 800))


class Board:
    def __init__(self):
        self.board = np.full((8,8), None)
        self.white = []
        self.black = []
        self.recent_move = {}

    def add_piece(self, piece, pos):
        self.board[pos[1]][pos[0]] = piece
        piece.change_pos(pos)
        if piece.color:
            self.white += [piece]
        else:
            self.black += [piece]

    def piece_by_pos(self, pos):
        return self.board[pos[1]][pos[0]]

    def create(self, color):
        side = 0
        if color:
            side = 7
        self.add_piece(King(color), [4, side])
        for i in range(8):
            if not color:
                self.add_piece(Pawn(color), [i, side+1])
            else:
                self.add_piece(Pawn(color), [i, side - 1])
            if i == 0 or i == 7:
                self.add_piece(Rook(color), [i, side])
            if i == 1 or i == 6:
                self.add_piece(Knight(color), [i, side])
            if i == 2 or i == 5:
                self.add_piece(Bishop(color), [i, side])

        self.add_piece(Queen(color), [3, side])

    def change(self, old, new):
        self.recent_move = {}
        new_pos = self.board[new[1]][new[0]]
        old_pos = self.board[old[1]][old[0]]
        if new_pos is not None:
            if new_pos.color is True:
                self.white.remove(new_pos)
            else:
                self.black.remove(new_pos)
        self.previous_move(new_pos, new, old_pos, old)
        self.board[new[1]][new[0]] = self.board[old[1]][old[0]]
        self.board[new[1]][new[0]].change_pos(new)
        self.board[old[1]][old[0]] = None

    def previous_move(self, new, new_pos, old, old_pos):
        if new is not None:
            self.recent_move[new] = new.position
        else:
            self.recent_move[new] = new_pos
        if old is not None:
            self.recent_move[old] = old.position
        else:
            self.recent_move[old] = old_pos

    def is_check(self, player):
        if player:
            opp = self.black
            side = self.white
        else:
            opp = self.white
            side = self.black
        enemies = []
        for pieces in opp:
            enemies = pieces.generate_moves(self)
            if side[0].get_position() in enemies:
                return True
        else:
            return False

    def checkmate(self, player):
        if player:
            opp = self.black
            side = self.white
        else:
            opp = self.white
            side = self.black
        king = side[0]
        orig  = king.position
        vals = []
        for moves in king.generate_moves(self):
            prev = self.piece_by_pos(moves)
            self.change(king.position, moves)
            vals += [self.is_check(player)]
            self.change(moves, orig)
            if prev is not None:
                self.add_piece(prev, moves)
        for allies in side:
            allies_moves = allies.generate_moves(self)
            for i in allies_moves:
                self.change(allies.position, i)
                vals+= [self.is_check(player)]
                print(vals)
                self.undo()

        if all(vals) and vals != []:
            return True
        return False

    def undo(self):
        old_pos = list(self.recent_move.keys())[1]
        new_pos = list(self.recent_move.keys())[0]
        new_other = self.recent_move[new_pos]
        self.change(self.recent_move[new_pos], self.recent_move[old_pos])
        if new_pos is not None:
            self.add_piece(new_pos, new_other)


    def is_turn(self, player, piece):
        if player is piece.color:
            return True
        else:
            return False

    def get_all_moves(self):
        all_moves = []
        for i in self.black:
            all_moves += i.generate_moves(self)
        return all_moves

    def pawn_promotion(self, player):
        if player:
            for i in self.white:
                if isinstance(i, Pawn):
                    if i.get_position()[1] == 0:
                        self.add_piece(Queen(True), i.get_position())
                        self.white.remove(i)
        else:
            for i in self.black:
                if isinstance(i, Pawn):
                    if i.get_position()[1] == 7:
                        self.add_piece(Queen(False), i.get_position())
                        self.black.remove(i)


class Piece:
    def __init__(self, color):
        self.color = color
        self.position = []

    def change_pos(self, new_pos):
        self.position = new_pos

    def get_position(self):
        return self.position

    def vert(self,board, pos, i, j):
        possible = []
        z = pos[1]
        d = pos[0]
        for s in range(1,8):
            if i == 1:
                z += j
            if i == -1:
                d += j

            if z > 7 or z <0 or d > 7 or d <0:
                break
            hori = board.piece_by_pos([d,z])
            if hori is not None:
                if hori.color != self.color:
                    possible.append([d, z])
                break
            else:
                possible.append([d, z])
        return possible

    def vertical_movement(self, board, pos):
        possible_moves = []
        for i in [1, -1]:
            for j in [1, -1]:
                possible_moves+=self.vert(board, pos, i, j)
        return possible_moves

    def diagonal_helper(self, board, pos, i, j):
        possible = []
        x = pos[0]
        y = pos[1]
        for t in range(1, 8):
            y += j
            x += i
            if x > 7 or y > 7 or x < 0 or y < 0:
                break
            diag = board.piece_by_pos([x, y])

            if diag is not None:
                if diag.color != self.color:
                    possible.append([x, y])
                break
            else:
                possible.append([x, y])
        return possible

    def diagonal(self, board, pos):
        possible_moves = []
        for i in [1, -1]:
            for j in [1, -1]:
                possible_moves+=self.diagonal_helper(board, pos, i, j)
        return possible_moves

    def generate_moves(self, board):
        return self.is_valid(board, self.position)

    def is_valid(self, board, pos):
        return []


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color is True:
            w_king = pygame.image.load('white_king.png').convert_alpha()
            self.w_king = pygame.transform.scale(w_king, (100, 100))
        else:
            w_king = pygame.image.load('black_king.png').convert_alpha()
            self.w_king = pygame.transform.scale(w_king, (100, 100))

    def image(self):
        return self.w_king

    def is_valid(self, board, pos):
        lst = [-1,1,0]
        possible = []
        for i in lst:
            for j in lst:
                if (8>pos[0]+i>-1) and (8>pos[1]+j>-1):
                    pie = board.piece_by_pos([pos[0] + i, pos[1] + j])
                    if pie is not None:
                        if pie.color != self.color:
                            possible.append([pos[0]+i, pos[1]+j])
                    else:
                        possible.append([pos[0]+i, pos[1]+j])
        return possible


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color is True:
            w_queen = pygame.image.load('white_queen.png').convert_alpha()
            self.queen = pygame.transform.scale(w_queen, (100, 100))
        else:
            b_queen = pygame.image.load('black_queen.png').convert_alpha()
            self.queen = pygame.transform.scale(b_queen, (100, 100))

    def image(self):
        return self.queen

    def is_valid(self, board, pos):
        moves = self.vertical_movement(board, pos)
        moves += self.diagonal(board, pos)
        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

        if self.color is True:
            w_rook = pygame.image.load('white_rook.png').convert_alpha()
            self.rook = pygame.transform.scale(w_rook, (100, 100))
        else:
            w_rook = pygame.image.load('black_rook.png').convert_alpha()
            self.rook = pygame.transform.scale(w_rook, (100, 100))

    def image(self):
        return self.rook

    def is_valid(self, board, pos):
        return self.vertical_movement(board, pos)


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        if color is True:
            w_bishop = pygame.image.load('white_bishop.png').convert_alpha()
            self.w_bishop = pygame.transform.scale(w_bishop, (100, 100))
        else:
            w_bishop = pygame.image.load('black_bishop.png').convert_alpha()
            self.w_bishop = pygame.transform.scale(w_bishop, (100, 100))

    def image(self):
        return self.w_bishop

    def is_valid(self, board, pos):
        return self.diagonal(board, pos)


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        if color is True:
            w_knight = pygame.image.load('white_knight.png').convert_alpha()
            self.w_knight = pygame.transform.scale(w_knight, (100, 100))
        else:
            w_knight = pygame.image.load('black_knight.png').convert_alpha()
            self.w_knight = pygame.transform.scale(w_knight, (100, 100))

    def image(self):
        return self.w_knight

    def is_valid(self, board, pos):
        possible_moves = []
        X = [2, 1, -1, -2, -2, -1, 1, 2]
        Y = [1, 2, 2, 1, -1, -2, -2, -1]
        for i in range(8):
            x = pos[0] + X[i]
            y = pos[1] + Y[i]
            if (7 >= x >= 0) and (0 <= y <= 7):
                if board.piece_by_pos([x, y]) is not None:
                    if self.color != board.piece_by_pos([x, y]).color:
                        possible_moves.append([x, y])
                else:
                    possible_moves.append([x, y])
        return possible_moves


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.num = 0
        if color is True:
            w_pawn = pygame.image.load('white_pawn.png').convert_alpha()
            self.w_pawn = pygame.transform.scale(w_pawn, (100, 100))
        else:
            w_pawn = pygame.image.load('black_pawn.png').convert_alpha()
            self.w_pawn = pygame.transform.scale(w_pawn, (100, 100))

    def image(self):
        return self.w_pawn

    def is_valid(self, board, pos):
        possible = []
        vert = 1
        if self.color:
            vert = -1
        if 0<pos[0]<7:
            left = board.piece_by_pos([pos[0]-1, pos[1]+vert])
            right = board.piece_by_pos([pos[0]+1, pos[1]+vert])
            if left is not None:
                if left.color != self.color:
                    possible.append([pos[0]-1, pos[1]+vert])
            if right is not None:
                if right.color != self.color:
                    possible.append([pos[0]+1, pos[1]+vert])
        if board.piece_by_pos([pos[0],pos[1]+vert]) is None:
            possible.append([pos[0], pos[1]+vert])
            if self.num == 0:
                possible.append([pos[0], pos[1] + 2*vert])
        self.num+=1

        return possible




class Players:
    def __init__(self, type):
        self.type = type
        if type:
            self.turn = 1
        else:
            self.turn = 2

    def is_turn(self, board, selected):
        if selected is self.type:
            return True
        else:
            return False




class main:
    def __init__(self):
        self.Board = Board()
        self.position = []
        self.valid = []
        self.player = True
        self.Board.create(True)
        self.Board.create(False)
        self.checkmate = False
        self.loop()

    def row_column(self, pos):
        column = math.floor(pos[0]/100)
        row = math.floor(pos[1]/100)
        return [column, row]

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def draw(self):
        util =0
        highlight_moves = None
        for i in range(8):
            util +=1
            for j in range(8):
                pi = self.Board.piece_by_pos([i,j])
                if util % 2:
                    pygame.draw.rect(screen, (255, 255, 255), (i * 100, j * 100, 100, 100))
                else:
                    pygame.draw.rect(screen, (52, 152, 0), (i * 100, j*100, 100, 100))
                if pi is not None:
                    if [i, j] == self.position and pi.color is self.player:
                        highlight_moves = pi
                        pygame.draw.rect(screen, (52, 250, 0), (self.position[0] * 100, self.position[1] * 100, 100, 100))
                    screen.blit(pi.image(), (i * 100, j * 100))
                if self.checkmate:
                    text = "Checkmate"
                    largeText = pygame.font.Font('freesansbold.ttf', 115)
                    TextSurf, TextRect = self.text_objects(text, largeText)
                    TextRect.center = ((800 / 2), (800 / 2))
                    screen.blit(TextSurf, TextRect)
                util += 1
        if highlight_moves is not None:
            for t in highlight_moves.generate_moves(self.Board):
                pygame.draw.rect(screen, (52, 250, 0), (t[0] * 100 + 45, t[1] * 100 + 45, 10, 10))

    def check_for_check(self, pos):
        if self.Board.is_check(not self.player):
            self.Board.undo()
            if self.Board.checkmate(not self.player):
                print('aight')
                self.checkmate = True
            self.player = not self.player

    def loop(self):
        running = True
        prev = None
        pos = []
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.position = self.row_column(pygame.mouse.get_pos())
                    pos += [self.position]
                    if len(pos) == 2:
                        piece = self.Board.piece_by_pos(pos[0])
                        if piece is not None:
                            valid = piece.is_valid(self.Board, pos[0])
                            if pos[1] in valid and self.Board.is_turn(self.player, piece):
                                self.Board.change(pos[0],pos[1])
                            else:
                                pos = []
                                break
                            self.Board.pawn_promotion(self.player)
                            self.player = not self.player


                            pos = []
                        else:
                            pos = []
            self.check_for_check(self.player)

            self.draw()
            pygame.display.update()

main()

