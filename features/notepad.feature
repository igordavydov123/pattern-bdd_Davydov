Feature: Note Management API
  As a user
  I want to interact with notes API
  So that I can manage my notes

  # Создание заметок
  Scenario: Successfully create a note with valid data
    Given I have a valid note payload
    When I send a POST request to "/notes"
    Then the response status code should be 200
    And the response should contain the created note data

  Scenario: Fail to create a note with invalid data
    Given I have an invalid note payload
    When I send a POST request to "/notes"
    Then the response status code should be 422

  # Получение списка заметок
  Scenario: Get empty notes list when no notes exist
    Given there are no notes in the system
    When I send a GET request to "/notes"
    Then the response status code should be 200
    And the response should be an empty list

  Scenario: Get all notes when notes exist
    Given there are 2 notes in the system
    When I send a GET request to "/notes"
    Then the response status code should be 200
    And the response should contain 2 notes

  # Получение заметки по ID
  Scenario: Get note by valid ID
    Given there is a note in the system
    When I get the note by its ID
    Then the response status code should be 200
    And the response should contain the note data

  Scenario: Fail to get note by invalid ID
    Given there are no notes in the system
    When I get the note with ID "999"
    Then the response status code should be 404

  # Редактирование заметки
  Scenario: Update note by valid ID
    Given there is a note in the system
    When I update the note with valid data
    Then the response status code should be 200
    And the response should contain updated data

  Scenario: Fail to update note by invalid ID
    Given there are no notes in the system
    When I update the note with ID "999"
    Then the response status code should be 404

  # Удаление заметки
  Scenario: Delete note by valid ID
    Given there is a note in the system
    When I delete the note by its ID
    Then the response status code should be 200
    And the note should be deleted

  Scenario: Fail to delete note by invalid ID
    Given there are no notes in the system
    When I delete the note with ID "999"
    Then the response status code should be 404