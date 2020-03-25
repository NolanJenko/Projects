import pygame
import math


screen = pygame.display.set_mode((600, 600))

class Space:
    def __init__(self, color):

        self.color = color
        self.piece = None


    def add_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece



class Board:
    def __init__(self):
        self.board = [[] for x in range(8)]
        self.turn = 2
        self.possible = []
        self.black_k = [4, 0]
        self.white_k = [4, 7]

    def create_board(self):
        for i in range(8):
            for j in range(8):
                if (i % 2) == 0:
                    if(j % 2) == 0:
                        self.board[j] += [Space('white')]
                    else:
                        self.board[j] += [Space('black')]

                else:
                    if (j % 2) != 0:
                        self.board[j] += [Space('white')]
                    else:
                        self.board[j] += [Space('black')]

        for i in range(8):
            self.board[1][i].add_piece(Pawn(True))
            self.board[6][i].add_piece(Pawn(False))
            if i == 0 or i == 7:
                self.board[0][i].add_piece(Rook(True))
                self.board[7][i].add_piece(Rook(False))
            elif i == 1 or i == 6:
                self.board[0][i].add_piece(Knight(True))
                self.board[7][i].add_piece(Knight(False))
            elif i == 2 or i == 5:
                self.board[0][i].add_piece(Bishop(True))
                self.board[7][i].add_piece(Bishop(False))
            elif i == 3:
                self.board[0][i].add_piece(Queen(True))
                self.board[7][i].add_piece(Queen(False))
            elif i == 4:
                self.board[0][i].add_piece(King(True))
                self.board[7][i].add_piece(King(False))

    def return_board(self):
        return self.board

    def row_column(self, pos):
        row  = math.floor(pos[0]/75)
        column = math.floor(pos[1]/75)
        return [row, column]

    def piece_by(self,x, y):
        return self.board[x][y].get_piece()

    def king_pos(self, selection, new):
        if selection.color is False:
            self.white_k = new
        else:
            self.black_k = new

    def change(self, pos1, pos2):

        self.board[pos2[1]][pos2[0]].add_piece(self.board[pos1[1]][pos1[0]].get_piece())

        (self.board[pos1[1]][pos1[0]]).add_piece(None)
        self.turn += 1


    def is_turn(self, pos, turn):

        if (turn % 2 is 0) and self.piece_by(pos[1], pos[0]).color is False:
            return True
        elif turn % 2 == 1 and self.piece_by(pos[1], pos[0]).color is True:
            return True
        else:
            return False

    def checka(self, board, turn):
        if turn % 2 == 0:
            king = self.piece_by(self.white_k[1], self.white_k[0])
            if king.check(board, None, self.white_k):
                return True
        elif turn % 2 == 1:
            king = self.piece_by(self.black_k[1], self.black_k[0])
            if king.check(board, None, self.black_k):
                return True

        return False


class Piece:
    def __init__(self, color):
        self.white = color

    def is_white(self):
        return self.white


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.color = color
        if color is False:
            w_king = pygame.image.load('white_king.png').convert_alpha()
            self.w_king = pygame.transform.scale(w_king, (75, 75))
        else:
            w_king = pygame.image.load('black_king.png').convert_alpha()
            self.w_king = pygame.transform.scale(w_king, (75, 75))

    def image(self):
        return self.w_king

    def check(self, board, pos, new):
        all = []
        for i in range(8):
            for j in range(8):
                piec = board.piece_by(i,j)
                if piec is not None:
                    if piec.color != self.color:
                        all+=piec.is_valid(board,[j,i])
        if new in all:
            return True
        return False



    def is_valid(self, board, pos):
        n = board.piece_by(pos[1], pos[0])
        return [0,0]

    def move(self, board, pos, new):
        distance = math.sqrt((pos[1]-new[1])**2 + (pos[0]- new[0])**2)
        if distance <= math.sqrt(2) and not self.check(board, pos, new):
            board.change(pos, new)
            board.king_pos(self, new)


