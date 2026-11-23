from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_questions_endpoint_returns_five_public_questions_by_default():
    response = client.get("/api/preguntas")

    assert response.status_code == 200
    questions = response.json()
    assert len(questions) == 5
    assert all(set(question) == {"id", "texto", "opciones"} for question in questions)
    assert all(len(question["opciones"]) == 4 for question in questions)
    assert questions[0]["id"] == "ciencia-1"
    assert questions[0]["texto"] == "¿Cuál es el planeta más cercano al Sol?"
    assert questions[0]["opciones"] == ["Venus", "Mercurio", "Marte", "Tierra"]


def test_questions_endpoint_returns_requested_number():
    response = client.get("/api/preguntas?cantidad=2")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "ciencia-1",
            "texto": "¿Cuál es el planeta más cercano al Sol?",
            "opciones": ["Venus", "Mercurio", "Marte", "Tierra"],
        },
        {
            "id": "ciencia-2",
            "texto": "¿Qué gas absorben principalmente las plantas?",
            "opciones": [
                "Oxígeno",
                "Nitrógeno",
                "Dióxido de carbono",
                "Helio",
            ],
        },
    ]


def test_questions_endpoint_rejects_amount_outside_supported_range():
    assert client.get("/api/preguntas?cantidad=0").status_code == 422
    assert client.get("/api/preguntas?cantidad=6").status_code == 422


def test_homepage_can_start_a_quiz_with_selected_question_count():
    homepage = client.get("/")
    quiz = client.post(
        "/api/quizzes",
        json={"category": "ciencia", "cantidad": 4},
    )

    assert homepage.status_code == 200
    assert 'id="question-quantity"' in homepage.text
    assert quiz.status_code == 200
    assert quiz.json()["total_questions"] == 4
    assert quiz.json()["question"]["id"] == "ciencia-1"
