WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = BLACK
        self.field = []
        self.checker = False
        self.bf = [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Pawn(WHITE),
                   Rook(WHITE), Knight(WHITE), Bishop(WHITE), Pawn(WHITE),
                   Rook(WHITE), Knight(WHITE), Bishop(WHITE), Pawn(WHITE),
                   Queen(WHITE)]
        self.wf = [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Pawn(BLACK),
                   Rook(BLACK), Knight(BLACK), Bishop(BLACK), Pawn(BLACK),
                   Rook(BLACK), Knight(BLACK), Bishop(BLACK), Pawn(BLACK),
                   Queen(BLACK)]
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]


    def current_player_color(self):
        return self.color

    def casting(self, row1, col1):
        ''' метод роверяет возможна ли рокировка '''
        if row1 in [7, 0] and col1 == 7:
            if (isinstance(self.field[7][4], King) and
                    self.field[7][5] is None and
                    self.field[7][6] is None and
                    isinstance(self.field[7][7], Rook) and
                    (self.field[7][4].color == BLACK == self.color) if self.field[7][4] is not None else False and
                    (self.field[7][7].color == BLACK == self.color) if self.field[7][4] is not None else False) and row1 == 7:
                return True
            elif (isinstance(self.field[0][4], King) and
                    self.field[0][5] is None and
                    self.field[0][6] is None and
                    isinstance(self.field[0][7], Rook) and
                    (self.field[0][4].color == WHITE == self.color) if self.field[0][4] is not None else False and
                    (self.field[0][7].color == WHITE == self.color) if self.field[0][4] is not None else False) and row1 == 0:
                return True

    def is_this_the_end(self):
        ''' метод считает количество королей на доске,
         а значит проверяет закончилась ли игра '''

        king_counter = 0
        for i in self.field:
            for j in i:
                if isinstance(j, King):
                    king_counter += 1
                    c = j.get_color()
        if king_counter == 2:
            return False
        else:
            return c

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        # возвращает фигуру и ее цвет
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def half_move(self, row, col, row1, col1, piece):
        self.field[row][col].m += 1
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = opponent(self.color)

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False

        if piece.can_move(self, row, col, row1, col1):
            if self.king_is_under_attack():
                if self.antishah(row, col, row1, col1):
                    self.half_move(row, col, row1, col1, piece)
                    return True
                else:
                    return False
            else:
                self.half_move(row, col, row1, col1, piece)
                return True
        elif piece.can_attack(self, row, col, row1, col1):
            if self.king_is_under_attack():
                if self.antishah(row, col, row1, col1):
                    self.half_move(row, col, row1, col1, piece)
                    return True
                else:
                    return False
            else:
                self.half_move(row, col, row1, col1, piece)
                return True

    def char(self, row, col):
        return self.cell(row, col)[1]

    def field_color(self, row, col):
        color = 1 if self.cell(row, col)[0] == 'w' else 2
        return color

    def number_of_moves(self, row, col):
        return self.field[row][col].m

    def castling0(self):
        colR = 0
        colK = 4
        if self.color == 1:
            row = 0
            if self.char(row, colR) == 'R':
                m = self.number_of_moves(row, colR)
                if m != 0:
                    return False
            if self.char(row, colK) == 'K':
                n = self.number_of_moves(row, colK)
                if n != 0:
                    return False
            for c in range(1, 4):
                if not (self.get_piece(row, c) is None):
                    return False
            if self.char(row, colR) == 'R' and self.cell(row, colR)[0] == 'w' \
                    and self.char(row, colK) == 'K' and \
                    self.cell(row, colK)[0] == 'w':
                self.field[row][colR] = None
                self.field[0][3] = Rook(WHITE)
                self.field[row][colK] = None
                self.field[0][2] = King(WHITE)
                self.color = opponent(self.color)
                return True
            else:
                return False
        elif self.color == 2:
            row = 7
            if self.char(row, colR) == 'R':
                m = self.number_of_moves(row, colR)
                if m != 0:
                    return False
            if self.char(row, colK) == 'K':
                n = self.number_of_moves(row, colK)
                if n != 0:
                    return False
            for c in range(1, 4):
                if not (self.get_piece(row, c) is None):
                    return False
            if self.char(row, colR) == 'R' and self.cell(row, colR)[0] == 'b' \
                    and self.char(row, colK) == 'K' and \
                    self.cell(row, colK)[0] == 'b':
                self.field[row][colR] = None
                self.field[7][3] = Rook(BLACK)
                self.field[row][colK] = None
                self.field[7][2] = King(BLACK)
                self.color = opponent(self.color)
                return True
            else:
                return False

    def castling7(self):
        colR = 7
        colK = 4
        if self.color == 1:
            row = 0
            if self.char(row, colR) == 'R':
                m = self.number_of_moves(row, colR)
                if m != 0:
                    return False
            if self.char(row, colK) == 'K':
                n = self.number_of_moves(row, colK)
                if n != 0:
                    return False
            for c in range(5, 7):
                if not (self.get_piece(row, c) is None):
                    return False
            if self.char(row, colR) == 'R' and self.cell(row, colR)[0] == 'w' \
                    and self.char(row, colK) == 'K' and \
                    self.cell(row, colK)[0] == 'w':
                self.field[row][colR] = None
                self.field[0][5] = Rook(WHITE)
                self.field[row][colK] = None
                self.field[0][6] = King(WHITE)
                self.color = opponent(self.color)
                return True
            else:
                return False
        elif self.color == 2:
            row = 7
            if self.char(row, colR) == 'R':
                m = self.number_of_moves(row, colR)
                if m != 0:
                    return False
            if self.char(row, colK) == 'K':
                n = self.number_of_moves(row, colK)
                if n != 0:
                    return False
            for c in range(5, 7):
                if not (self.get_piece(row, c) is None):
                    return False
            if self.char(row, colR) == 'R' and self.cell(row, colR)[0] == 'b' \
                    and self.char(row, colK) == 'K' and \
                    self.cell(row, colK)[0] == 'b':
                self.field[row][colR] = None
                self.field[7][5] = Rook(BLACK)
                self.field[row][colK] = None
                self.field[7][6] = King(BLACK)
                self.color = opponent(self.color)
                return True
            else:
                return False

    def is_under_attack(self, row, col):
        for r in range(7, -1, -1):
            for c in range(8):
                self.checker = True
                if not (self.field[r][c] is None):
                    if (self.field[r][c].color == opponent(self.color)
                            and (self.field[r][c].can_attack(self, r, c, row, col))):
                        self.checker = False
                        return True
        self.checker = False
        return False

    def king_finder(self):
        for row in range(7, -1, -1):
            for col in range(8):
                if isinstance(self.field[row][col], King) and self.color == self.field[row][col].color:
                    return row, col

    def king_is_under_attack(self):
        row, col = self.king_finder()
        if self.is_under_attack(row, col):
            return True
        return False

    def antishah(self, row, col, row1, col1):
        piece = self.field[row][col]
        if self.char(row, col) != 'K':
            if not piece.can_move(self, row, col, row1, col1):
                return False
            for r in range(-7, -1, -1):
                for c in range(8):
                    if self.char(r, c) == 'K' and self.color == self.field_color(r, c):
                        for r1 in range(7, -1, -1):
                            for c1 in range(8):
                                if not (self.field[r1][c1] is None) \
                                        and self.field_color(r1, c1) == opponent(self.color) \
                                        and self.field[r1][c1].can_attack(self, r1, c1, r, c):
                                    if row1 == r1 and col1 == c1:
                                        return True
                                    if self.char(r1, c1) == 'R':
                                        if r > r1:
                                            stepr1 = 1
                                        elif r < r1:
                                            stepr1 = -1
                                        else:
                                            stepr1 = 0
                                        if c > c1:
                                            stepc1 = 1
                                        elif c < c1:
                                            stepc1 = -1
                                        else:
                                            stepc1 = 0
                                        r0 = r1
                                        c0 = c1
                                        if stepr1 != 0 and stepc1 == 0:
                                            for i in range(r1, r, stepr1):
                                                r0 += stepr1
                                                c0 += stepc1
                                                if row1 == r0 and col1 == c0:
                                                    return True
                                        if stepr1 == 0 and stepc1 != 0:
                                            for i in range(c1, c, stepc1):
                                                r0 += stepr1
                                                c0 += stepc1
                                                if row1 == r0 and col1 == c0:
                                                    return True
                                    elif self.char(r1, c1) == 'B':
                                        stepc1 = 1 if (c > c1) else -1
                                        stepr1 = 1 if (r > r1) else -1
                                        r0 = r1
                                        c0 = c1
                                        if stepr1 != 0 and stepc1 != 0:
                                            for cr in range(c1, c, stepc1):
                                                r0 += stepr1
                                                c0 += stepc1
                                                if row1 == r0 and col1 == c0:
                                                    return True
                                    elif self.char(r1, c1) == 'Q':
                                        if r > r1:
                                            stepr1 = 1
                                        elif r < r1:
                                            stepr1 = -1
                                        else:
                                            stepr1 = 0
                                        if c > c1:
                                            stepc1 = 1
                                        elif c < c1:
                                            stepc1 = -1
                                        else:
                                            stepc1 = 0
                                        r0 = r1
                                        c0 = c1
                                        if stepr1 != 0 and stepc1 == 0:
                                            for i in range(r1, r, stepr1):
                                                r0 += stepr1
                                                c0 += stepc1
                                                if row1 == r0 and col1 == c0:
                                                    return True
                                        if stepr1 == 0 and stepc1 != 0:
                                            for i in range(c1, c, stepc1):
                                                r0 += stepr1
                                                c0 += stepc1
                                                if row1 == r0 and col1 == c0:
                                                    return True
                                        if stepr1 != 0 and stepc1 != 0:
                                            for cr in range(c1, c, stepc1):
                                                r0 += stepr1
                                                c0 += stepc1
                                                if row1 == r0 and col1 == c0:
                                                    return True
                                    else:
                                        return False
        else:
            return piece.can_move(self, row, col, row1, col1)


