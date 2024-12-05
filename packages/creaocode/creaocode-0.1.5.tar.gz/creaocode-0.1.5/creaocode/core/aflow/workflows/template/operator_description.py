operator_description_data = {
    "Custom": {
        "description": "Generates anything based on customized input and instruction.",
        "interface": "custom(input: str, instruction: str) -> dict with key 'response' of type str"
    },
    "ScEnsemble": {
        "description": "Uses self-consistency to select the solution that appears most frequently in the solution list, improve the selection to enhance the choice of the best solution.",
        "interface": "sc_ensemble(solutions: List[str], problem: str) -> dict with key 'response' of type str"
    },
    "Search": {
        "description": "Searches the web for information relevant to the query.",
        "interface": "search(query: str) -> dict with key 'response' of type str"
    },
    "COTGenerate": {
        "description": "Generate step by step based on the task and problem (original problem). The step by step thought process is in the field of 'thought', and the final answer is in the field of 'answer'.",
        "interface": "cot_generate(task: str, problem: str) -> dict with key 'thought' of type str, 'answer' of type str"
    },
    "Format": {
        "description": "Format the solution to the problem description.",
        "interface": "format(problem: str, solution: str) -> dict with key 'response' of type str"
    },
    "Review": {
        "description": "Review the solution and provide a boolean result and feedback.",
        "interface": "review(problem: str, solution: str) -> dict with key 'result' of type bool, 'feedback' of type str"
    },
    "Revise": {
        "description": "Revise the solution to solve the problem/instruction.",
        "interface": "revise(problem: str, solution: str, feedback: str) -> dict with key 'solution' of type str"
    },
    "ReviewAndRevise": {
        "description": "Review the solution and revise it if it is incorrect.",
        "interface": "review_and_revise(problem: str, solution: str) -> dict with key 'response' of type str"
    },
    "Plan": {
        "description": "Creates a strategic plan or sequence of steps to solve the given problem.",
        "interface": "plan(problem: str, instruction: str) -> dict with key 'plan' of type List[str]"
    }
}
