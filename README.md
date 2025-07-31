# Review Sentiment Analyzer - FastAPI

To install all dependencies:
```commandline
pip install -r requirements.txt
```

To run web server:
```commandline
uvicorn main:app --reload
```

### Sample curl-requests and responses:

<b>Create review:</b>
<br>
Request:
```commandline
curl -X 'POST' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "какой-то хороший не плохой текст"
}'
```
Response:
```
code: 200
body:
{
  "id": 6,
  "text": "какой-то хороший не плохой текст",
  "sentiment": "positive",
  "created_at": "2025-07-31T08:36:45.417194"
}
```

<b>Get all positive reviews:</b>
<br>
Request:
```commandline
curl -X 'GET' \
  'http://127.0.0.1:8000/reviews?sentiment=positive' \
  -H 'accept: application/json'
```
Response:
```
[
  {
    "id": 1,
    "text": "какой-то хорош текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T07:50:05.353712"
  },
  {
    "id": 2,
    "text": "какой-то хороший текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T07:50:27.110389"
  },
  {
    "id": 5,
    "text": "какой-то хороший текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T08:25:48.794924"
  },
  {
    "id": 6,
    "text": "какой-то хороший не плохой текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T08:36:45.417194"
  }
]
```
<b>Get all reviews:</b>
<br>
Request:
```commandline
curl -X 'GET' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json'
```
Response:
```
[
  {
    "id": 1,
    "text": "какой-то хорош текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T07:50:05.353712"
  },
  {
    "id": 2,
    "text": "какой-то хороший текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T07:50:27.110389"
  },
  {
    "id": 3,
    "text": "какой-то плохой текст",
    "sentiment": "neutral",
    "created_at": "2025-07-31T08:19:20.435291"
  },
  {
    "id": 4,
    "text": "какой-то плохой текст",
    "sentiment": "negative",
    "created_at": "2025-07-31T08:25:30.843311"
  },
  {
    "id": 5,
    "text": "какой-то хороший текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T08:25:48.794924"
  },
  {
    "id": 6,
    "text": "какой-то хороший не плохой текст",
    "sentiment": "positive",
    "created_at": "2025-07-31T08:36:45.417194"
  }
]
```
