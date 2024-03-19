from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QTableWidget
from table import Table


class UiForm(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        table = Table([[0, 1, 2], [1, 2, 0], [2, 0, 1]])
        table.show_table()
        layout.addWidget(table)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def load_level(self):
        pass