class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.color = color
        if color is False:
            w_queen = pygame.image.load('white_queen.png').convert_alpha()
            self.queen = pygame.transform.scale(w_queen, (75, 75))
        else:
            b_queen = pygame.image.load('black_queen.png').convert_alpha()
            self.queen = pygame.transform.scale(b_queen, (75, 75))

    def image(self):
        return self.queen

    def direct(self, board, pos, i, j):
        possible = []
        x = pos[0]
        y = pos[1]
        z = pos[1]
        d = pos[0]
        for t in range(1, 8):
            y += i
            x += j
            if x > 7 or y > 7 or x<0 or y < 0:
                break
            diag = board.piece_by(y, x)

            if diag is not None:
                if diag.color != self.color:
                    possible.append([x, y])
                break
            else:
                possible.append([x, y])

        for s in range(1,8):
            if i == 1:
                z += j
            if i == -1:
                d += j

            if z > 7 or z <0 or d > 7 or d <0:
                break
            hori = board.piece_by(z,d)
            if hori is not None:
                if hori.color != self.color:
                    possible.append([d, z])
                break
            else:
                possible.append([d, z])
        return possible

    def is_valid(self, board, pos):
        possible_moves = []
        for i in [1, -1]:
            for j in [1, -1]:
                possible_moves+=self.direct(board, pos, i, j)
        return possible_moves

    def move(self, board, pos, new):
        if new in self.is_valid(board, pos):
            board.change(pos, new)



class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.color = color
        if self.color is False:
            w_rook = pygame.image.load('white_rook.png').convert_alpha()
            self.rook = pygame.transform.scale(w_rook, (75, 75))
        else:
            w_rook = pygame.image.load('black_rook.png').convert_alpha()
            self.rook = pygame.transform.scale(w_rook, (75, 75))

    def image(self):
        return self.rook


    def is_valid(self, board, pos):
        possible_moves = []
        maxx = 7 - pos[0]
        maxy = 7 - pos[1]
        for i in range(1, maxx+1):
            if board.piece_by(pos[1], pos[0]+i) is not None:
                if board.piece_by(pos[1], pos[0]+i).color != self.color:
                    possible_moves.append([pos[0] + i, pos[1]])
                break
            else:
                possible_moves.append([pos[0] + i, pos[1]])
        for i in range(1, pos[0]+1):
            if board.piece_by(pos[1], pos[0]-i) is not None:
                if board.piece_by(pos[1], pos[0]-i).color != self.color:
                    possible_moves.append([pos[0] - i, pos[1]])
                break
            else:
                possible_moves.append([pos[0] - i, pos[1]])
        for i in range(1, maxy+1):
            if board.piece_by(pos[1] +i, pos[0]) is not None:
                if board.piece_by(pos[1] +i, pos[0]).color != self.color:
                    possible_moves.append([pos[0], pos[1] + i])
                break
            else:
                possible_moves.append([pos[0], pos[1] + i])
        for i in range(1, pos[1]+1):
            if board.piece_by(pos[1] - i, pos[0]) is not None:
                if board.piece_by(pos[1] - i, pos[0]).color != self.color:
                    possible_moves.append([pos[0], pos[1] - i])
                break
            else:
                possible_moves.append([pos[0], pos[1]-i])
        return possible_moves

    def move(self, board, pos, new):
        if new in self.is_valid(board, pos):
            board.change(pos, new)


class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.color = color
        if color is False:
            w_bishop = pygame.image.load('white_bishop.png').convert_alpha()
            self.w_bishop = pygame.transform.scale(w_bishop, (75, 75))
        else:
            w_bishop = pygame.image.load('black_bishop.png').convert_alpha()
            self.w_bishop = pygame.transform.scale(w_bishop, (75, 75))

    def image(self):
        return self.w_bishop

    def direct(self, board, pos, i, j):
        possible = []
        x=pos[0]
        y=pos[1]
        for t in range(1, 7):
            y += i
            x += j
            if x >7 or y>7 or x<0 or y<0:
                break
            m = board.piece_by(y,x)
            if m is not None:
                if m.color != self.color:
                    possible.append([x, y])
                break
            else:
                possible.append([x, y])
        return possible


    def is_valid(self, board, pos):
        possible_moves = []
        for i in [1,-1]:
            for j in [1,-1]:
                possible_moves+= self.direct(board, pos, i, j)
        return possible_moves


    def move(self, board, pos, new):
        valid = self.is_valid(board,pos)
        if new in valid:
            board.change(pos, new)


