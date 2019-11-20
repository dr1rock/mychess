# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Mind import *
import sqlite3
from random import choice


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Шахматы')
        self.setGeometry(50, 30, 1300, 850)
        self.m = 0
        self.shah = False
        self.field = Board()
        self.last_cklick = 0
        self.fboard = []
        self.the_end = False
        for i in range(1, 9, 1):
            self.row = []
            for j in range(1, 9, 1):
                self.la = QLabel('', self)
                self.la.move(j * 75, i * 75)
                if not (self.field.field[i - 1][j - 1] is None):
                    self.la.setPixmap(QPixmap(self.field.field[i - 1][j - 1].img))
                else:
                    self.la.setPixmap(QPixmap('blank.png'))
                self.la.coords = [j * 75, i * 75]
                self.la.fcoords = [8 - i, (j - 1)]
                self.la.resize(75, 75)
                self.la.installEventFilter(self)
                if self.field.field[i - 1][j - 1] is not None:
                    self.la.condition = 1 if self.field.field[i - 1][j - 1].color == self.field.color else 0
                else:
                    self.la.condition = 1
                self.row.append(self.la)
            self.fboard.append(self.row)
        self.player1 = QRadioButton(self)
        self.player1.setText('Белые')
        self.player1.move(100, 8)
        self.player1.resize(self.player1.sizeHint())
        self.player1.setChecked(True)
        self.player2 = QRadioButton(self)
        self.player2.setText('Чёрные')
        self.player2.move(160, 8)
        self.player2.resize(self.player2.sizeHint())
        self.p1 = QLineEdit(self)
        self.p1.move(300, 8)
        self.p1.setText('Белый')
        self.p2 = QLineEdit(self)
        self.p2.move(450, 8)
        self.p2.setText('Чёрный')
        self.pn_btn = QPushButton(self)
        self.pn_btn.move(600, 8)
        self.pn_btn.setText('Обработать имена игроков')
        self.pn_btn.clicked.connect(self.name)
        self.new_game = QPushButton(self)
        self.new_game.setText('Новая игра')
        self.new_game.move(8, 8)
        self.new_game.resize(self.new_game.sizeHint())
        self.new_game.clicked.connect(self.new_board)
        self.table = QTableWidget(self)
        self.table.move(750, 80)
        self.table.resize(420, 600)
        self.surrender = QPushButton(self)
        self.surrender.move(750, 8)
        self.surrender.setText('Сдаться')
        self.surrender.clicked.connect(self.surrender_in_game)
        self.sur = False
        self.humility = QPushButton(self)
        self.humility.move(830, 8)
        self.humility.setText('Объявить ничью')
        self.humility.clicked.connect(self.humility_in_game)
        self.hum = False
        self.crazy_chess = QPushButton(self)
        self.crazy_chess.move(930, 8)
        self.crazy_chess.setText('Безумные шахматы')
        self.crazy_chess.clicked.connect(self.mad)
        self.check_crazy = 0
        self.crazy = False
        self.name()
        self.fchess = QPushButton(self)
        self.fchess.move(1040, 8)
        self.fchess.setText('Шахматы фишера')
        self.fchess.clicked.connect(self.chess_of_Fisher)
        self.show()

    def chess_of_Fisher(self):
        self.field.field = [[None for j in range(8)] for i in range(8)]
        self.field.field[0] = [Bishop(WHITE), Knight(WHITE), Rook(WHITE),
                               Knight(WHITE), Queen(WHITE), King(WHITE), Rook(WHITE), Bishop(WHITE)]
        self.field.field[1] = [Pawn(WHITE) for i in range(8)]
        self.field.field[6] = [Pawn(BLACK) for i in range(8)]
        self.field.field[7] = [Bishop(BLACK), Knight(BLACK), Rook(BLACK),
                               Knight(BLACK), Queen(BLACK), King(BLACK), Rook(BLACK), Bishop(BLACK)]
        self.updater()

    def updater(self):
        for i in range(8):
            for j in range(8):
                if not (self.field.field[i][j] is None):
                    self.fboard[i][j].setPixmap(QPixmap(self.field.field[i][j].img))
                else:
                    self.fboard[i][j].setPixmap(QPixmap('blank.png'))

    def mad(self):
        if self.check_crazy % 2 == 0:
            self.crazy = True
        else:
            self.crazy = False
        self.check_crazy += 1

    def global_swap(self):
        for i in range(8):
            for j in range(8):
                if self.field.field[i][j] is not None and not(isinstance(self.field.field[i][j], King)):
                    if self.field.field[i][j].color == BLACK:
                        self.field.field[i][j] = choice(self.field.wf)
                        self.fboard[i][j].setPixmap(QPixmap(self.field.field[i][j].img))
                    else:
                        self.field.field[i][j] = choice(self.field.bf)
                        self.fboard[i][j].setPixmap(QPixmap(self.field.field[i][j].img))

    def name(self):
        self.pn1 = self.p1.text()
        self.pn2 = self.p2.text()

    def humility_in_game(self):
        self.the_end = True
        self.hum = True

    def surrender_in_game(self):
        self.the_end = True
        self.sur = True

    def new_board(self):
        self.m = 0
        self.con = sqlite3.connect('stat.db')
        cur = self.con.cursor()
        result = cur.execute("""
                    DELETE from game
                    WHERE q > 0""").fetchall()
        self.con.close()
        self.field = Board()
        self.the_end = False
        self.hum = False
        self.sur = False
        for i in range(8):
            for j in range(8):
                if self.field.field[i][j] is not None:
                    self.fboard[i][j].setPixmap(QPixmap(self.field.field[i][j].img))
                else:
                    self.fboard[i][j].setPixmap(QPixmap('blank.png'))
        self.player1.setChecked(True)

    def load_table(self, r, c, r1, c1):
        self.con = sqlite3.connect("stat.db")
        # Создание курсора
        cursor = self.con.cursor()
        cursor.execute('''SELECT * FROM game''')
        self.table.setRowCount(self.m)
        self.table.setColumnCount(4)     # Устанавливаем три колонки
        self.table.setHorizontalHeaderLabels(["Ход", "Откуда", "Куда", "Ходит"])
        self.table.setItem(0, 0, QTableWidgetItem(str(self.m)))
        self.table.setItem(0, 1, QTableWidgetItem("{}".format(self.alf[c] + str(7 - r + 1))))
        self.table.setItem(0, 2, QTableWidgetItem("{}".format(self.alf[c1] + str(7 - r1 + 1))))
        if self.field.color == BLACK:
            self.table.setItem(0, 3, QTableWidgetItem(self.pn1))
        else:
            self.table.setItem(0, 3, QTableWidgetItem(self.pn2))
        for row, form in enumerate(cursor):
            self.table.insertRow(row)
            for column, item in enumerate(form):
                self.table.setItem(row, column, QTableWidgetItem(str(item)))
        self.con.close()

    def eventFilter(self, obj, e):
        # метод позволяет виджету QLabel() реагировать на клики мышкой по нему
        if e.type() == QEvent.MouseButtonRelease:
            btn = e.button()
            if btn == 1 and not self.the_end:
                self.motion(obj)
        return super(QWidget, self).eventFilter(obj, e)

    def paintEvent(self, event):
        self.alf = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.qp = QPainter(self)
        self.qp.begin(self)
        # рисую фон окна
        self.qp.drawPixmap(0, 0, QPixmap('images/background.jpg'))
        self.qp.setPen(QPen(QColor(140, 187, 211), 40))
        self.qp.drawRect(0, 0, 2000, 20)
        # рисую доску
        self.qp.drawPixmap(75, 75, QPixmap('images/board.png'))
        # рисую у доски "шахматные кординаты" полей
        self.qp.setPen(QPen(QColor(0, 0, 0), 10))
        self.qp.drawRect(70, 70, 610, 610)
        self.qp.setFont(QFont('Arial', 20, 200))
        for i in range(1, 9, 1):
            self.qp.drawText(75 - 35, i * 75 + 45, '{}'.format(9 - i))
            self.qp.drawText(i * 75 + 25, 720, self.alf[i - 1])
        self.qp.setPen(QPen(QColor(0, 0, 0), 10))
        # (описание в методе draw_marking())
        if self.last_cklick != 0:
            self.draw_marking(self.qp)
        # рисую экран окончания
        if self.the_end and not self.hum and not self.sur:
            pl = self.field.is_this_the_end()
            if pl == BLACK:
                pl = 'Белые'
            else:
                pl = 'Черные'
            self.qp.setFont(QFont('Arial', 50, 200))
            self.qp.drawText(80, 390, pl + ' победили')
        elif self.hum:
            self.qp.setFont(QFont('Arial', 50, 200))
            self.qp.drawText(250, 390, 'Ничья')
        elif self.sur:
            pl = 'Белые' if self.field.color == WHITE else 'Чёрные'
            self.qp.setFont(QFont('Arial', 50, 200))
            self.qp.drawText(80, 390, pl + ' победили')
        if self.shah:
            row, col = self.field.king_finder()
            self.qp.setPen(QPen(QColor(255, 0, 0), 8))
            self.qp.setFont(QFont('Arial', 12, 200))
            self.qp.drawText(240, 22, 'Шах')
            self.qp.drawRect((col + 1) * 75, (row + 1) * 75, 75, 75)
        self.qp.end()
        self.update()

    def draw_marking(self, qp):
        '''метод обрисовывает нажатые поля на доске
         и поля на которые выделенная фигура может сходить'''

        if type(self.last_cklick) == type(QLabel()):
            col = int(self.last_cklick.coords[0] / 75)
            row = int(self.last_cklick.coords[1] / 75)
            t = self.field.field[row - 1][col - 1]
            if t.color == self.field.color if t is not None else False:
                qp.setPen(QPen(QColor(0, 255, 0), 8))
                qp.drawRect(col * 75, row * 75, 75, 75)
                for i in range(8):
                    for j in range(8):
                        if isinstance(t, Pawn) and t.can_move(self.field, row - 1, col - 1, i, j):
                            qp.setPen(QPen(QColor(0, 255, 0), 8))
                            qp.drawRect((j + 1) * 75, (i + 1) * 75, 75, 75)
                        elif (t.can_move(self.field, row - 1, col - 1, i, j)
                              and not(t.can_eat(self.field, row - 1, col - 1, i, j))):
                            qp.setPen(QPen(QColor(0, 255, 0), 8))
                            qp.drawRect((j + 1) * 75, (i + 1) * 75, 75, 75)
                        elif (t.can_attack(self.field, row - 1, col - 1, i, j) and (
                                (t.can_move(self.field, row - 1, col - 1, i, j))
                                if not isinstance(self.field.field[row - 1][col - 1], Pawn) else
                                self.field.field[row - 1][col - 1].can_eat(self.field, row - 1, col - 1, i, j))):
                            qp.setPen(QPen(QColor(255, 0, 0), 8))
                            qp.drawRect((j + 1) * 75, (i + 1) * 75, 75, 75)
            else:
                qp.setPen(QPen(QColor(255, 0, 0), 8))
                qp.drawRect(col * 75, row * 75, 75, 75)

    def pawn_transformation(self):
        ''' метод проеряет не дошла ли пешка до конца поля.
         Если дошла то превращает её в Ферзя'''
        for i in range(8):
            for j in range(8):
                if i == 7 and isinstance(self.field.field[i][j], Pawn) and\
                        (self.field.field[i][j].color == WHITE if
                            self.field.field[i][j] is not None else False):
                    self.field.field[i][j] = Queen(WHITE)
                    self.fboard[i][j].setPixmap(QPixmap(self.field.field[i][j].img))
                elif i == 0 and isinstance(self.field.field[i][j], Pawn) and\
                        (self.field.field[i][j].color == BLACK if
                            self.field.field[i][j] is not None else False):
                    self.field.field[i][j] = Queen(BLACK)
                    self.fboard[i][j].setPixmap(QPixmap(self.field.field[i][j].img))

    def motion(self, obj):
        '''метод оуществляет движение фигур'''

        lc = self.last_cklick
        if self.last_cklick == 0:
            self.last_cklick = obj
        elif lc.fcoords == obj.fcoords:
            self.last_cklick = 0
        elif (((not (self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].can_move(self.field,
                                                                                 7 - lc.fcoords[0], lc.fcoords[1],
                                                                                 7 - obj.fcoords[0], obj.fcoords[1])))
                if not(self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]] is None) else False)
                if not isinstance(self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]], Pawn) else False):
            self.last_cklick = obj
        elif self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]] is None:
            self.last_cklick = obj
        # движение
        elif ((self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].can_move(self.field,
                                                                           7 - lc.fcoords[0], lc.fcoords[1],
                                                                           7 - obj.fcoords[0], obj.fcoords[1]))
                if type(lc) == type(QLabel()) and
                self.field.field[7 - obj.fcoords[0]][obj.fcoords[1]] is None else False):
            self.m += 1
            self.load_table(7 - lc.fcoords[0], lc.fcoords[1], 7 - obj.fcoords[0], obj.fcoords[1])
            self.fboard[7 - lc.fcoords[0]][lc.fcoords[1]].setPixmap(QPixmap('blank.png'))
            self.fboard[7 - obj.fcoords[0]][obj.fcoords[1]].setPixmap(QPixmap(
                self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].img))
            self.field.field[7 - obj.fcoords[0]][obj.fcoords[1]] = \
                self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].set_position()
            self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]] = None
            self.pawn_transformation()
            self.last_cklick = 0
            self.field.color = opponent(self.field.color)
            if self.crazy:
                self.global_swap()
        # съедение
        elif (self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].can_eat(self.field,
                                                                           7 - lc.fcoords[0],lc.fcoords[1],
                                                                           7 - obj.fcoords[0], obj.fcoords[1])) and \
                self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].can_move(self.field,
                                                                           7 - lc.fcoords[0], lc.fcoords[1],
                                                                           7 - obj.fcoords[0], obj.fcoords[1]) if \
                not isinstance(self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]], Pawn) else\
                self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].can_eat(self.field,
                                                                           7 - lc.fcoords[0],lc.fcoords[1],
                                                                           7 - obj.fcoords[0], obj.fcoords[1]):
            self.m += 1
            self.load_table(7 - lc.fcoords[0], lc.fcoords[1], 7 - obj.fcoords[0], obj.fcoords[1])
            self.fboard[7 - lc.fcoords[0]][lc.fcoords[1]].setPixmap(QPixmap('blank.png'))
            self.fboard[7 - obj.fcoords[0]][obj.fcoords[1]].setPixmap(
                QPixmap(self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].img))
            self.field.field[7 - obj.fcoords[0]][obj.fcoords[1]] = self.field.field[7 - lc.fcoords[0]][
                lc.fcoords[1]].set_position()
            self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]] = None
            self.last_cklick.condition, obj.condition = obj.condition, self.last_cklick.condition
            self.pawn_transformation()
            self.last_cklick = 0
            self.field.color = opponent(self.field.color)
            if self.field.is_this_the_end():
                self.the_end = True
                self.player1.setChecked(True)
            elif self.crazy:
                self.global_swap()

        # движение для пешки
        elif isinstance(self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]], Pawn):
            if (not self.field.field[7 - lc.fcoords[0]][lc.fcoords[1]].can_move(self.field,
                                                                               7 - lc.fcoords[0], lc.fcoords[1],
                                                                               7 - obj.fcoords[0], obj.fcoords[1])):
                self.last_cklick = obj
        # рокировка
        elif self.field.casting(7 - obj.fcoords[0], obj.fcoords[1]) if lc is not None else False:
            if self.field.color == BLACK:
                p = 7
            else:
                p = 0
            self.m += 1
            self.load_table(p, 4, p, 6)
            self.field.field[p][6] = self.field.field[p][4].set_position()
            self.field.field[p][5] = self.field.field[p][7].set_position()
            self.field.field[p][4] = None
            self.field.field[p][7] = None
            self.fboard[p][4].setPixmap(QPixmap('blank.png'))
            self.fboard[p][7].setPixmap(QPixmap('blank.png'))
            self.fboard[p][5].setPixmap(QPixmap(self.field.field[p][5].img))
            self.fboard[p][6].setPixmap(QPixmap(self.field.field[p][6].img))
            self.last_cklick = 0
            self.field.color = opponent(self.field.color)
            if self.crazy:
                self.field.global_swap()

        if self.field.color == BLACK:
            self.player1.setChecked(True)
        else:
            self.player2.setChecked(True)

        if (self.field.king_is_under_attack() if not self.the_end else False) and lc != 0:
            self.shah = True
        else:
            self.shah = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    sys.exit(app.exec_())