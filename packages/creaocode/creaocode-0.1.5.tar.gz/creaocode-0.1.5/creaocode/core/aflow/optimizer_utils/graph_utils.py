import json
import os
import re
import time
import traceback
from typing import List
import importlib.util
import sys
from creaocode.core.aflow.prompts.optimze_prompt import (
    WORKFLOW_INPUT,
    WORKFLOW_OPTIMIZE_PROMPT,
    WORKFLOW_TEMPLATE,
    WORKFLOW_CUSTOM_USE
)
from creaocode.core.aflow.workflows.template.operator_description import operator_description_data
import logging

logger = logging.getLogger(__name__)

class GraphUtils:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def create_round_directory(self, graph_path: str, round_number: int) -> str:
        directory = os.path.join(graph_path, f"round_{round_number}")
        os.makedirs(directory, exist_ok=True)
        return directory

    def load_graph(self, round_number: int, workflows_path: str):
        graph_module_path = f"{workflows_path}/round_{round_number}/graph.py"

        # Determine the root directory of the project
        # Assuming workflows_path is something like 'project_root/workflows'
        root_dir = os.path.abspath(os.path.join(workflows_path, '..', '..'))

        # Add the root directory to sys.path
        if root_dir not in sys.path:
            sys.path.append(root_dir)

        try:
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location("graph_module", graph_module_path)
            graph_module = importlib.util.module_from_spec(spec)
            sys.modules["graph_module"] = graph_module
            spec.loader.exec_module(graph_module)
            
            # Access the Workflow class from the dynamically loaded module
            graph_class = getattr(graph_module, "Workflow")
            return graph_class
        except ImportError as e:
            logger.error(f"Error loading graph for round {round_number}: {e}")
            raise

    def read_graph_files(self, round_number: int, workflows_path: str):
        prompt_file_path = os.path.join(workflows_path, f"round_{round_number}", "prompt.py")
        graph_file_path = os.path.join(workflows_path, f"round_{round_number}", "graph.py")

        try:
            with open(prompt_file_path, "r", encoding="utf-8") as file:
                prompt_content = file.read()
            with open(graph_file_path, "r", encoding="utf-8") as file:
                graph_content = file.read()
        except FileNotFoundError as e:
            logger.info(f"Error: File not found for round {round_number}: {e}")
            raise
        except Exception as e:
            logger.info(f"Error loading prompt for round {round_number}: {e}")
            raise
        return prompt_content, graph_content

    def extract_solve_graph(self, graph_load: str) -> List[str]:
        pattern = r"class Workflow:.+"
        return re.findall(pattern, graph_load, re.DOTALL)

    def load_operators_description(self, operators: List[str]) -> str:
        path = f"creaocode/core/aflow/workflows/template/operator.json"
        operators_description = ""
        for id, operator in enumerate(operators):
            operator_description = self._load_operator_description(id + 1, operator)
            operators_description += f"{operator_description}\n"
        return json.dumps(operator_description)

    def _load_operator_description(self, id: int, operator_name: str) -> str:
        operator_data = operator_description_data
        matched_data = operator_data[operator_name]
        desc = matched_data["description"]
        interface = matched_data["interface"]
        return f"{id}. {operator_name}: {desc}, with interface {interface})."

    def create_graph_optimize_prompt(
        self,
        input_prompt_template: str,
        experience: str,
        score: float,
        graph: str,
        prompt: str,
        operator_description: str,
        type: str,
        log_data: str,
    ) -> str:
        print(f"operator_description for graph optimize: {operator_description}")
        graph_input = WORKFLOW_INPUT.format(
            experience=experience,
            score=score,
            graph=graph,
            prompt=prompt,
            input_prompt_template=input_prompt_template,
            operator_description=operator_description,
            type=type,
            log=log_data,
        )
        graph_system = WORKFLOW_OPTIMIZE_PROMPT.format(type=type)
        return graph_input + WORKFLOW_CUSTOM_USE + graph_system

    async def get_graph_optimize_response(self, graph_optimize_node):
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                response = graph_optimize_node.instruct_content.model_dump()
                return response
            except Exception as e:
                retries += 1
                logger.info(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")
                if retries == max_retries:
                    logger.info("Maximum retries reached. Skipping this sample.")
                    break
                traceback.print_exc()
                time.sleep(5)
        return None

    def write_graph_files(self, directory: str, response: dict, round_number: int, dataset: str):
        graph = WORKFLOW_TEMPLATE.format(graph=response["graph"], round=round_number, dataset=dataset)

        with open(os.path.join(directory, "graph.py"), "w", encoding="utf-8") as file:
            file.write(graph)

        with open(os.path.join(directory, "prompt.py"), "w", encoding="utf-8") as file:
            file.write(response["prompt"])      

        with open(os.path.join(directory, "__init__.py"), "w", encoding="utf-8") as file:
            file.write("")