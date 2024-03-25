from PyQt6.QtWidgets import QTableWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QEvent, Qt
from enum import Enum


class CellType(Enum):
    EMPTY = 0
    BLOCK = 1
    CAN = 2
    SELECTED = 3


def get_type(i: int):
    match i:
        case 0:
            return CellType.EMPTY
        case 1:
            return CellType.BLOCK
        case 2:
            return CellType.CAN
        case 3:
            return CellType.SELECTED


class Table(QTableWidget):
    keyPressed = pyqtSignal(QEvent)
    selected_row = -1
    selected_col = -1
    can_row = []
    can_col = []

    def __init__(self, table: list[list[int]]):
        super().__init__(len(table), len(table[0]))

        self.table = [[get_type(i) for i in row] for row in table]

        self.set_size(50)

        self.show_table()
        self.cellClicked.connect(self.cell_event)

    def set_size(self, size: int):
        for i in range(len(self.table)):  # set row height and column width
            self.setRowHeight(i, size)

        for i in range(len(self.table[0])):
            self.setColumnWidth(i, size)

    def cell_event(self, row, col):  # main game logic
        match self.table[row][col]:
            case CellType.EMPTY:
                pass
            case CellType.BLOCK:
                self.cell_move(row, col)
            case CellType.CAN:
                self.cell_moved(row, col)
            case CellType.SELECTED:  # deselect
                self.remove_can()
                self.table[row][col] = CellType.BLOCK
                self.repaint_cell(row, col, CellType.BLOCK)
                if self.selected_row != -1:
                    self.table[self.selected_row][self.selected_col] = CellType.BLOCK
                    self.repaint_cell(self.selected_row, self.selected_col, CellType.BLOCK)
                self.selected_row = -1
                self.selected_col = -1

    def cell_move(self, row, col):
        if self.selected_row != -1:  # deselect
            self.table[self.selected_row][self.selected_col] = CellType.BLOCK
            self.repaint_cell(self.selected_row, self.selected_col, CellType.BLOCK)
            self.remove_can()

        self.table[row][col] = CellType.SELECTED
        self.repaint_cell(row, col, CellType.SELECTED)
        self.selected_row = row
        self.selected_col = col
        if row < len(self.table) - 2:  # down check
            if (self.table[row + 2][col] == CellType.EMPTY and
                    self.table[row + 1][col] == CellType.BLOCK):
                self.table[row + 2][col] = CellType.CAN
                self.can_row.append(row + 2)
                self.can_col.append(col)
                self.repaint_cell(row + 2, col, CellType.CAN)
        if row > 1:  # up check
            if (self.table[row - 2][col] == CellType.EMPTY and
                    self.table[row - 1][col] == CellType.BLOCK):
                self.table[row - 2][col] = CellType.CAN
                self.can_row.append(row - 2)
                self.can_col.append(col)
                self.repaint_cell(row - 2, col, CellType.CAN)
        if col < len(self.table[0]) - 2:  # right check
            if (self.table[row][col + 2] == CellType.EMPTY and
                    self.table[row][col + 1] == CellType.BLOCK):
                self.table[row][col + 2] = CellType.CAN
                self.can_row.append(row)
                self.can_col.append(col + 2)
                self.repaint_cell(row, col + 2, CellType.CAN)
        if col > 1:  # left check
            if (self.table[row][col - 2] == CellType.EMPTY and
                    self.table[row][col - 1] == CellType.BLOCK):
                self.table[row][col - 2] = CellType.CAN
                self.can_row.append(row)
                self.can_col.append(col - 2)
                self.repaint_cell(row, col - 2, CellType.CAN)

    def cell_moved(self, row, col):
        delete_row = (self.selected_row + row) // 2
        delete_col = (self.selected_col + col) // 2

        self.table[row][col] = CellType.BLOCK
        self.table[self.selected_row][self.selected_col] = CellType.EMPTY
        self.table[delete_row][delete_col] = CellType.EMPTY

        self.remove_can()

        self.repaint_cell(row, col, CellType.BLOCK)  # repaint moved cell
        self.repaint_cell(self.selected_row, self.selected_col, CellType.EMPTY)
        self.repaint_cell(delete_row, delete_col, CellType.EMPTY)  # repaint deleted cell
        self.selected_row = -1
        self.selected_col = -1

    def remove_can(self):
        for i in range(len(self.can_row)):
            row = self.can_row.pop()
            col = self.can_col.pop()
            self.table[row][col] = CellType.EMPTY
            self.repaint_cell(row, col, CellType.EMPTY)

    def show_table(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = self.table[i][j]
                self.setCellWidget(i, j, self.get_block(item))

    def repaint_cell(self, row, col, cell_type: CellType):
        self.table[row][col] = cell_type
        self.setCellWidget(row, col, self.get_block(cell_type))

    def get_block(self, cell_type: CellType) -> QLabel:
        item = QLabel()
        match cell_type:
            case CellType.EMPTY:
                item.setStyleSheet("background-color: white;")
            case CellType.BLOCK:
                item.setStyleSheet("background-color: red;")
            case CellType.CAN:
                item.setStyleSheet("background-color: green;")
            case CellType.SELECTED:
                item.setStyleSheet("background-color: purple;")
        return item
