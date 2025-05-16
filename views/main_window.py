from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QComboBox, QTableView, QMessageBox, QLineEdit, QLabel
from models.note_table import NoteTableModel
from .note_dialog_window import NoteDialog
from PyQt6.QtWidgets import QPushButton
from controllers.note_controller import NoteController
class MainWindow(QMainWindow):
    def __init__(self, controller: NoteController) -> None:
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Менеджер заметок")
        self.resize(800, 600)

        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.on_search)

        self.table_view = QTableView()
        self.create_btn = QPushButton("Создать")
        self.delete_btn = QPushButton("Удалить")
        self.edit_btn = QPushButton("Редактировать")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["По дате создания", "По дате обновления"])
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        self.theme_toggle_btn = QPushButton("Тёмная тема")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Поиск:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.sort_combo)

        layout.addWidget(self.table_view)
        layout.addWidget(self.create_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.theme_toggle_btn)

        self.current_theme = "light"
        self.set_light_theme()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_notes()

        self.create_btn.clicked.connect(self.on_create_note)
        self.edit_btn.clicked.connect(self.on_edit_note)
        self.delete_btn.clicked.connect(self.on_delete_note)

    def load_notes(self) -> None:
        notes = self.controller.get_all_notes()
        self.model = NoteTableModel(notes)
        self.table_view.setModel(self.model)

    def on_create_note(self) -> None:
        dialog = NoteDialog(self, controller=self.controller)
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec():
            self.load_notes()

    def on_edit_note(self) -> None:
        index = self.table_view.currentIndex()
        note = self.model.get_note_by_row(index.row())
        dialog = NoteDialog(self, note=note, controller=self.controller)
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec():
            values = {}
            title, text = dialog.get_data()
            if title != note.title:
                values["title"] = title
            if text != note.text:
                values["text"] = text

            self.controller.update_note(note_id=note.id, values=values)
            self.load_notes()

    def on_delete_note(self) -> None:
        index = self.table_view.currentIndex()
        note = self.model.get_note_by_row(index.row())
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Удалить заметку '{note.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_note(note.id)
            self.load_notes()

    def on_search(self, text: str) -> None:
        filtered_notes = self.controller.search_notes_by_title(text)
        self.model = NoteTableModel(filtered_notes)
        self.table_view.setModel(self.model)

    def on_sort_changed(self, index: int) -> None:
        if index == 0:
            sort_by = "created_at"
        else:
            sort_by = "updated_at"
        notes = self.controller.get_all_notes(sort_by=sort_by)
        self.model = NoteTableModel(notes)
        self.table_view.setModel(self.model)

    def toggle_theme(self) -> None:
        if self.current_theme == "light":
            self.set_dark_theme()
            self.current_theme = "dark"
            self.theme_toggle_btn.setText("Светлая тема")
        else:
            self.set_light_theme()
            self.current_theme = "light"
            self.theme_toggle_btn.setText("Тёмная тема")

    def set_dark_theme(self) -> None:
        self.current_style = """
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
                font-size: 14px;
            }

            QTableView {
                background-color: #2e2e2e;
                gridline-color: #555;
                selection-background-color: #505050;
                selection-color: #fff;
                border: 1px solid #ccc;
            }

            QHeaderView {
                background-color: #2e2e2e;
            }

            QHeaderView::section {
                background-color: #3a3a3a;
                color: #ffffff;
                padding: 6px;
                border: 1px solid #444;
                font-weight: bold;
                
            }

            QTableCornerButton::section {
                background-color: #3a3a3a;
                border: 1px solid #444;
            }

            QPushButton, QDialogButtonBox QPushButton {
                background-color: #444;
                color: #fff;
                border-radius: 12px;
                padding: 8px 16px;
                margin: 4px;
                
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #3c3c3c;
                color: #fff;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 6px;
                margin-bottom: 8px;
            }

            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #fff;
                selection-background-color: #505050;
            }
        """
        self.setStyleSheet(self.current_style)

    def set_light_theme(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-size: 14px;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #aaa;
                border-radius: 8px;
                padding: 6px;
                margin-bottom: 8px;
            }

            QTableView {
                background-color: #ffffff;
                gridline-color: #ccc;
                selection-background-color: #e0e0e0;
                selection-color: #000;
                border: 1px solid #ccc;
            }

            QHeaderView::section {
                background-color: #f0f0f0;
                color: #000000;
                padding: 6px;
                border: 1px solid #dcdcdc;
                font-weight: bold;
                
            }

            QTableCornerButton::section {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
                
            }
            
            QPushButton, QDialogButtonBox QPushButton {
                background-color: #f5f5f5;
                color: #000000;
                border-radius: 12px;
                padding: 8px 16px;
                margin: 4px;
                
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                selection-background-color: #e0e0e0;
                color: #000000;
            }
        """)