class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.color = color
        if color is False:
            w_knight = pygame.image.load('white_knight.png').convert_alpha()
            self.w_knight = pygame.transform.scale(w_knight, (75, 75))
        else:
            w_knight = pygame.image.load('black_knight.png').convert_alpha()
            self.w_knight = pygame.transform.scale(w_knight, (75, 75))

    def image(self):
        return self.w_knight


    def is_valid(self, board, pos):
        possible_moves = []
        X = [2, 1, -1, -2, -2, -1, 1, 2]
        Y = [1, 2, 2, 1, -1, -2, -2, -1]
        for i in range(8):
            x = pos[0] +X[i]
            y = pos[1] +Y[i]
            if (7 >=x>=0) and (0<=y<=7):
                if board.piece_by(y, x) is not None:
                    if self.color != board.piece_by(y,x).color:
                        possible_moves.append([x, y])
                else:
                    possible_moves.append([x,y])
        return possible_moves

    def move(self, board, pos, new):
        valid = self.is_valid(board, pos)
        if new in valid:
            board.change(pos, new)


class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.color = color
        self.num = 0
        if color is False:
            w_pawn = pygame.image.load('white_pawn.png').convert_alpha()
            self.w_pawn = pygame.transform.scale(w_pawn, (75, 75))
        else:
            w_pawn = pygame.image.load('black_pawn.png').convert_alpha()
            self.w_pawn = pygame.transform.scale(w_pawn, (75, 75))

    def image(self):
        return self.w_pawn

    def is_valid(self, board, pos):
        n = board.piece_by(pos[1], pos[0])
        possible = []
        vert = 1
        if self.color == True:
            vert = -1

        for i in [1,-1]:
            if 0 <=(pos[1]-vert) <= 7 and 0 <= (pos[0]-i) <= 7:
                if board.piece_by(pos[1]-vert, pos[0]-i) is not None:
                    if board.piece_by(pos[1]-vert, pos[0]-i).color != self.color:
                        possible.append([pos[0]-i, pos[1]-vert])


        return possible

    def move(self,board, pos, new):
        valid = self.is_valid(board, pos)
        vert = 1
        if self.color == True:
            vert = -1
        if board.piece_by(pos[1]-vert, pos[0]) is None:
            valid.append([pos[0], pos[1] - vert])
            if self.num == 0:
                valid.append([pos[0], pos[1]-2*vert])
                self.num +=1

        if new in valid:
            board.change(pos, new)

class Player:
    def __init__(self, color):
        self.color = color
        if color is False:
            self.turn = 0
        else:
            self.turn = 1

    def moved(self):
        self.turn


class Main:
    def __init__(self):
        self.Board = Board()
        self.Board.create_board()
        self.board = self.Board.return_board()
        self.loop()

    def draw(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color == 'white':
                    pygame.draw.rect(screen, (255, 255, 255), (j * 75, i * 75, 75, 75))
                    if self.board[i][j].piece is not None:
                        screen.blit(self.Board.piece_by(i, j).image(), (j * 75, i * 75))
                else:
                    pygame.draw.rect(screen, (52, 152, 0), (j * 75, i*75, 75, 75))
                    if self.Board.piece_by(i,j) is not None:
                        screen.blit(self.Board.piece_by(i,j).image(), (j *75, i*75))


    def loop(self):
        pygame.init()


        WHITE=(255,255,255)
        pos = []
        turn =0
        Player1 = Player(False)
        Player2 = Player(True)
        screen.fill(WHITE)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    po = pygame.mouse.get_pos()
                    po = self.Board.row_column(po)
                    pos += [po]
                    if len(pos) == 2:
                        selected = self.Board.piece_by(pos[0][1], pos[0][0])
                        if selected is not None and self.Board.is_turn(pos[0], turn):
                            selected.move(self.Board, pos[0], pos[1])

                            print(pos)
                            if self.Board.checka(self.Board, turn):
                                self.Board.change(pos[1], pos[0])
                                turn -= 1
                            turn += 1

                            pos = []
                        else:
                            pos = []
            self.draw()
            pygame.display.update()

Main()
