import requests

def before_scenario(context, scenario):
    context.base_url = "http://127.0.0.1:8000/docs"
    context.notes = []
    context.headers = {"Content-Type": "application/json"}

def after_scenario(context, scenario):
    # Clean up created notes after each scenario
    for note_id in context.notes:
        requests.delete(f"{context.base_url}/notes/{note_id}")
