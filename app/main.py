from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request

from .servicios import (
    CompletedQuizError,
    InvalidCategoryError,
    InvalidOptionError,
    InvalidTurnError,
    QuizNotFoundError,
    create_quiz,
    get_categories,
    get_questions,
    submit_answer,
)

app = FastAPI(title="Trivia de cultura general")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


class QuizRequest(BaseModel):
    category: str
    cantidad: int = Field(default=3, ge=1, le=5)


class AnswerRequest(BaseModel):
    question_id: str
    selected_option: int = Field(ge=0, le=3)


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/api/categories")
def categories() -> list[dict[str, str]]:
    return get_categories()


@app.get("/api/preguntas")
def questions(cantidad: int = Query(default=5, ge=1, le=5)) -> list[dict]:
    return get_questions(cantidad)


@app.post("/api/quizzes")
def start_quiz(payload: QuizRequest) -> dict:
    try:
        return create_quiz(payload.category, payload.cantidad)
    except InvalidCategoryError as error:
        raise HTTPException(
            status_code=422, detail="La categoría seleccionada no existe."
        ) from error


@app.post("/api/quizzes/{quiz_id}/answers")
def answer_quiz(quiz_id: str, payload: AnswerRequest) -> dict:
    try:
        return submit_answer(
            quiz_id, payload.question_id, payload.selected_option
        )
    except QuizNotFoundError as error:
        raise HTTPException(status_code=404, detail="La trivia no existe.") from error
    except (InvalidTurnError, CompletedQuizError) as error:
        raise HTTPException(
            status_code=409,
            detail="La respuesta no corresponde al turno actual de la trivia.",
        ) from error
    except InvalidOptionError as error:
        raise HTTPException(
            status_code=422, detail="La opción seleccionada no es válida."
        ) from error
