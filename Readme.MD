# QuizAI - AI-Powered Quiz Application

## Overview

QuizAI is a personal AI-powered quiz app designed to help users learn and reinforce knowledge on various topics. By providing a topic or subtopics, the app generates a series of quiz-style questions, such as multiple-choice questions (MCQs), true/false, and fill-in-the-blanks. The questions are designed to start with basic concepts and gradually increase in difficulty, ensuring an effective learning experience.

## Features

- **Adaptive Questioning**: Questions start simple and progressively become more challenging.
- **Interactive Learning**: Users answer 5–10 questions at a time, with feedback provided before continuing.
- **Customizable Topics**: Learn about anything, from "SOLID principles in Java" to "PostgreSQL indexing."

## Tech Stack

### Frontend
- **Next.js with TypeScript**: For building a fast and interactive user interface.
- **Zustand**: Lightweight state management.
- **TanStack Query**: Efficient data fetching and caching.
- **TailwindCSS or Plain CSS**: For styling (optional).

### Backend
- **FastAPI (Python)**: Robust API development.
- **PostgreSQL**: Database for storing user progress, scores, and topic history.

### AI Model & Infrastructure
- **Groq Cloud**: High-performance infrastructure for AI workloads.
- **Qwen-32B-Instruct**: Advanced LLM for generating quiz questions tailored to user needs.

## How It Works

1. **Choose a Topic**: Select a topic or subtopics you want to learn.
2. **Quiz Generation**: The AI generates a series of questions to test and reinforce your knowledge.
3. **Answer & Learn**: Respond to 5–10 questions at a time, receive feedback, and continue learning.

## Example Topics
- SOLID principles in Java
- Python decorators
- PostgreSQL indexing

## Getting Started

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/quizai.git
  cd quizai
  ```

2. Install dependencies:
  ```bash
  # Frontend
  cd frontend
  npm install

  # Backend
  cd ../backend
  pip install -r requirements.txt
  ```

3. Run the application:
  ```bash
  # Frontend
  cd frontend
  npm run dev

  # Backend
  cd ../backend
  uvicorn main:app --reload
  ```

4. Open your browser and start learning!

## First Topic
{{your topic here}}

Generate the first round of quiz questions and begin your learning journey!
