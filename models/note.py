
class Note:
    def __init__(self, id: int, title: str, text: str, created_at: str, updated_at: str) -> None:
        self.id = id
        self.title = title
        self.text = text
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_row(cls, row: tuple):
        return cls(
            id=row[0],
            title=row[1],
            text=row[2],
            created_at=row[3],
            updated_at=row[4]
        )