from typing import Any, Dict, List
import uuid
from openai import OpenAI
import boto3
import os
import json
from pydantic import BaseModel, create_model
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_pydantic_model(fields: List[Dict[str, Any]]) -> BaseModel:
    """
    Create a Pydantic model dynamically from a list of dictionaries representing fields.

    Args:
    - fields (List[Dict[str, Any]]): A list where each dict contains 'name' and 'type' keys.

    Returns:
    - A dynamically created Pydantic model class.
    """
    new_json_list = []
    for item in fields:
        if item["type"] == "list[str]":
            item["type"] = List[str]
        elif item["type"] == "str":
            item["type"] = str
        new_json_list.append(item)
    fields = new_json_list
    field_definitions = {field["name"]: (field["type"], ...) for field in fields}
    return create_model("JsonBase", **field_definitions)


class Embed:
    def __init__(self):
        self.client = OpenAI()

    def invoke(self, text):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding


# Load your OpenAI API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(
    api_key=os.environ.get(
        "OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"
    )
)


class CreaoLLM:
    def __init__(self, bot_name="assistant", bot_content="assistant") -> None:
        self.bot_name = bot_name
        self.bot_content = bot_content

    def invoke(
        self, prompt, output_schema, component_id="default", pipeline_id="default"
    ):
        """
        Invoke the Creao LLM API
        """
        # The API Gateway endpoint URL
        # Payload to be sent to the Lambda function via API Gateway
        pandantic_model = create_pydantic_model(output_schema)
        # Define the system message for output schema enforcement
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful assistant. You are assisting a user with a task."
            ),
        }
        # The user prompt
        user_message = {"role": "user", "content": prompt}
        response = openai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # Specify the GPT-4 model gpt-4o-2024-08-06
            messages=[system_message, user_message],
            response_format=pandantic_model,
        )
        message = response.choices[0].message.content
        response_josn = json.loads(message)
        dynamodb = boto3.resource("dynamodb")
        # table name
        table = dynamodb.Table("creao_component")
        logger.info(f"creao_component id: {component_id}")
        # generate a uuid
        uuid_str = str(uuid.uuid4())
        # inserting values into table
        table_response = table.put_item(
            Item={
                "pipeline_id": pipeline_id,
                "uuid": uuid_str,
                "prompt": prompt,
                "component_id": component_id,
                "pipeline_id": pipeline_id,
                "service": f"gpt-4o-mini",
                "response": response_josn,
            }
        )
        try:
            return response_josn
        except Exception as e:
            print(f"CreaoLLM json decode error:{e}, with response:{response.text}")
            return {"reply": ""}


class OpenAILLM:
    def __init__(self, model_id="gpt-4o-mini"):
        self.client = OpenAI()
        self.model_id = model_id

    def invoke(self, prompt, schema=None):
        messages = [{"role": "user", "content": prompt}]
        try:
            if schema is None:
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                )
                return response.choices[0].message.content
            else:
                response = self.client.beta.chat.completions.parse(
                    model=self.model_id,
                    messages=messages,
                    temperature=0,
                    max_tokens=1024,
                    response_format=schema,
                )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return None


# creaoLM = CreaoLLM()
# r = creaoLM.invoke("hello", {"name":"world"})
# print(r)
