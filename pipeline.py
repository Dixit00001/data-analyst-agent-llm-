from llm_utils import analyze_question, generate_code, review_and_debug_code
from executor import execute_code
import json

def run_pipeline(question_file: str, data_files: list):
    # 1. Parse question
    with open(question_file, "r") as f:
        question_text = f.read()

    # 2. LLM breakdown
    steps = analyze_question(question_text)

    # 3. Generate initial Python code
    code = generate_code(steps, question_file, data_files)

    # 4. Review/debug loop (max 3 retries)
    for attempt in range(3):
        output, error = execute_code(code, question_file, data_files)
        if error:
            code = review_and_debug_code(code, error)
            continue
        try:
            return json.loads(output)  # Must return JSON output
        except:
            code = review_and_debug_code(code, "Output format error")
    return {"error": "Pipeline failed after retries"}
