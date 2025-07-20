from features.steps.note_api import NoteApiClient


def before_scenario(context, scenario):
    api_client = NoteApiClient()
    response = api_client.get_all_notes()
    if response.status_code == 200:
        for note in response.json():
            api_client.delete_note(note['id'])