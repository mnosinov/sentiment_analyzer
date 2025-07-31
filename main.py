import sqlite3

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
    sentiment = analyze_sentiment(review.text)
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


# Функция анализа тональности
def analyze_sentiment(text: str) -> str:
    # TODO
    return 'positive'
    return 'negative'
    return 'neutral'


