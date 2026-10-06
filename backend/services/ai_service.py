"""
AI Service — LangChain Orchestration with Hallucination Handling
=================================================================
USE_MOCK=true  → realistic mock data, no API key needed
USE_MOCK=false → real Claude via LangChain
"""
import os, json, re
from langchain.prompts import PromptTemplate

USE_MOCK = os.environ.get("USE_MOCK", "true").lower() == "true"

# ── Prompt Templates ──────────────────────────────────────────────────────────

CURRICULUM_PROMPT = PromptTemplate(
    input_variables=["topic", "level", "num_modules"],
    template="""You are an expert instructional designer. Generate a structured course curriculum as JSON.
Topic: {topic} | Level: {level} | Modules: {num_modules}
Return ONLY valid JSON:
{{"course_title":"...","course_description":"...","estimated_hours":number,"modules":[{{"module_number":1,"title":"...","description":"...","youtube_search_queries":["query1"],"lessons":[{{"lesson_number":1,"title":"...","type":"video","duration_minutes":number,"description":"...","key_concepts":["c1","c2","c3"]}}]}}]}}
Each module: 2 video lessons + 1 quiz lesson. Be specific to {topic}."""
)

QUIZ_PROMPT = PromptTemplate(
    input_variables=["topic", "module_title", "lesson_title", "key_concepts"],
    template="""Generate 4 quiz questions about {topic} - {lesson_title}. Key concepts: {key_concepts}
Return ONLY valid JSON: {{"questions":[{{"id":1,"question":"...","options":["A....","B....","C....","D...."],"correct_index":0,"explanation":"..."}}]}}
Make questions SPECIFIC to {topic}. Mix: 1 easy, 2 medium, 1 hard."""
)

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["topic", "lesson_title", "key_concepts"],
    template="""Write a 3-4 sentence lesson summary for: {topic} - {lesson_title}. Concepts: {key_concepts}
Plain text only. Be specific to {topic}."""
)

# ── LLM Factory ───────────────────────────────────────────────────────────────

def _get_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        max_tokens=4000
    )

def _run_chain(prompt, inputs):
    llm = _get_llm()
    result = (prompt | llm).invoke(inputs)
    text = result.content if hasattr(result, "content") else str(result)
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return text

# ── Reliability Layer: retry + validation + fallback ──────────────────────────

class AIGenerationError(Exception):
    pass

def _validate_schema(data: dict, required_keys: list) -> bool:
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys)

def _safe_json_call(prompt, inputs, required_keys, fallback_fn, fallback_args, max_retries=1):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            if attempt == 0:
                raw = _run_chain(prompt, inputs)
            else:
                correction_inputs = dict(inputs)
                correction_inputs["_retry_note"] = (
                    "IMPORTANT: Your previous response was not valid JSON. "
                    "Return ONLY a single valid JSON object with no markdown or extra text."
                )
                raw = _run_chain(prompt, correction_inputs)
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                last_error = f"Invalid JSON (attempt {attempt+1}): {e}"
                print(f"[AI Service] {last_error}")
                continue
            if not _validate_schema(data, required_keys):
                last_error = f"Missing keys {required_keys} (attempt {attempt+1}). Got: {list(data.keys())}"
                print(f"[AI Service] {last_error}")
                continue
            return data
        except Exception as e:
            last_error = f"API error (attempt {attempt+1}): {type(e).__name__}: {e}"
            print(f"[AI Service] {last_error}")
            continue
    print(f"[AI Service] All attempts failed. Using fallback. Last error: {last_error}")
    return fallback_fn(*fallback_args)

def _safe_text_call(prompt, inputs, fallback_fn, fallback_args, max_retries=1):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            text = _run_chain(prompt, inputs)
            if text and len(text.strip()) > 10:
                return text
            last_error = f"Empty/too-short response (attempt {attempt+1})"
            print(f"[AI Service] {last_error}")
        except Exception as e:
            last_error = f"API error (attempt {attempt+1}): {type(e).__name__}: {e}"
            print(f"[AI Service] {last_error}")
    print(f"[AI Service] All attempts failed. Using fallback. Last error: {last_error}")
    return fallback_fn(*fallback_args)

# ── Topic-specific quiz bank ──────────────────────────────────────────────────

