import requests

class NoteApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def create_note(self, note_data):
        url = f"{self.base_url}/notes"
        return requests.post(url, json=note_data.__dict__ if hasattr(note_data, '__dict__') else note_data)

    def get_all_notes(self):
        url = f"{self.base_url}/notes"
        return requests.get(url)

    def get_note_by_id(self, note_id):
        url = f"{self.base_url}/notes/{note_id}"
        return requests.get(url)

    def update_note(self, note_id, update_data):
        url = f"{self.base_url}/notes/{note_id}"
        return requests.put(url, json=update_data.__dict__ if hasattr(update_data, '__dict__') else update_data)

    def delete_note(self, note_id):
        url = f"{self.base_url}/notes/{note_id}"
        return requests.delete(url)