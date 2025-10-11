# QuizAI Backend

A FastAPI-based backend service for quiz generation and management.

## Core Concepts

This project uses a modern Python stack for building robust and scalable APIs. Here are some of the core concepts and design choices:

### SQLModel vs. SQLAlchemy

- **SQLAlchemy** is a powerful, low-level SQL toolkit and Object-Relational Mapper (ORM). It is the engine that handles all database communication.
- **SQLModel** is a library built on top of SQLAlchemy and Pydantic. It's a "convenience layer" that simplifies development by allowing you to define your database structure and your API data shapes in a single, clear class.
- **Why SQLModel?** We use SQLModel to reduce code duplication. Instead of defining a SQLAlchemy class for the database and a separate Pydantic class for API validation, SQLModel combines them. This leads to less code, fewer bugs, and better editor support with autocompletion.

### Models vs. Schemas

This project intentionally separates database models from API schemas. This is a critical design pattern for security and flexibility.

- **Models (`app/models/quiz_models.py`)**: This file is the **source of truth** for your data. The classes here define the exact structure of your database tables, including all columns, primary keys, foreign keys, and relationships. This is the **internal representation** of your data.

- **Schemas (`app/schemas/`)**: These files define the **API contract**. They are a "view" or a filter on your models. They control what data a user can send to your API and what data your API sends back. This is the **external representation**.
  - **Example**: A `QuizCreate` schema might only include `topic_name`, while the `QuizRead` schema includes the auto-generated `id` and `created_at` fields. This separation prevents users from providing data they shouldn't control.

## Project Structure

The project follows a standard structure for FastAPI applications.

```
quizai-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── quiz.py         # API routes for quizzes
│   ├── db/
│   │   ├── database.py             # Engine setup and session management
│   │   └── sample_data.py          # Script to populate DB with sample data
│   ├── models/
│   │   └── quiz_models.py          # SQLModel classes defining DB tables
│   ├── schemas/                    # Pydantic schemas for API validation
│   │   ├── quiz.py
│   │   └── ... (other schema files)
│   ├── services/
│   │   └── ai.py                   # Business logic (e.g., AI integration)
│   └── main.py                     # Main FastAPI application instance
├── .env                            # Environment variables (needs to be created)
├── requirements.txt                # Project dependencies
└── Readme.MD
```

## Setup and Running the Application

Follow these steps to get the application running locally.

### 1. Create and Activate Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```powershell
# Create the virtual environment
python -m venv venv

# Activate the virtual environment (for Windows PowerShell)
.\venv\Scripts\activate
```

### 2. Install Dependencies

Install all the required Python packages.

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables

The application uses a `.env` file to manage configuration, such as the database connection string.

1.  Create a file named `.env` in the root of the `quizai-backend` directory.
2.  Add the following line to it. This example uses SQLite for simplicity.

```
DATABASE_URL="sqlite+aiosqlite:///./quizai.db"
```

### 4. Create and Populate the Database

The `sample_data.py` script is designed to initialize the database. It will create all the necessary tables based on your models and then populate them with sample quizzes and questions.

Run the script as a module from the project root:

```powershell
python -m app.db.sample_data
```

### 5. Run the Server

Use `uvicorn` to run the FastAPI application.

```powershell
uvicorn app.main:app --reload
```

- `--reload`: This flag makes the server automatically restart when you make code changes.
- The API will now be running at `http://127.0.0.1:8000`.
- You can access the interactive API documentation (Swagger UI) at `http://1227.0.0.1:8000/docs`.

## Database Management

### `app/db/database.py`

This is the central file for all database-related setup.

- **`engine`**: The core SQLAlchemy engine that manages a pool of connections to the database. It is created once when the application starts.
- **`create_db_and_tables()`**: A function that connects to the database and creates all tables defined by your SQLModel classes.
- **`get_db()`**: A reusable dependency function that provides a database session for a single API request and ensures it's properly closed afterward.

### How to Get a Database Connection

In your API routes, you use FastAPI's dependency injection system to get a session from the `get_db` function. This is the standard way to interact with the database.

**Example (`app/api/v1/routes/quiz.py`):**

```python
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_db
from app.schemas.quiz import QuizRead

router = APIRouter()

@router.get("/{quiz_id}", response_model=QuizRead)
async def get_a_quiz(
    *,
    session: AsyncSession = Depends(get_db),
    quiz_id: int
):
    # You can now use the 'session' object to query the database
    # quiz = await session.get(Quiz, quiz_id)
    # return quiz
    pass
```
