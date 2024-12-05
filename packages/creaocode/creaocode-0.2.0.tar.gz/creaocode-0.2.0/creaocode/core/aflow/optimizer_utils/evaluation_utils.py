import asyncio
from creaocode.core.aflow.evaluator import Evaluator
import random
from jinja2 import Template
from pydantic import BaseModel, Field
import openai
import os
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import psycopg2
import json
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def generate_prediction_and_judge(configured_graph, row_dict, input_prompt_template, judge_prompt_template):
    print(f"row_dict: {row_dict}")
    input_prompt = input_prompt_template.render(row_dict)
    try:
        prediction, cost = await configured_graph(input_prompt)
        print(f"prediction: {prediction}")
        row_dict["prediction"] = prediction
    except Exception as e:
        print(f"Error in generate_prediction_and_judge: {e}")
        prediction = f"error: {e}"
        row_dict["prediction"] = prediction
        cost = 0
    class JudgeResult(BaseModel):
        score: float
    judge_prompt = judge_prompt_template.render(row_dict)
    completion = client.beta.chat.completions.parse(
        #TODO: yutong make the model configurable
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "you are a helpful assistant"},
            {"role": "user", "content": f"{judge_prompt}"},
        ],
        response_format=JudgeResult,
    )
    score = completion.choices[0].message.parsed.score
    print(f"judge prompt: {judge_prompt}")
    print(f"score: {score}")
    return score, row_dict

def save_results_to_csv(path, results_rows, avg_score):
    df = pd.DataFrame(results_rows)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{avg_score:.5f}_{current_time}.csv"
    output_file = os.path.join(path, filename)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

class EvaluationUtils:
    def __init__(self, root_path: str):
        self.root_path = root_path

    async def evaluate_initial_round(self, optimizer, graph_path, directory, validation_n, data):
        # 使用 optimizer 的 graph_utils 来加载图
        optimizer.graph = optimizer.graph_utils.load_graph(optimizer.round, graph_path)
        evaluator = Evaluator(eval_path=directory)

        for i in range(validation_n):
            score, avg_cost, total_cost = await evaluator.graph_evaluate(
                optimizer.dataset,
                optimizer.graph,
                {"dataset": optimizer.dataset, "llm_config": optimizer.execute_llm_config},
                directory,
                is_test=False,
            )

            new_data = optimizer.data_utils.create_result_data(optimizer.round, score, avg_cost, total_cost)
            data.append(new_data)

            result_path = optimizer.data_utils.get_results_file_path(graph_path)
            optimizer.data_utils.save_results(result_path, data)

        return data

    async def evaluate_graph(self, optimizer, directory, validation_n, data, initial=False):
        # TODO: yutong make the graph name configurable
        configured_graph = optimizer.graph(name="default")
        sum_score = 0
        input_prompt_template = optimizer.inputPromptTemplate
        judge_prompt_template = optimizer.judgePromptTemplate
        data_rows = optimizer.data_rows
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        cur = conn.cursor()
        for i in range(validation_n):
            #score = random.uniform(0, 1)
            avg_cost = 0 
            total_cost =0
            # Construct the input prompt using the input_prompt_template and input_dict
            input_template = Template(input_prompt_template)
            # Construct the judge prompt using the judge_prompt_template and input_dict
            judge_template = Template(judge_prompt_template)

            # Generate responses for each row in data_rows
            score_res = []
            row_dicts = []
            # Fetch the DataTable ID based on projectId
            fetch_data_table_id_query = """
                SELECT "id"
                FROM data_tables
                WHERE "projectId" = %s
            """
            cur.execute(fetch_data_table_id_query, (optimizer.projectId,))
            conn.commit()
            data_table_id = cur.fetchone()
            cur_round = optimizer.round + 1 if initial is False else optimizer.round
            for row in tqdm(data_rows):
                score, new_row_dict = await generate_prediction_and_judge(configured_graph, row["input"], input_template, judge_template)
                print(f"Generated with score: {score}")
                score_res.append(score)
                row_dicts.append(new_row_dict)
                row_id = row["id"]
                original_output = row['output']
                original_output[f"round_{cur_round}"] = new_row_dict["prediction"]
                print(f"original_output: {original_output}")
                update_data_table_row_query = """
                    UPDATE data_table_rows
                    SET "output" = %s::jsonb, "rowStatus" = 'ACTIVE', "updatedAt" = NOW()
                    WHERE "dataTableId" = %s AND "id" = %s
            """
                cur.execute(update_data_table_row_query, (json.dumps(original_output), data_table_id, row_id))
                conn.commit()
            output_path = f"{optimizer.root_path}/workflows/round_{cur_round}"
            print(f"output_path: {output_path}")
            score = sum(score_res) / len(score_res)
            save_results_to_csv(output_path, row_dicts, score)
            print(f"Average Score: {score}")
            new_data = optimizer.data_utils.create_result_data(cur_round, score, avg_cost, total_cost)
            data.append(new_data)

            result_path = optimizer.data_utils.get_results_file_path(f"{optimizer.root_path}/workflows")
            optimizer.data_utils.save_results(result_path, data)

            sum_score += score
            cur.close()
            conn.close()
        # data here is the result data of all the rounds
        return sum_score / validation_n, data

    async def evaluate_graph_test(self, optimizer, directory, is_test=True):
        evaluator = Evaluator(eval_path=directory)
        return await evaluator.graph_evaluate(
            optimizer.dataset,
            optimizer.graph,
            {"dataset": optimizer.dataset, "llm_config": optimizer.execute_llm_config},
            directory,
            is_test=is_test,
        )