class Rook:

    def __init__(self, color):
        self.color = color
        self.m = 0
        self.img = 'images/' + ('white' if self.color != 1 else 'black') + '_rook.png'

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if board.field[row][col].color == board.color or board.checker:
            if row1 > row:
                stepr = 1
            elif row1 < row:
                stepr = -1
            else:
                stepr = 0

            if col1 > col:
                stepc = 1
            elif col1 < col:
                stepc = -1
            else:
                stepc = 0

            r = row
            c = col
            if stepr != 0 and stepc == 0:
                for i in range(row, row1, stepr):
                    r += stepr
                    c += stepc
                    # Если на пути по вертикали есть фигура
                    if not (board.get_piece(r - stepr, c) is None) and \
                            board.cell(r - stepr, c)[0] != board.cell(row, col)[0]:
                        return False
                    if not (board.get_piece(r, c) is None) and \
                            board.cell(r, c)[0] == board.cell(row, col)[0]:
                        return False

            if stepr == 0 and stepc != 0:
                for i in range(col, col1, stepc):
                    r += stepr
                    c += stepc
                    # Если на пути по горизонтали есть фигура
                    if not (board.get_piece(r, c - stepc) is None) and \
                            board.cell(r, c - stepc)[0] != board.cell(row, col)[0]:
                        return False
                    if not (board.get_piece(r, c) is None) and \
                            board.cell(r, c)[0] == board.cell(row, col)[0]:
                        return False

            if row == row1 or col == col1 and (0 <= row <= 7) and (0 <= col <= 7):
                if row == row1 and col == col1:
                    return False
                else:
                    return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def set_position(self):
        return Rook(self.color)

    def can_eat(self, field, row0, col0, row, col):
        if field.field[row0][col0].color == field.color:
            if field.field[row][col] is not None:
                if field.field[row][col].color != self.color:
                    return True
        return False


