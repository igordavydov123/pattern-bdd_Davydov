from dataclasses import dataclass

@dataclass
class NoteData:
    title: str
    content: str

class NoteFactory:
    @staticmethod
    def create_valid_note():
        return NoteData(title="Valid Note", content="This is a valid note content")

    @staticmethod
    def create_invalid_note():
        return NoteData(title=4444, content=5555)

    @staticmethod
    def create_note_with_missing_fields():
        return {"title": "Only Title"}