_QUIZ_BANK = {
    "python": [
        ("What is the correct way to define a function in Python?",
         ["A. function myFunc():", "B. def myFunc():", "C. void myFunc():", "D. func myFunc():"], 1,
         "Python uses 'def' keyword to define functions."),
        ("What does the 'len()' function return?",
         ["A. Deletes a list", "B. Number of items in an object", "C. Creates a new list", "D. Sorts a list"], 1,
         "len() returns the count of elements in a sequence."),
        ("Which of these is a valid Python list?",
         ["A. list = (1,2,3)", "B. list = {1,2,3}", "C. list = [1,2,3]", "D. list = <1,2,3>"], 2,
         "Python lists use square brackets []."),
        ("What is a Python decorator?",
         ["A. A type of comment", "B. A function that modifies another function", "C. A class method", "D. A variable type"], 1,
         "Decorators wrap other functions to extend their behavior."),
    ],
    "java": [
        ("What is the entry point of a Java program?",
         ["A. start()", "B. run()", "C. main()", "D. init()"], 2,
         "Java programs start from public static void main(String[] args)."),
        ("What does OOP stand for?",
         ["A. Online Object Programming", "B. Object-Oriented Programming", "C. Ordered Output Processing", "D. Open Object Protocol"], 1,
         "OOP stands for Object-Oriented Programming — Java's core paradigm."),
        ("Which keyword creates a new object in Java?",
         ["A. create", "B. instance", "C. new", "D. make"], 2,
         "The 'new' keyword allocates memory and creates a new object instance."),
        ("What is an interface in Java?",
         ["A. A complete class", "B. A contract defining method signatures", "C. A built-in data type", "D. A loop"], 1,
         "Interfaces define what a class must do without specifying how."),
    ],
    "javascript": [
        ("What does 'const' do in JavaScript?",
         ["A. Creates a constant that cannot be reassigned", "B. Creates a reassignable variable", "C. Declares a function", "D. Creates a class"], 0,
         "'const' declares a block-scoped variable that cannot be reassigned."),
        ("What is the DOM?",
         ["A. Data Object Model", "B. Document Object Model", "C. Dynamic Object Manager", "D. Default Output Method"], 1,
         "The DOM is a programming interface representing HTML as a tree of objects."),
        ("What does async/await do?",
         ["A. Makes code run faster", "B. Handles async operations synchronously-style", "C. Creates threads", "D. Prevents errors"], 1,
         "async/await makes asynchronous code easier to read and write."),
        ("What is a JavaScript Promise?",
         ["A. A variable declaration", "B. An object representing eventual async completion", "C. A loop type", "D. A constructor"], 1,
         "A Promise represents an operation that hasn't completed yet."),
    ],
    "react": [
        ("What is a React component?",
         ["A. A CSS file", "B. A reusable piece of UI that returns JSX", "C. A database model", "D. A server endpoint"], 1,
         "React components are reusable UI building blocks that return JSX."),
        ("What does useState() do?",
         ["A. Fetches API data", "B. Manages local state in a functional component", "C. Creates a component", "D. Handles routing"], 1,
         "useState allows functional components to have local state."),
        ("When does useEffect() run?",
         ["A. Only on creation", "B. Only on deletion", "C. After render based on dependency array", "D. Before render always"], 2,
         "useEffect runs after render, controlled by the dependency array."),
        ("What is prop drilling?",
         ["A. A performance optimization", "B. Passing props through many unnecessary component levels", "C. A type of hook", "D. A build tool"], 1,
         "Prop drilling is passing data through intermediate components that don't need it."),
    ],
    "machine learning": [
        ("What is supervised learning?",
         ["A. Learning without data", "B. Training on labelled input-output pairs", "C. Self-directed learning", "D. A database type"], 1,
         "Supervised learning trains models on labelled data with known outputs."),
        ("What is overfitting?",
         ["A. Using too little data", "B. Model performs well on training but poorly on new data", "C. A fast training technique", "D. Too many features"], 1,
         "Overfitting means the model memorized training data instead of learning patterns."),
        ("What does a neural network layer do?",
         ["A. Stores raw data", "B. Transforms input through weighted computations", "C. Deletes irrelevant features", "D. Connects to internet"], 1,
         "Each layer applies transformations to progressively learn complex patterns."),
        ("What is gradient descent?",
         ["A. A data cleaning technique", "B. An optimization algorithm minimizing loss by updating weights", "C. A neural network type", "D. Feature selection"], 1,
         "Gradient descent iteratively adjusts weights to reduce the loss function."),
    ],
    "cooking": [
        ("What does 'mise en place' mean?",
         ["A. A French dessert", "B. Everything in its place — preparing ingredients before cooking", "C. A cooking technique", "D. A type of sauce"], 1,
         "Mise en place means preparing all ingredients before you start cooking."),
        ("What is the Maillard reaction?",
         ["A. A preservation method", "B. Chemical reaction causing browning and flavor when food is heated", "C. A mixing technique", "D. Fermentation"], 1,
         "The Maillard reaction gives browned food its distinctive flavor."),
        ("What does blanching involve?",
         ["A. High-temperature roasting", "B. Brief boiling then immediate cooling in ice water", "C. Slow cooking in oil", "D. Marinating overnight"], 1,
         "Blanching preserves color by briefly boiling then shocking in cold water."),
        ("Why do recipes say 'season to taste'?",
         ["A. Salt is harmful", "B. Adjust salt/pepper to your preference as you cook", "C. Add sugar", "D. Use seasoning packets"], 1,
         "Seasoning to taste means adjusting gradually since preferences and ingredients vary."),
    ],
    "sql": [
        ("What does SQL stand for?",
         ["A. Structured Question Language", "B. Structured Query Language", "C. Simple Query Logic", "D. System Query Layer"], 1,
         "SQL stands for Structured Query Language."),
        ("What does a JOIN do?",
         ["A. Deletes rows", "B. Combines rows from multiple tables based on a related column", "C. Creates a database", "D. Updates records"], 1,
         "JOIN combines rows from multiple tables using matching conditions."),
        ("Difference between WHERE and HAVING?",
         ["A. They are identical", "B. WHERE filters rows before grouping; HAVING filters groups after GROUP BY", "C. HAVING is faster", "D. WHERE only works with numbers"], 1,
         "WHERE filters rows before aggregation; HAVING filters after GROUP BY."),
        ("What is a PRIMARY KEY?",
         ["A. Most important column name", "B. Unique identifier for each row that cannot be NULL", "C. First column in a table", "D. A foreign key reference"], 1,
         "A primary key uniquely identifies each record in a table."),
    ],
    "docker": [
        ("What is a Docker container?",
         ["A. A virtual machine", "B. A lightweight isolated environment packaging an app and its dependencies", "C. A cloud server", "D. A database backup"], 1,
         "Containers package code and dependencies together, running consistently everywhere."),
        ("What is a Dockerfile?",
         ["A. A running container", "B. A text file with instructions to build a Docker image", "C. A Docker network", "D. A storage volume"], 1,
         "A Dockerfile is a script Docker uses to automatically build an image."),
        ("What does 'docker-compose up' do?",
         ["A. Deletes all containers", "B. Starts all services defined in docker-compose.yml", "C. Builds a single container", "D. Pushes to Docker Hub"], 1,
         "docker-compose up reads docker-compose.yml and starts all defined services."),
        ("Difference between image and container?",
         ["A. They are the same", "B. An image is a blueprint; a container is a running instance of that image", "C. Containers are larger", "D. Images run code; containers store it"], 1,
         "A Docker image is a static template; a container is the live running instance."),
    ],
    "data science": [
        ("What is a DataFrame in pandas?",
         ["A. A Python list", "B. A 2D labelled data structure like a spreadsheet", "C. A machine learning model", "D. A database table"], 1,
         "A DataFrame is pandas' core 2D data structure with rows and columns."),
        ("What does EDA stand for?",
         ["A. Error Detection Algorithm", "B. Exploratory Data Analysis", "C. Extended Data Aggregation", "D. Encoded Data Array"], 1,
         "EDA is the process of visually and statistically exploring datasets."),
        ("What is a null value in a dataset?",
         ["A. A value of zero", "B. A missing or undefined value", "C. A negative number", "D. A string value"], 1,
         "Null values represent missing data and must be handled before modeling."),
        ("What does data normalization do?",
         ["A. Removes duplicate rows", "B. Scales features to a common range so no feature dominates", "C. Sorts the data", "D. Converts text to numbers"], 1,
         "Normalization scales features so they contribute equally to models."),
    ],
}

