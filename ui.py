from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QPushButton, QFileDialog
from table import Table
from menu import Menu
import json
from game import Game


class UiForm(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = Menu(self)
        self.table = None
        self.game = None
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
        level = json.load(json_file)
        json_file.close()

        self.game = Game(level)

        self.layout.addWidget(self.game.get_table())
