from PyQt6.QtWidgets import QApplication
from controllers.note_controller import NoteController
from views.main_window import MainWindow
from db import init_db

app = QApplication([])
init_db()

controller = NoteController()
window = MainWindow(controller)
window.show()

app.exec()