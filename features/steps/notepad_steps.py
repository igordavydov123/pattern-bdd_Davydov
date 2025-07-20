import requests
from behave import given, when, then
import json

def create_note(context, title, content):
    payload = {"title": title, "content": content}
    response = requests.post(
        f"{context.base_url}/notes",
        headers=context.headers,
        data=json.dumps(payload),
    )
    if response.status_code == 201:
        note_id = response.json()["id"]
        context.notes.append(note_id)
    return response

# Note creation
@given('I have a valid note payload')
def step_impl(context):
    context.payload = {"title": "Test Note", "content": "This is a test note"}

@given('I have an invalid note payload')
def step_impl(context):
    context.payload = {"title": "", "content": ""}  # Invalid empty data

@when('I send a POST request to "/notes"')
def step_impl(context):
    context.response = requests.post(
        f"{context.base_url}/notes",
        headers=context.headers,
        data=json.dumps(context.payload))

@then('the response status code should be {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code}, got {context.response.status_code}"

@then('the response should contain the created note data')
def step_impl(context):
    response_data = context.response.json()
    assert "id" in response_data, "Response missing note ID"
    assert response_data["title"] == context.payload["title"]
    assert response_data["content"] == context.payload["content"]

# Getting notes list
@given('there are no notes in the system')
def step_impl(context):
    # Clean up any existing notes
    response = requests.get(f"{context.base_url}/notes")
    if response.status_code == 200:
        for note in response.json():
            requests.delete(f"{context.base_url}/notes/{note['id']}")

@given('there are 2 notes in the system')
def step_impl(context):
    # Create 2 test notes
    create_note(context, "Note 1", "Content 1")
    create_note(context, "Note 2", "Content 2")

@when('I send a GET request to "/notes"')
def step_impl(context):
    context.response = requests.get(f"{context.base_url}/notes")

@then('the response should be an empty list')
def step_impl(context):
    assert context.response.json() == [], "Response should be empty list"

@then('the response should contain {count} notes')
def step_impl(context, count):
    assert len(context.response.json()) == int(count), \
        f"Expected {count} notes, got {len(context.response.json())}"

# Getting note by ID
@given('there is a note in the system')
def step_impl(context):
    context.response = create_note(context, "Test Note", "Test Content")
    context.note_id = context.response.json()["id"]

@when('I get the note by its ID')
def step_impl(context):
    context.response = requests.get(
        f"{context.base_url}/notes/{context.note_id}")

@when('I get the note with ID "{note_id}"')
def step_impl(context, note_id):
    context.response = requests.get(f"{context.base_url}/notes/{note_id}")

@then('the response should contain the note data')
def step_impl(context):
    response_data = context.response.json()
    assert "id" in response_data, "Response missing note ID"
    assert "title" in response_data, "Response missing title"
    assert "content" in response_data, "Response missing content"

# Updating a note
@when('I update the note with valid data')
def step_impl(context):
    context.update_payload = {
        "title": "Updated Title",
        "content": "Updated Content"
    }
    context.response = requests.put(
        f"{context.base_url}/notes/{context.note_id}",
        headers=context.headers,
        data=json.dumps(context.update_payload))

@when('I update the note with ID "{note_id}"')
def step_impl(context, note_id):
    context.response = requests.put(
        f"{context.base_url}/notes/{note_id}",
        headers=context.headers,
        data=json.dumps({"title": "Test", "content": "Test"}))

@then('the response should contain updated data')
def step_impl(context):
    response_data = context.response.json()
    assert response_data["title"] == context.update_payload["title"]
    assert response_data["content"] == context.update_payload["content"]

# Deleting a note
@when('I delete the note by its ID')
def step_impl(context):
    context.response = requests.delete(
        f"{context.base_url}/notes/{context.note_id}")

@when('I delete the note with ID "{note_id}"')
def step_impl(context, note_id):
    context.response = requests.delete(f"{context.base_url}/notes/{note_id}")

@then('the note should be deleted')
def step_impl(context):
    # Verify the note no longer exists
    response = requests.get(f"{context.base_url}/notes/{context.note_id}")
    assert response.status_code == 404, "Note was not deleted"