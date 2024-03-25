import json


class Settings:
    def __init__(self, file):
        self.settings = json.load(open(file))['settings']

    def set_size(self, size: int):
        self.settings['size'] = size

    def get_size(self) -> int:
        return self.settings['size']

    def get_x_indent(self) -> int:
        return self.settings['x_indent']

    def get_y_indent(self) -> int:
        return self.settings['y_indent']

    def get_score(self) -> int:
        return self.settings['score_by_one']
