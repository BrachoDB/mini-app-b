from uuid import uuid4

CATEGORIES = [
    {"id": "ciencia", "name": "Ciencia"},
    {"id": "historia", "name": "Historia"},
    {"id": "geografia", "name": "Geografía"},
    {"id": "tecnologia", "name": "Tecnología"},
]

QUESTIONS = [
    {
        "id": "ciencia-1",
        "category": "ciencia",
        "question": "¿Cuál es el planeta más cercano al Sol?",
        "options": ["Venus", "Mercurio", "Marte", "Tierra"],
        "correct_option": 1,
        "explanation": "Mercurio es el planeta cuya órbita está más cerca del Sol.",
    },
    {
        "id": "ciencia-2",
        "category": "ciencia",
        "question": "¿Qué gas absorben principalmente las plantas?",
        "options": ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Helio"],
        "correct_option": 2,
        "explanation": "Las plantas absorben dióxido de carbono durante la fotosíntesis.",
    },
    {
        "id": "ciencia-3",
        "category": "ciencia",
        "question": "¿Cuál es la unidad básica de los seres vivos?",
        "options": ["El átomo", "La célula", "El tejido", "El órgano"],
        "correct_option": 1,
        "explanation": "La célula es la unidad estructural y funcional básica de la vida.",
    },
    {
        "id": "historia-1",
        "category": "historia",
        "question": "¿En qué año llegó Cristóbal Colón a América?",
        "options": ["1492", "1521", "1453", "1500"],
        "correct_option": 0,
        "explanation": "La expedición de Colón llegó a América en 1492.",
    },
    {
        "id": "historia-2",
        "category": "historia",
        "question": "¿Qué civilización construyó Machu Picchu?",
        "options": ["Maya", "Azteca", "Inca", "Muisca"],
        "correct_option": 2,
        "explanation": "Machu Picchu fue construido por la civilización inca.",
    },
    {
        "id": "historia-3",
        "category": "historia",
        "question": "¿En qué país comenzó el Renacimiento?",
        "options": ["Francia", "Italia", "Grecia", "España"],
        "correct_option": 1,
        "explanation": "El Renacimiento tuvo sus primeros centros en Italia.",
    },
    {
        "id": "geografia-1",
        "category": "geografia",
        "question": "¿Cuál es el océano más grande del planeta?",
        "options": ["Atlántico", "Índico", "Ártico", "Pacífico"],
        "correct_option": 3,
        "explanation": "El océano Pacífico es el más extenso de la Tierra.",
    },
    {
        "id": "geografia-2",
        "category": "geografia",
        "question": "¿Cuál es la capital de Japón?",
        "options": ["Kioto", "Tokio", "Osaka", "Nagoya"],
        "correct_option": 1,
        "explanation": "Tokio es la capital de Japón.",
    },
    {
        "id": "geografia-3",
        "category": "geografia",
        "question": "¿En qué continente está el desierto del Sahara?",
        "options": ["Asia", "América", "África", "Oceanía"],
        "correct_option": 2,
        "explanation": "El Sahara se extiende por el norte de África.",
    },
    {
        "id": "tecnologia-1",
        "category": "tecnologia",
        "question": "¿Qué significan las siglas CPU?",
        "options": [
            "Control de Programa Unificado",
            "Unidad Central de Procesamiento",
            "Conexión Principal de Usuario",
            "Circuito de Potencia Universal",
        ],
        "correct_option": 1,
        "explanation": "CPU corresponde a Unidad Central de Procesamiento.",
    },
    {
        "id": "tecnologia-2",
        "category": "tecnologia",
        "question": "¿Cuál de estos es un lenguaje usado para estructurar páginas web?",
        "options": ["HTML", "SQL", "Bash", "C"],
        "correct_option": 0,
        "explanation": "HTML define la estructura del contenido de una página web.",
    },
    {
        "id": "tecnologia-3",
        "category": "tecnologia",
        "question": "¿Qué dispositivo permite conectar una red local a Internet?",
        "options": ["Escáner", "Router", "Proyector", "Teclado"],
        "correct_option": 1,
        "explanation": "El router dirige el tráfico entre redes, incluida la conexión a Internet.",
    },
]

QUESTION_BY_ID = {question["id"]: question for question in QUESTIONS}
_CATEGORY_BY_ID = {category["id"]: category for category in CATEGORIES}
_QUIZZES: dict[str, dict] = {}


class InvalidCategoryError(Exception):
    pass


class QuizNotFoundError(Exception):
    pass


class InvalidTurnError(Exception):
    pass


class InvalidOptionError(Exception):
    pass


class CompletedQuizError(Exception):
    pass


def get_categories() -> list[dict[str, str]]:
    return [category.copy() for category in CATEGORIES]


def _public_question(question: dict) -> dict:
    return {
        "id": question["id"],
        "question": question["question"],
        "options": question["options"].copy(),
    }


def create_quiz(category_id: str) -> dict:
    if category_id not in _CATEGORY_BY_ID:
        raise InvalidCategoryError(category_id)

    question_ids = [
        question["id"]
        for question in QUESTIONS
        if question["category"] == category_id
    ]
    quiz_id = str(uuid4())
    _QUIZZES[quiz_id] = {
        "category": category_id,
        "question_ids": question_ids,
        "position": 0,
        "score": 0,
    }

    return {
        "quiz_id": quiz_id,
        "category": _CATEGORY_BY_ID[category_id]["name"],
        "total_questions": len(question_ids),
        "question": _public_question(QUESTION_BY_ID[question_ids[0]]),
    }


def submit_answer(
    quiz_id: str, question_id: str, selected_option: int
) -> dict:
    quiz = _QUIZZES.get(quiz_id)
    if quiz is None:
        raise QuizNotFoundError(quiz_id)
    if quiz["position"] >= len(quiz["question_ids"]):
        raise CompletedQuizError(quiz_id)
    if question_id != quiz["question_ids"][quiz["position"]]:
        raise InvalidTurnError(question_id)

    question = QUESTION_BY_ID[question_id]
    if not 0 <= selected_option < len(question["options"]):
        raise InvalidOptionError(selected_option)

    correct = selected_option == question["correct_option"]
    if correct:
        quiz["score"] += 1
    quiz["position"] += 1
    completed = quiz["position"] == len(quiz["question_ids"])
    next_question = (
        None
        if completed
        else _public_question(
            QUESTION_BY_ID[quiz["question_ids"][quiz["position"]]]
        )
    )

    return {
        "correct": correct,
        "answered": quiz["position"],
        "completed": completed,
        "score": quiz["score"],
        "correct_option": question["correct_option"],
        "explanation": question["explanation"],
        "next_question": next_question,
    }
