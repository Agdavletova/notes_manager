from PyQt6.QtCore import QAbstractTableModel, Qt
from models.note import Note

class NoteTableModel(QAbstractTableModel):
    def __init__(self, notes: list[Note]) -> None:
        super().__init__()
        self._notes = notes

    def rowCount(self, parent=None) -> int:
        return len(self._notes)

    def columnCount(self, parent=None) -> int:
        return 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            note = self._notes[index.row()]
            if index.column() == 0:
                return note.title
            elif index.column() == 1:
                return note.updated_at

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ["Название", "Обновлено"][section]

    def get_note_by_row(self, row: int) -> Note:
        return self._notes[row]

    def update_notes(self, notes: list[Note]) -> None:
        self.beginResetModel()
        self._notes = notes
        self.endResetModel()