class Pawn:

    def __init__(self, color):
        self.color = color
        self.m = 0
        self.img = 'images/' + ('white' if self.color != 1 else 'black') + '_pawn.png'

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def set_position(self):
        return Pawn(self.color)

    def can_move(self, board, row, col, row1, col1):
        # "взятие на проходе" не реализовано
        if board.field[row][col].color == board.color:
            if col - 1 != col1 and col + 1 != col1 and col != col1 or board.field[row1][col1] is not None:
                return False

            if self.color == WHITE:
                direction = 1
                start_row = 1
            else:
                direction = -1
                start_row = 6

            if row + direction == row1 and col == col1:
                if not (board.get_piece(row1, col) is None) and \
                        board.cell(row1, col)[0] != board.cell(row, col)[0]:
                    return True
                if board.get_piece(row1, col) is None:
                    return True

            if row == start_row and row + 2 * direction == row1 and col == col1:
                if not (board.field[row + direction][col] is None):
                    return False
                if not (board.field[row + 2 * direction][col] is None):
                    if board.cell(row + 2 * direction, col)[0] != board.cell(row, col)[0]:
                        return True
                if board.field[row + 2 * direction][col] is None:
                    return True
        return False

    def can_attack(self, board, row0, col0, row, col):
        if board.field[row0][col0].color == board.color or board.checker:
            if ((row0 - row) in [1, -1]) and col0 - col in [1, -1]:
                if board.field[row0][col0].color == WHITE and row == row0 + 1:
                    return True
                elif board.field[row0][col0].color == BLACK and row == row0 - 1:
                    return True
        return False

    def can_eat(self, field, row0, col0, row, col):
        if field.field[row0][col0].color == field.color:
            if (field.field[row][col] is not None) and ((row0 - row) in [1, -1]) and col0 - col in [1, -1]:
                if field.field[row0][col0].color != field.field[row][col].color:
                    if field.field[row][col].color == WHITE and row == row0 - 1:
                        return True
                    elif field.field[row][col].color == BLACK and row == row0 + 1:
                        return True
        return False