def _topic_quiz(topic, lesson_title, key_concepts):
    c = (key_concepts + [topic, "basics", "methods"])[:3]
    return {"questions": [
        {"id": 1, "question": f"What is the primary purpose of {c[0]} in {topic}?",
         "options": [f"A. To provide structure when working with {c[0]} in {topic}", f"B. To replace all other {topic} concepts", f"C. To slow down the workflow", f"D. To avoid using {topic}"],
         "correct_index": 0, "explanation": f"{c[0]} provides structure and consistency in {topic}."},
        {"id": 2, "question": f"Which approach is best for learning {c[1]} in {topic}?",
         "options": ["A. Memorise without practice", f"B. Build real projects applying {c[1]} concepts", f"C. Skip {c[1]} entirely", "D. Only read documentation"],
         "correct_index": 1, "explanation": f"Hands-on practice applying {c[1]} to real projects is most effective."},
        {"id": 3, "question": f"What is a common beginner mistake in {topic}?",
         "options": ["A. Starting with simple projects", "B. Memorising syntax before understanding concepts", "C. Following structured tutorials", "D. Asking questions"],
         "correct_index": 1, "explanation": f"Understanding concepts before memorising syntax is key to mastering {topic}."},
        {"id": 4, "question": f"How does {c[2]} relate to {topic} overall?",
         "options": [f"A. Unrelated to {topic}", f"B. A core building block other {topic} concepts depend on", f"C. Only for advanced {topic}", f"D. Replaces other {topic} concepts"],
         "correct_index": 1, "explanation": f"{c[2]} is foundational — mastering it makes advanced {topic} much easier."},
    ]}

