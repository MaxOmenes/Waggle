from PyQt6.QtWidgets import QMenuBar
import ui


class Menu(QMenuBar):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.menu = self.addMenu('Menu')
        self.menu.addAction('Load Level')
        self.menu.addAction('Restart Level')
        self.menu.addAction('Settings')
        self.menu.addAction('Exit')
        self.menu.triggered.connect(self.menu_event)

    def menu_event(self, action):
        match action.text():
            case 'Load Level':
                self.screen.load_level()
            case 'Restart Level':
                self.screen.restart()
            case 'Settings':
                settings = ui.SettingsForm(self.screen)
                settings.show()
            case 'Exit':
                self.screen.close()
