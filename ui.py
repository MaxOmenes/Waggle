from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QPushButton, QFileDialog
from table import Table
from menu import Menu
import json


class UiForm(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = Menu(self)
        self.level = None
        self.table = None
        self.layout = QVBoxLayout()
        self.setMenuBar(menu)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def load_level(self):
        dialog = QFileDialog()
        dialog.setNameFilter('JSON files (*.json)')
        dialog.exec()

        file_name = dialog.selectedFiles()[0]
        json_file = open(file_name)  # open file dialog
        self.level = json.load(json_file)
        json_file.close()

        self.table = Table(self.level)
        self.table.show_table()
        self.layout.addWidget(self.table)
