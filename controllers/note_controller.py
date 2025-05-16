import sqlite3
from datetime import datetime
from models.note import Note

class NoteController:
    def __init__(self, db_path="notes.database") -> None:
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_all_notes(self)-> list[Note]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT id, title, text, created_at, updated_at FROM notes")
            rows = cursor.fetchall()
            return [Note.from_row(row) for row in rows]

    def add_note(self, title:str, text:str)-> None:
        now = datetime.now().isoformat()
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO notes (title, text, created_at, updated_at)
                VALUES (?, ?, ?, ?)""",
                (title, text, now, now)
            )

    def update_note(self, note_id: int, values: dict) -> None:

        values["updated_at"] = datetime.now().isoformat()

        set_values = ", ".join(f"{key} = ?" for key in values.keys())

        query = f"UPDATE notes SET {set_values} WHERE id = ?"
        params = list(values.values()) + [note_id]

        with self._connect() as conn:
            conn.execute(query, params)

    def validate_note(self, title: str, note_id: int| None = None) -> None | str:
        title = title.strip()
        if not title:
            return "Название заметки не может быть пустым"
        if self.note_title_exists(title, exclude_id=note_id):
            return "Заметка с таким названием уже существует"
        return None

    def delete_note(self, note_id: int) -> None:
        query = f"DELETE FROM notes WHERE id = ?"
        with self._connect() as conn:
            conn.execute(query, (note_id, ))

    def search_notes_by_title(self, title: str) -> list[Note]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, title, text, created_at, updated_at FROM notes WHERE title LIKE ?",
                (f"%{title}%",)
            )
            rows = cursor.fetchall()
            return [Note.from_row(row) for row in rows]

    def get_all_notes(self, sort_by: str ="created_at") -> list[Note]:
        if sort_by not in ("created_at", "updated_at"):
            sort_by = "created_at"

        with self._connect() as conn:
            cursor = conn.execute(f"""
                SELECT id, title, text, created_at, updated_at
                FROM notes
                ORDER BY {sort_by} DESC
            """)
            rows = cursor.fetchall()
            return [Note.from_row(row) for row in rows]

    def note_title_exists(self, title: str, exclude_id: int | None = None) -> bool:
        params = [title]
        condition = "AND id != ?" if exclude_id is not None else ""
        if exclude_id is not None:
            params.append(exclude_id)

        query = f"SELECT COUNT(*) FROM notes WHERE title = ? {condition}"

        with self._connect() as conn:
            (count,) = conn.execute(query, params).fetchone()
            return count > 0

