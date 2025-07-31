import sqlite3
import re

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()


def get_db_cursor_and_connection():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    return cursor, conn


# Создание таблицы reviews в случае если она не была создана
def init_db():
    cursor, conn = get_db_cursor_and_connection()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


class ReviewRequest(BaseModel):
    text: str


# Модель ответа
class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str


# сохранение отзыва
@app.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewRequest):
    sentiment = simple_analyze_sentiment(review.text)
    created_at = datetime.utcnow().isoformat()

    cursor, conn = get_db_cursor_and_connection()
    cursor.execute(
        "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
        (review.text, sentiment, created_at)
    )
    review_id = cursor.lastrowid
    conn.commit()

    cursor.execute(
        "SELECT id, text, sentiment, created_at FROM reviews WHERE id = ?",
        (review_id,)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=500, detail="Не удалось сохранить отзыв")

    return ReviewResponse(id=result[0], text=result[1], sentiment=result[2], created_at=result[3])


# получение отзывов с оценкой
@app.get("/reviews", response_model=List[ReviewResponse])
def get_reviews(sentiment: str = None):
    cursor, conn = get_db_cursor_and_connection()

    query_str = "SELECT id, text, sentiment, created_at FROM reviews "
    if sentiment:
        query_str += "WHERE sentiment = ?"
        cursor.execute(query_str, (sentiment,))
    else:
        cursor.execute(query_str)

    reviews = cursor.fetchall()
    conn.close()

    return [
        ReviewResponse(
            id=row[0],
            text=row[1],
            sentiment=row[2],
            created_at=row[3]
        )
        for row in reviews
    ]


# Адаптация анализа тональности
def simple_analyze_sentiment(text: str) -> str:
    positive_weight, negative_weight = analyze_sentiment(text)
    if positive_weight:
        return 'positive'
    if negative_weight:
        return 'negative'
    return 'neutral'


POSITIVE_TERMS = ("хорош", "люблю")
NEGATIVE_TERMS = ("плохо", "ненавижу")


# Функция анализа тональности
def analyze_sentiment(text: str) -> str:
    """
      Функция анализа тональности. Производит подсчет вхождений позитивных и негативных слов из словарей.
    :param text: текст для анализа
    :return: tuple(количество позитивных слов, количество негативных слов)
    """
    text_lower = text.lower()


    positive_weight = 0
    negative_weight = 0

    for word in POSITIVE_TERMS:
        positive_weight += len(re.findall(word, text_lower))

    for word in NEGATIVE_TERMS:
        negative_weight += len(re.findall(word, text_lower))

    return positive_weight, negative_weight
