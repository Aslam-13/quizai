import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.quiz import QuizResponse

load_dotenv()
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.getenv("OPEN_AI_API_KEY"),
)
 

SYSTEM_PROMPT = "You are a skilled educator generating high-quality quizzes."

def build_level_1_prompt(topic: str, num_questions: int) -> str:
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
- Start with easy questions and gradually get harder
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

async def generate_level_1_quiz(topic: str, num_questions: int) -> QuizResponse:
    prompt = build_level_1_prompt(topic, num_questions)

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    json_content = response.choices[0].message.content
    parsed = json.loads(json_content)
    return QuizResponse(**parsed)