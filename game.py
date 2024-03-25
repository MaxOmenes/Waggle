from table import Table
from cell_type import CellType
from game_status import GameStatus


class Game:
    can_row = []
    can_col = []

    def __init__(self, level: list[list[int]]):
        self.level = level
        self.status = GameStatus.PLAYING
        self.table = Table(level)
        self.table.cellClicked.connect(self.event)
        self.table.set_size(50)
        self.table.show_table()

    def get_table(self):
        return self.table

    def remove_can(self):
        for i in range(len(self.can_row)):
            self.table.set_empty(self.can_row[i], self.can_col[i])
        self.can_row = []
        self.can_col = []

    def calculate_can(self, row, col) -> list[tuple[int, int]]:
        can = []
        table: list[list[CellType]] = self.table.table.copy()
        if row < len(table) - 2:  # down check
            if ((table[row + 2][col] == CellType.EMPTY or
                    table[row + 2][col] == CellType.CAN) and
                    table[row + 1][col] == CellType.BLOCK):
                can.append((row + 2, col))

        if row > 1:  # up check
            if ((table[row - 2][col] == CellType.EMPTY or
                    table[row - 2][col] == CellType.CAN) and
                    table[row - 1][col] == CellType.BLOCK):
                can.append((row - 2, col))

        if col < len(table[0]) - 2: # right check
            if ((table[row][col + 2] == CellType.EMPTY or
                    table[row][col + 2] == CellType.CAN) and
                    table[row][col + 1] == CellType.BLOCK):
                can.append((row, col + 2))

        if col > 1:  # left check
            if ((table[row][col - 2] == CellType.EMPTY or
                    table[row][col - 2] == CellType.CAN) and
                    table[row][col - 1] == CellType.BLOCK):
                can.append((row, col - 2))

        return can

    def game_status(self) -> bool:
        if self.status != GameStatus.PLAYING:
            return False
        if self.check_win():
            self.status = GameStatus.WIN
            print("You win!")
            return True
        if self.check_lose():
            self.status = GameStatus.LOSE
            print("Looser!")

            return True

    def event(self, row, col):

        clicked_cell = self.table.table[row][col]

        match clicked_cell:
            case CellType.EMPTY:
                return
            case CellType.BLOCK:
                self.table.set_selected(row, col)
                self.remove_can()
                can = self.calculate_can(row, col)
                self.can_row = [x for x, y in can]
                self.can_col = [y for x, y in can]
                for i in range(len(can)):
                    self.table.add_can(self.can_row[i], self.can_col[i])
            case CellType.CAN:
                empty_row = (row + self.table.selected_row) // 2
                empty_col = (col + self.table.selected_col) // 2
                self.remove_can()
                self.table.set_block(row, col)
                self.table.set_empty(empty_row, empty_col)
                selected_row, selected_col = self.table.get_selected()
                self.table.remove_selected()
                self.table.set_empty(selected_row, selected_col)
            case CellType.SELECTED:
                self.table.remove_selected()
                self.remove_can()

        self.table.show_table()

        if self.game_status():
            return

    def check_win(self):
        count = 0
        for i in range(len(self.table.table)):
            for j in range(len(self.table.table[0])):
                if self.table.table[i][j] == CellType.BLOCK:
                    count += 1

        return count == 1

    def check_lose(self):
        for i in range(len(self.table.table)):
            for j in range(len(self.table.table[0])):
                if (self.table.table[i][j] == CellType.BLOCK or
                        self.table.table[i][j] == CellType.SELECTED):
                    if self.calculate_can(i, j):
                        return False
        return True
