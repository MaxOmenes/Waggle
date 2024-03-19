import sys
from PyQt6.QtWidgets import QApplication
from ui import UiForm

app = QApplication(sys.argv)
window = UiForm()
window.show()
app.exec()

