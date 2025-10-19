import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.schemas.quiz import QuizResponse

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
 

SYSTEM_PROMPT = "You are a skilled educator generating high-quality quizzes."

def build_prompt(topic: str, num_questions: int, version: int) -> str:
    return f"""
You are a skilled educator generating quizzes for learners.

Create a JSON object containing a set of questions on the topic: "{topic}".

Generate a balanced mix of the following question types:
- MCQs (single correct)
- MCQs with multiple correct answers
- Fill-in-the-blanks
- True/False

The quiz should:
- Contain {num_questions} questions (2–3 from each type)
- Start with easy questions and gradually get harder (difficulty level: {version})
- Include answer and explanation for each question
- Return only JSON in this structure:

{{
  "mcq": [
    {{
      "q": "What is ...?",
      "options": ["A", "B", "C", "D"],
      "ans": "B",
      "explain": "Brief explanation here."
    }}
  ],
  "multi_mcq": [
    {{
      "q": "Which of the following are ...?",
      "options": ["A", "B", "C", "D"],
      "ans": ["A", "C"],
      "explain": "Brief explanation here."
    }}
  ],
  "fillblanks": [
    {{
      "q": "The principle of ___ states that...",
      "ans": "Single Responsibility",
      "explain": "Brief explanation here."
    }}
  ],
  "true_false": [
    {{
      "q": "The Liskov principle allows... (True/False)",
      "ans": "False",
      "explain": "Brief explanation here."
    }}
  ]
}}
Only return valid JSON. Do not include markdown or explanations outside the object.
"""

async def generate_quiz(topic: str, num_questions: int, version: int) -> QuizResponse:
    prompt = build_prompt(topic, num_questions, version)

    response = model.generate_content(
        contents=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
            {"role": "user", "parts": [prompt]},
        ],
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
        ),
    )

    json_content = response.text
    parsed = json.loads(json_content)
    return QuizResponse(**parsed)


SYSTEM_PROMPT_SUMMARY = "You are an AI assistant that provides constructive feedback and summarizes quiz performance."

def build_summary_prompt(topic: str, correct_questions: list, incorrect_questions: list) -> str:
    correct_q_text = "\n".join([f"- {q.q} (Answer: {q.ans})" for q in correct_questions]) if correct_questions else "None"
    incorrect_q_text = "\n".join([f"- {q.q} (Correct Answer: {q.ans})" for q in incorrect_questions]) if incorrect_questions else "None"

    return f"""
Based on a quiz on the topic '{topic}', provide a concise summary of the user's performance.

Correctly Answered Questions:
{correct_q_text}

Incorrectly Answered Questions:
{incorrect_q_text}

Provide a summary that:
- Highlights areas of strength based on correct answers.
- Identifies areas for improvement based on incorrect answers.
- Suggests topics or concepts to review.
- Is no more than 200 words.
"""

async def generate_summary(topic: str, correct_questions: list, incorrect_questions: list) -> str:
    prompt = build_summary_prompt(topic, correct_questions, incorrect_questions)

    response = model.generate_content(
        contents=[
            {"role": "user", "parts": [SYSTEM_PROMPT_SUMMARY]},
            {"role": "user", "parts": [prompt]},
        ],
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
        ),
    )
    return response.text