class Knight:

    def __init__(self, color):
        self.m = 0
        self.color = color
        self.img = 'images/' + ('white' if self.color != 1 else 'black') + '_knight.png'

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):

        stepr = row1 - row
        stepc = col1 - col
        if board.field[row][col].color == board.color or board.checker:
            if not (board.get_piece(row1, col1) is None) and \
                    board.cell(row1, col1)[0] == board.cell(row, col)[0]:
                return False

            if ((((stepr == 1 or stepr == -1) and (stepc == 2 or stepc == -2)) or (
                    (stepr == 2 or stepr == -2) and (stepc == 1 or stepc == -1)))
                or row == row1 or col == col1) and (
                    0 <= row <= 7) and (0 <= col <= 7):
                if row == row1 or col == col1:
                    return False
                else:
                    return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def set_position(self):
        return Knight(self.color)

    def can_eat(self, field, row0, col0, row, col):
        if field.field[row][col] is not None and self.can_move(field, row0, col0, row, col):
            if field.field[row][col].color != self.color:
                return True
        else:
            return False


class King:

    def __init__(self, color):
        self.color = color
        self.m = 0
        self.img = 'images/' + ('white' if self.color != 1 else 'black') + '_king.png'

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if board.casting(row1, col1) and board.field[row][col].color == board.color:
            return True
        if col - col1 in [0, 1, -1] and row - row1 in [0, 1, -1]:
            if board.field[row][col].color == board.color:
                if board.field[row1][col1] is not None:
                    if board.field[row1][col1].color != board.field[row][col].color:
                        return True
                    else:
                        return False
                if board.field[row1][col1] is None:
                    if row == row1 and col == col1:
                        return False
                    if board.is_under_attack(row1, col1):
                        return False
                return True
        return False

    def can_attack(self, field, row0, col0, row, col):
        if col0 - col in [0, 1, -1] and row0 - row in [0, 1, -1] and field.field[row][col] is not None:
            if field.field[row0][col0].color == field.color or self.checker:
                if field.field[row][col].color != field.field[row0][col0].color:
                    return True
            return False
        else:
            return False

    def set_position(self):
        return King(self.color)

    def can_eat(self, field, row0, col0, row, col):
        if col0 - col in [0, 1, -1] and row0 - row in [0, 1, -1] and field.field[row][col] is not None:
            if field.field[row0][col0].color == field.color:
                if field.field[row][col].color != field.field[row0][col0].color:
                    return True
        else:
            return False


