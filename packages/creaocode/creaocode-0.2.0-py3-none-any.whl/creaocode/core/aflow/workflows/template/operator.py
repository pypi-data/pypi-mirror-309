# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 17:36 PM
# @Author  : didi
# @Desc    : operator demo of ags
import concurrent
import sys
import traceback
from typing import List

import openai

from tenacity import retry, stop_after_attempt, wait_fixed
from exa_py import Exa

from creaocode.core.aflow.workflows.template.operator_an import *
from creaocode.core.aflow.workflows.template.op_prompt import *
import asyncio
import logging
import os
logger = logging.getLogger(__name__)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
class Operator:
    def __init__(self, name: str, model: str = "gpt-4o-mini"):
        # other model options: gpt-4o-2024-08-06 
        self.name = name
        self.model = model

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    async def _completion(self, op_class, input_prompt, instruction= "", **extra_kwargs):
        input_prompt = instruction + "\n" + input_prompt
        completion = client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant"},
                {"role": "user", "content": input_prompt},
            ],
            temperature=0.6,
            response_format=op_class,
        )
        output = completion.choices[0].message.parsed
        json_output = output.model_dump(mode='json')
        print("json_output:", json_output)
        return json_output

class Custom(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "Custom"):
        super().__init__(name, model)

    async def __call__(self, input_prompt, instruction=""):
        response = await self._completion(GenerateOp, input_prompt, instruction=instruction)
        return response
    
def run_code(code):
    try:
        # Create a new global namespace
        global_namespace = {}

        disallowed_imports = [
            "os", "sys", "subprocess", "multiprocessing",
            "matplotlib", "seaborn", "plotly", "bokeh", "ggplot",
            "pylab", "tkinter", "PyQt5", "wx", "pyglet"
        ]

        # Check for prohibited imports
        for lib in disallowed_imports:
            if f"import {lib}" in code or f"from {lib}" in code:
                logger.info("Detected prohibited import: %s", lib)
                return "Error", f"Prohibited import: {lib} and graphing functionalities"

        # Use exec to execute the code
        exec(code, global_namespace)
        # Assume the code defines a function named 'solve'
        if 'solve' in global_namespace and callable(global_namespace['solve']):
            result = global_namespace['solve']()
            return "Success", str(result)
        else:
            return "Error", "Function 'solve' not found"
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return "Error", f"Execution error: {str(e)}\n{''.join(tb_str)}"
    

class Search(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "Search"):
        super().__init__(name, model)

    async def __call__(self, query: str):
        print(f"exa api key: {os.getenv('EXA_API_KEY')}")
        exa = Exa(os.getenv('EXA_API_KEY'))
        result_with_text = exa.search_and_contents(
            query,
            text=True,
            num_results=2
        )
        print(f"query: {query}")
        print(f"result_with_text: {result_with_text}")
        result = "\n".join([res.text for res in result_with_text.results])
        return {"response": result}
    

class Review(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "Review"):
        super().__init__(name, model)

    async def __call__(self, problem, solution):
        prompt = REVIEW_PROMPT.format(problem=problem, solution=solution)
        response = await self._completion(ReviewOp, prompt)
        return response
    
class Revise(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "Revise"):
        super().__init__(name, model)

    async def __call__(self, problem, solution, feedback):
        prompt = REVISE_PROMPT.format(problem=problem, solution=solution, feedback=feedback)
        response = await self._completion(ReviseOp, prompt)
        return response
    

class ReviewAndRevise(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "ReviewAndRevise"):
        self.review = Review(model)
        self.revise = Revise(model)
        super().__init__(name, model)

    async def __call__(self, problem, solution):
        review_response = await self.review(problem, solution)
        if review_response["result"]:
            return {"response": solution}
        else:
            revise_response = await self.revise(problem, solution, review_response["feedback"])
            return {"response": revise_response["solution"]}
    
class Plan(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "Plan"):
        super().__init__(name, model)

    async def __call__(self, problem, instruction=""):
        prompt = PLAN_PROMPT.format(problem=problem, instruction=instruction)
        response = await self._completion(PlanOp, prompt)
        return response

class COTGenerate(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "COTGenerate"):
        super().__init__(name, model)

    async def __call__(self, task: str, problem: str):
        prompt = COT_GENERATE_PROMPT.format(task=task, problem=problem) 
        response = await self._completion(COTGenerateOp, prompt)
        return response
    
class Format(Operator):
    def __init__(self, model: str = "gpt-4o-mini", name: str = "Format"):
        super().__init__(name, model)

    async def __call__(self, problem, solution, mode: str = None):
        prompt = FORMAT_PROMPT.format(problem_description=problem, solution=solution)
        response = await self._completion(FormatOp, prompt, mode)
        return response


class ScEnsemble(Operator):
    """
    Paper: Self-Consistency Improves Chain of Thought Reasoning in Language Models
    Link: https://arxiv.org/abs/2203.11171
    Paper: Universal Self-Consistency for Large Language Model Generation
    Link: https://arxiv.org/abs/2311.17311
    """

    def __init__(self, model: str = "gpt-4o-mini", name: str = "ScEnsemble"):
        super().__init__(name, model)

    async def __call__(self, solutions: List[str], problem: str):
        solution_text = "\n".join(solutions)
        prompt = SC_ENSEMBLE_PROMPT.format(problem=problem, solutions=solution_text)
        print(f"sc ensemble prompt: {prompt}")
        response = await self._completion(ScEnsembleOp, prompt)

        answer = response.get("solution", "")
        print(f"sc ensemble answer: {answer}")
        return {"response": answer}
