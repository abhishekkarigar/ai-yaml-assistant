import os
from pathlib import Path
from typing import List, Union

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# Environment & Constants
# -------------------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YAML_PATH = Path("testfile/test.yaml")

YamlValue = Union[str, int, float, bool]


# -------------------------------------------------------------------
# OpenAI Client
# -------------------------------------------------------------------

client = OpenAI(api_key=OPENAI_API_KEY)


# -------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------

class YamlUpdate(BaseModel):
    path: List[str] = Field(
        description="Path to the YAML field as a list of keys"
    )
    value: YamlValue = Field(
        description="New value to set at the path"
    )


class YamlUpdateResponse(BaseModel):
    updates: List[YamlUpdate]


# -------------------------------------------------------------------
# LLM System Prompt
# -------------------------------------------------------------------

SYSTEM_PROMPT = """
You are a YAML configuration editor.

Rules:
- Do NOT return full YAML
- Only return structured updates
- Paths must be accurate
- Do NOT invent fields
- Do NOT delete fields, only update
- Output must strictly follow the JSON schema
"""


# -------------------------------------------------------------------
# Core Functions
# -------------------------------------------------------------------

def update_yaml_file(user_prompt: str) -> None:
    yaml_dict = read_yaml_file()
    updates = extract_yaml_properties(user_prompt)

    updated_yaml = apply_updates(
        yaml_dict=yaml_dict,
        updates=updates.updates,
    )

    write_yaml_file(updated_yaml)


def apply_updates(yaml_dict: dict,updates: List[YamlUpdate]) -> dict:
    for update in updates:
        current = yaml_dict

        for key in update.path[:-1]:
            if key not in current:
                raise ValueError(f"Invalid path: {update.path}")
            current = current[key]

        current[update.path[-1]] = update.value

    return yaml_dict


def read_yaml_file() -> dict:
    with YAML_PATH.open("r") as file:
        return yaml.safe_load(file)


def extract_yaml_properties(user_prompt: str) -> YamlUpdateResponse:
    yaml_content = YAML_PATH.read_text()

    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Current YAML:\n"
                    f"{yaml_content}\n\n"
                    "Instruction:\n"
                    f"{user_prompt}"
                ),
            },
        ],
        response_format=YamlUpdateResponse,
    )

    return response.choices[0].message.parsed


def write_yaml_file(data: dict) -> None:
    with YAML_PATH.open("w") as file:
        yaml.safe_dump(data, file, sort_keys=False)


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    update_yaml_file("update resource cpu to 20m and image tag to v2.0.0")
