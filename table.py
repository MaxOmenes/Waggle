from PyQt6.QtWidgets import QTableWidget, QLabel
from PyQt6.QtCore import pyqtSignal, QEvent, Qt
from enum import Enum

class CellType(Enum):
    EMPTY = 0
    BLOCK = 1
    CAN = 2
class Table(QTableWidget):
    keyPressed = pyqtSignal(QEvent)

    def __init__(self, table:list[list[int]]):
        super().__init__(len(table), len(table[0]))
        self.table = table
        self.cellClicked.connect(self.cell_event)
        self.show_table()

    def cell_event(self, row, col):
        match self.table[row][col]:
            case CellType.EMPTY:
                pass
            case CellType.BLOCK:
                print(f"Block at {row}, {col}")
            case CellType.CAN:
                self.table[row][col] = CellType.EMPTY


    def show_table(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = self.table[i][j]
                self.setCellWidget(i, j, self.get_block(item))

    def get_block(self, cell_type:int) -> QLabel:
        item = QLabel(self)
        match cell_type:
            case CellType.EMPTY:
                item.setStyleSheet("background-color: white;")
            case CellType.BLOCK:
                item.setStyleSheet("background-color: red;")
            case CellType.CAN:
                item.setStyleSheet("background-color: green;")
        return item
