from fastapi.testclient import TestClient

from app import QUESTION_BY_ID, QUESTIONS, app

client = TestClient(app)


def test_homepage_and_categories_are_available():
    homepage = client.get("/")
    categories = client.get("/api/categories")

    assert homepage.status_code == 200
    assert "¿Cuánto sabes" in homepage.text
    assert categories.status_code == 200
    assert {category["id"] for category in categories.json()} == {
        "ciencia",
        "historia",
        "geografia",
        "tecnologia",
    }


def test_quiz_hides_answers_until_submission_and_scores_correctly():
    quiz_response = client.post("/api/quizzes", json={"category": "ciencia"})
    assert quiz_response.status_code == 200
    quiz = quiz_response.json()
    question = quiz["question"]
    assert len(question["options"]) == 4
    assert "correct_option" not in question
    assert "explanation" not in question

    wrong_turn = client.post(
        f"/api/quizzes/{quiz['quiz_id']}/answers",
        json={"question_id": "not-the-current-question", "selected_option": 0},
    )
    assert wrong_turn.status_code == 409

    invalid_option = client.post(
        f"/api/quizzes/{quiz['quiz_id']}/answers",
        json={"question_id": question["id"], "selected_option": 99},
    )
    assert invalid_option.status_code == 422

    correct_option = QUESTION_BY_ID[question["id"]]["correct_option"]
    answer = client.post(
        f"/api/quizzes/{quiz['quiz_id']}/answers",
        json={"question_id": question["id"], "selected_option": correct_option},
    )
    assert answer.status_code == 200
    assert answer.json()["correct"] is True
    assert answer.json()["answered"] == 1
    assert answer.json()["completed"] is False
    assert answer.json()["next_question"]["id"] != question["id"]

    duplicate = client.post(
        f"/api/quizzes/{quiz['quiz_id']}/answers",
        json={"question_id": question["id"], "selected_option": correct_option},
    )
    assert duplicate.status_code == 409


def test_category_validation_and_full_quiz_completion():
    invalid_category = client.post("/api/quizzes", json={"category": "deportes"})
    assert invalid_category.status_code == 422

    quiz = client.post("/api/quizzes", json={"category": "historia"}).json()
    question = quiz["question"]
    wrong_question_id = next(
        item["id"] for item in QUESTIONS if item["id"] != question["id"]
    )
    wrong_turn = client.post(
        f"/api/quizzes/{quiz['quiz_id']}/answers",
        json={"question_id": wrong_question_id, "selected_option": 0},
    )
    assert wrong_turn.status_code == 409

    answer = None
    while True:
        correct_option = QUESTION_BY_ID[question["id"]]["correct_option"]
        answer = client.post(
            f"/api/quizzes/{quiz['quiz_id']}/answers",
            json={"question_id": question["id"], "selected_option": correct_option},
        ).json()
        if answer["completed"]:
            break
        question = answer["next_question"]

    assert answer["score"] == quiz["total_questions"]
    assert answer["answered"] == quiz["total_questions"]
    assert answer["next_question"] is None