_MODULE_THEMES = [
    ("Foundations & Core Concepts",  ["What is", "Why it matters"]),
    ("Core Techniques",              ["Essential methods", "Hands-on walkthrough"]),
    ("Real-World Application",       ["Case studies", "Building your first project"]),
    ("Advanced Patterns",            ["Performance", "Scaling best practices"]),
    ("Mastery & Next Steps",         ["Deep dives", "Career paths"]),
]

def _mock_curriculum(topic, level, num_modules):
    modules = []
    for i, (theme, subtitles) in enumerate(_MODULE_THEMES[:num_modules]):
        lessons = [{"lesson_number": j+1, "title": f"{sub} in {topic}", "type": "video",
                    "duration_minutes": 15, "description": f"Learn {sub.lower()} in {topic}.",
                    "key_concepts": [f"{topic} {sub.split()[0].lower()}", "practical examples", "common patterns"]}
                   for j, sub in enumerate(subtitles)]
        lessons.append({"lesson_number": len(lessons)+1, "title": f"{theme} — Knowledge Check",
                         "type": "quiz", "duration_minutes": 5, "description": "Test your understanding.", "key_concepts": []})
        modules.append({"module_number": i+1, "title": f"Module {i+1}: {theme}",
                         "description": f"Master {theme.lower()} of {topic}.",
                         "youtube_search_queries": [f"{topic} {theme.lower()} tutorial"],
                         "lessons": lessons})
    return {"course_title": f"{topic} — {level.title()} Course",
            "course_description": f"A structured {level}-level course on {topic}. Covers fundamentals through real-world application.",
            "estimated_hours": num_modules * 2,
            "total_videos": sum(len([l for l in m["lessons"] if l["type"] == "video"]) for m in modules),
            "total_quizzes": sum(len([l for l in m["lessons"] if l["type"] == "quiz"]) for m in modules),
            "modules": modules}

def _mock_quiz(topic, module_title, lesson_title, key_concepts):
    for bank_key in _QUIZ_BANK:
        if bank_key in topic.lower() or topic.lower() in bank_key:
            qs = _QUIZ_BANK[bank_key]
            return {"questions": [{"id": i+1, "question": q, "options": o, "correct_index": c, "explanation": e}
                                  for i, (q, o, c, e) in enumerate(qs)]}
    return _topic_quiz(topic, lesson_title, key_concepts)

def _mock_summary(topic, lesson_title, key_concepts):
    c = ", ".join(key_concepts[:3]) if key_concepts else topic
    return (f"This lesson covers {lesson_title.lower()}, a key area within {topic}. "
            f"You will explore {c} through practical examples. "
            f"By the end you will have the skills to apply these concepts in real {topic} projects.")

# ── Public API ────────────────────────────────────────────────────────────────

def generate_curriculum(topic, level="beginner", num_modules=4):
    if USE_MOCK:
        return _mock_curriculum(topic, level, num_modules)
    return _safe_json_call(CURRICULUM_PROMPT,
                           {"topic": topic, "level": level, "num_modules": num_modules},
                           required_keys=["course_title", "modules"],
                           fallback_fn=_mock_curriculum, fallback_args=(topic, level, num_modules))

def generate_quiz(topic, module_title, lesson_title, key_concepts):
    if USE_MOCK:
        return _mock_quiz(topic, module_title, lesson_title, key_concepts)
    return _safe_json_call(QUIZ_PROMPT,
                           {"topic": topic, "module_title": module_title,
                            "lesson_title": lesson_title, "key_concepts": ", ".join(key_concepts)},
                           required_keys=["questions"],
                           fallback_fn=_mock_quiz, fallback_args=(topic, module_title, lesson_title, key_concepts))

def generate_lesson_summary(topic, lesson_title, key_concepts):
    if USE_MOCK:
        return _mock_summary(topic, lesson_title, key_concepts)
    return _safe_text_call(SUMMARY_PROMPT,
                           {"topic": topic, "lesson_title": lesson_title, "key_concepts": ", ".join(key_concepts)},
                           fallback_fn=_mock_summary, fallback_args=(topic, lesson_title, key_concepts))
