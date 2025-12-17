# learning_platform/models.py

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    def __init__(self, id, username, full_name=None):
        self.id = id
        self.username = username
        self.full_name = full_name



@dataclass
class Course:
    id: int
    title: str
    description: str | None


@dataclass
class Lesson:
    id: int
    course_id: int
    title: str
    content: str | None
    order_index: int


@dataclass
class Question:
    id: int
    lesson_id: int
    question_text: str


@dataclass
class Answer:
    id: int
    question_id: int
    answer_text: str
    is_correct: bool


@dataclass
class TestAttempt:
    id: int
    user_id: int
    lesson_id: int
    correct_answers: int
    total_questions: int
    finished_at: datetime | None
