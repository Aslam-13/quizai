from fastapi import APIRouter, HTTPException
from app.schemas.quiz import QuizRequest, QuizResponse
from app.services.ai import generate_level_1_quiz

router = APIRouter()

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(payload: QuizRequest):
    try:
        quiz_json = await generate_level_1_quiz(payload.topic, payload.num_questions)
        return quiz_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


{
    "mcq": [
        {
            "q": "What does Low Level Design (LLD) primarily focus on?",
            "options": [
                "High-level business processes",
                "Detailed design of modules and components",
                "User interface design",
                "System deployment strategies"
            ],
            "ans": "Detailed design of modules and components",
            "explain": "LLD involves detailed design aspects of modules, classes, and components within the system."
        },
        {
            "q": "Which diagram is most commonly used in Low Level Design?",
            "options": [
                "Use Case Diagram",
                "Class Diagram",
                "Deployment Diagram",
                "Context Diagram"
            ],
            "ans": "Class Diagram",
            "explain": "Class diagrams depict the structure of classes and relationships, key in LLD."
        },
        {
            "q": "In Low Level Design, what is the main purpose of interfaces?",
            "options": [
                "To implement user interfaces",
                "To define contracts for classes to follow",
                "To store data persistently",
                "To manage database transactions"
            ],
            "ans": "To define contracts for classes to follow",
            "explain": "Interfaces specify methods that implementing classes must provide, promoting abstraction."
        }
    ],
    "multi_mcq": [
        {
            "q": "Which of the following are benefits of Low Level Design?",
            "options": [
                "Improves code readability",
                "Facilitates unit testing",
                "Defines overall system architecture",
                "Helps in identifying reusable components"
            ],
            "ans": [
                "Improves code readability",
                "Facilitates unit testing",
                "Helps in identifying reusable components"
            ],
            "explain": "LLD promotes readable code, supports testing, and helps in finding reusable parts, though it does not define overall system architecture."
        },
        {
            "q": "Which of the following are SOLID principles important in Low Level Design?",
            "options": [
                "Single Responsibility Principle",
                "Open/Closed Principle",
                "Don’t Repeat Yourself",
                "Liskov Substitution Principle"
            ],
            "ans": [
                "Single Responsibility Principle",
                "Open/Closed Principle",
                "Liskov Substitution Principle"
            ],
            "explain": "SOLID principles include Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion Principles; DRY is a general best practice."
        }
    ],
    "fillblanks": [
        {
            "q": "The principle of ___ states that a class should have only one reason to change.",
            "ans": "Single Responsibility",
            "explain": "This principle ensures classes are focused and maintainable by having a single responsibility."
        },
        {
            "q": "In Low Level Design, ___ diagrams are used to show interactions between objects over time.",
            "ans": "Sequence",
            "explain": "Sequence diagrams illustrate how objects interact in a particular sequence of events."
        },
        {
            "q": "The ___ principle suggests that software entities should be open for extension but closed for modification.",
            "ans": "Open/Closed",
            "explain": "This principle encourages extending behavior without changing existing code, enhancing maintainability."
        }
    ],
    "true_false": [
        {
            "q": "Low Level Design typically deals with class structures and method implementations. (True/False)",
            "ans": "True",
            "explain": "LLD focuses on the detailed internal design of modules including classes and methods."
        },
        {
            "q": "In Low Level Design, coupling should be maximized to increase module dependency. (True/False)",
            "ans": "False",
            "explain": "Low coupling is preferred to reduce dependencies and improve modularity."
        },
        {
            "q": "Polymorphism allows objects of different classes to be treated as objects of a common superclass. (True/False)",
            "ans": "True",
            "explain": "Polymorphism enables this behavior, which is a key object-oriented design concept used in LLD."
        }
    ]
}