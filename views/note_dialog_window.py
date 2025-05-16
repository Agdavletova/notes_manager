from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QDialogButtonBox, QMessageBox
)
from models.note import Note
from controllers.note_controller import NoteController
class NoteDialog(QDialog):
    def __init__(self, parent: QDialog | None = None, note: Note | None = None, controller: NoteController | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Заметка")

        self.note = note
        self.controller = controller

        self.title_edit = QLineEdit()
        self.title_edit.setMaxLength(50)
        self.text_edit = QTextEdit()

        if note:
            self.title_edit.setText(note.title)
            self.text_edit.setText(note.text)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Текст заметки:"))
        layout.addWidget(self.text_edit)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.save_note)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_data(self) -> tuple[str, str]:
        return self.title_edit.text(), self.text_edit.toPlainText()

    def save_note(self) -> None:
        title = self.title_edit.text().strip()
        text = self.text_edit.toPlainText().strip()

        error = self.controller.validate_note(title, note_id=self.note.id if self.note else None)
        if error:
            QMessageBox.warning(self, "Ошибка", error)
            return

        if self.note is None:
            self.controller.add_note(title, text)
        else:
            self.controller.update_note(self.note.id, {"title": title, "text": text})

        self.accept()
