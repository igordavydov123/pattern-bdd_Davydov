from behave import given, when, then
from note_factories import NoteFactory
from note_api import NoteApiClient
import json

api_client = NoteApiClient()

@given('I have a valid note payload')
def step_impl(context):
    context.note_data = NoteFactory.create_valid_note()

@given('I have an invalid note payload')
def step_impl(context):
    context.note_data = NoteFactory.create_invalid_note()

@given('there are no notes in the system')
def step_impl(context):
    # Очищаем все заметки (если API поддерживает)
    response = api_client.get_all_notes()
    if response.status_code == 200:
        for note in response.json():
            api_client.delete_note(note['id'])

@given('there are {count} notes in the system')
def step_impl(context, count):
    for _ in range(int(count)):
        api_client.create_note(NoteFactory.create_valid_note())

@given('there is a note in the system')
def step_impl(context):
    response = api_client.create_note(NoteFactory.create_valid_note())
    assert response.status_code == 201
    context.note_id = response.json()['id']

@when('I send a POST request to "/notes"')
def step_impl(context):
    context.response = api_client.create_note(context.note_data)

@when('I send a GET request to "/notes"')
def step_impl(context):
    context.response = api_client.get_all_notes()

@when('I get the note by its ID')
def step_impl(context):
    context.response = api_client.get_note_by_id(context.note_id)

@when('I get the note with ID "{note_id}"')
def step_impl(context, note_id):
    context.response = api_client.get_note_by_id(note_id)

@when('I update the note with valid data')
def step_impl(context):
    update_data = NoteFactory.create_valid_note()
    update_data.title = "Updated Title"
    context.response = api_client.update_note(context.note_id, update_data)

@when('I update the note with ID "{note_id}"')
def step_impl(context, note_id):
    update_data = NoteFactory.create_valid_note()
    context.response = api_client.update_note(note_id, update_data)

@when('I delete the note by its ID')
def step_impl(context):
    context.response = api_client.delete_note(context.note_id)

@when('I delete the note with ID "{note_id}"')
def step_impl(context, note_id):
    context.response = api_client.delete_note(note_id)

@then('the response status code should be {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then('the response should contain the created note data')
def step_impl(context):
    response_data = context.response.json()
    assert 'id' in response_data
    assert response_data['title'] == context.note_data.title
    assert response_data['content'] == context.note_data.content

@then('the response should be an empty list')
def step_impl(context):
    assert context.response.json() == []

@then('the response should contain {count} notes')
def step_impl(context, count):
    assert len(context.response.json()) == int(count)

@then('the response should contain the note data')
def step_impl(context):
    response_data = context.response.json()
    assert 'id' in response_data
    assert 'title' in response_data
    assert 'content' in response_data

@then('the response should contain updated data')
def step_impl(context):
    response_data = context.response.json()
    assert response_data['title'] == "Updated Title"

@then('the note should be deleted')
def step_impl(context):
    response = api_client.get_note_by_id(context.note_id)
    assert response.status_code == 404