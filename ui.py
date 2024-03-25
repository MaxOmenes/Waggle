from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QPushButton, QFileDialog, QLineEdit, QLabel
from table import Table
from menu import Menu
import json
from game import Game
from settings import Settings
from game_status import GameStatus


class UiForm(QMainWindow):
    def __init__(self):
        super().__init__()
        menu = Menu(self)
        self.table = None
        self.game = None
        self.settings = Settings('waggle/settings.json')
        self.layout = QVBoxLayout()
        self.setMenuBar(menu)
        self.score = QLabel('Score: 0')
        self.layout.addWidget(self.score)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


    def set_score(self, score: int):
        self.score.setText(f'Score: {score}')

    def load_level(self):
        dialog = QFileDialog()
        dialog.setNameFilter('JSON files (*.json)')
        dialog.exec()

        file_name = dialog.selectedFiles()[0]
        json_file = open(file_name)  # open file dialog
        level = json.load(json_file)
        json_file.close()

        self.game = Game(level, self.settings)
        self.setGeometry(100, 100,
                         len(level[0]) * self.settings.get_size() + self.settings.get_x_indent(),
                         len(level) * self.settings.get_size() + self.settings.get_y_indent())
        self.layout.addWidget(self.game.get_table())
        self.game.get_table().clicked.connect(lambda: self.label_event())

    def restart(self):
        self.layout.removeWidget(self.game.get_table())
        self.game.restart()
        self.layout.addWidget(self.game.get_table())

    def change_settings(self):
        self.game.change_settings()

    def label_event(self):
        match self.game.status:
            case GameStatus.PLAYING:
                self.set_score(self.game.get_score())
            case GameStatus.WIN:
                self.score.setStyleSheet('color: green;')
                self.score.setText('You win!')
            case GameStatus.LOSE:
                self.score.setStyleSheet('color: red;')
                self.score.setText('You lose!')


class SettingsForm(QMainWindow):
    def __init__(self, ui: UiForm):
        super().__init__()
        self.settings = ui.settings
        self.ui = ui
        self.layout = QVBoxLayout()
        current_size = self.settings.get_size()
        size_field = QLineEdit(str(current_size))
        self.layout.addWidget(size_field)
        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda: self.save(int(size_field.text())))

        self.layout.addWidget(save_button)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 200, 200)

    def save(self, size: int):
        self.settings.set_size(size)
        self.ui.change_settings()
        self.close()