from PyQt6.QtWidgets import QTableWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QEvent
from cell_type import CellType, get_type


class Table(QTableWidget):
    keyPressed = pyqtSignal(QEvent)
    selected_row = -1
    selected_col = -1

    def __init__(self, table: list[list[int]]):
        super().__init__(len(table), len(table[0]))
        self.table = [[get_type(i) for i in row] for row in table]

    def get_selected(self) -> tuple[int, int]:
        return self.selected_row, self.selected_col

    def set_selected(self, row, col):
        if self.selected_row != -1:
            self.table[self.selected_row][self.selected_col] = CellType.BLOCK
        self.selected_row = row
        self.selected_col = col
        self.table[row][col] = CellType.SELECTED

    def remove_selected(self):
        self.table[self.selected_row][self.selected_col] = CellType.BLOCK
        self.selected_row = -1
        self.selected_col = -1

    def add_can(self, row, col):
        self.table[row][col] = CellType.CAN

    def set_empty(self, row, col):
        self.table[row][col] = CellType.EMPTY

    def set_block(self, row, col):
        self.table[row][col] = CellType.BLOCK

    def set_size(self, size: int):
        for i in range(len(self.table)):  # set row height and column width
            self.setRowHeight(i, size)

        for i in range(len(self.table[0])):
            self.setColumnWidth(i, size)

    def show_table(self) -> None:
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                cell_type = self.table[row][col]
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
