# QuizAI Backend

A FastAPI-based backend service for quiz generation and management.

## Project Structure

```
quizai-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── quiz.py
│   ├── db/
│   │   ├── models/
│   │   │   ├── fill_blank.py
│   │   │   ├── mcq.py
│   │   │   ├── mcq_multiple.py
│   │   │   └── true_false.py
│   │   ├── base.py
│   │   ├── sample_data.py
│   │   └── session.py
│   ├── routers/
│   │   └── quiz.py
│   ├── schemas/
│   │   ├── fill_blank.py
│   │   ├── mcq.py
│   │   ├── mcq_multiple.py
│   │   ├── quiz.py
│   │   └── true_false.py
│   ├── services/
│   │   └── ai.py
│   ├── create_tables.py
│   └── main.py
└── README.md
```

## Directory Overview

- `app/`: Main application directory
  - `api/`: API version management
  - `db/`: Database related files
    - `models/`: SQLAlchemy ORM models
  - `routers/`: FastAPI route handlers
  - `schemas/`: Pydantic models for request/response validation
  - `services/`: Business logic services