class Queen:

    def __init__(self, color):
        self.m = 0
        self.color = color
        self.img = 'images/' + ('white' if self.color != 1 else 'black') + '_queen.png'

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if board.field[row][col].color == board.color or board.checker:
            if row1 > row:
                stepr = 1
            elif row1 < row:
                stepr = -1
            else:
                stepr = 0

            if col1 > col:
                stepc = 1
            elif col1 < col:
                stepc = -1
            else:
                stepc = 0

            r = row
            c = col
            if stepr != 0 and stepc == 0:
                for i in range(row, row1, stepr):
                    r += stepr
                    c += stepc
                    # Если на пути по вертикали есть фигура
                    if not (board.get_piece(r - stepr, c) is None) and \
                            board.cell(r - stepr, c)[0] != board.cell(row, col)[0]:
                        return False
                    if not (board.get_piece(r, c) is None) and \
                            board.cell(r, c)[0] == board.cell(row, col)[0]:
                        return False

            if stepr == 0 and stepc != 0:
                for i in range(col, col1, stepc):
                    r += stepr
                    c += stepc
                    # Если на пути по горизонтали есть фигура
                    if not (board.get_piece(r, c - stepc) is None) and \
                            board.cell(r, c - stepc)[0] != board.cell(row, col)[0]:
                        return False
                    if not (board.get_piece(r, c) is None) and \
                            board.cell(r, c)[0] == board.cell(row, col)[0]:
                        return False

            if stepr != 0 and stepc != 0:
                for cr in range(row, row1, stepr):
                    r += stepr
                    c += stepc
                    if not (board.get_piece(r - stepr, c - stepc) is None) and \
                            board.cell(r - stepr, c - stepc)[0] != \
                            board.cell(row, col)[0]:
                        return False
                    if not (board.get_piece(r, c) is None) and \
                            board.cell(r, c)[0] == board.cell(row, col)[0]:
                        return False

            if ((row - row1 == col - col1) or (row - row1 == -(col - col1))
                or (row == row1) or (col == col1)) and (
                    0 <= row <= 7) and (0 <= col <= 7):
                if row == row1 and col == col1:
                    return False
                else:
                    return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def set_position(self):
        return Queen(self.color)

    def can_eat(self, feild, row0, col0, row, col):
        if feild.field[row][col] is not None:
            return self.can_move(feild, row0, col0, row, col)
        return False


class Bishop:

    def __init__(self, color):
        self.color = color
        self.m = 0
        self.img = 'images/' + ('white' if self.color != 1 else 'black') + '_bishop.png'

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        stepc = 1 if (col1 > col) else -1
        stepr = 1 if (row1 > row) else -1
        r = row
        c = col
        if board.field[row][col].color == board.color or board.checker:
            if stepr != 0 and stepc != 0:
                for cr in range(col, col1, stepc):
                    r += stepr
                    c += stepc
                    if not (board.get_piece(r - stepr, c - stepc) is None) and \
                            board.cell(r - stepr, c - stepc)[0] != \
                            board.cell(row, col)[0]:
                        return False
                    if not (board.get_piece(r, c) is None) and \
                            board.cell(r, c)[0] == board.cell(row, col)[0]:
                        return False

            if ((row - row1 == col - col1) or (row - row1 == -(col - col1))) \
                    or (row == row1) or (col == col1) and (
                    0 <= row <= 7) and (0 <= col <= 7):
                if row == row1 or col == col1:
                    return False
                else:
                    return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def set_position(self):
        return Bishop(self.color)

    def can_eat(self, field, row0, col0, row, col):
        if field.field[row0][col0].color == field.color:
            if field.field[row][col] is not None:
                if field.field[row][col].color != self.color:
                    return True
        return False

