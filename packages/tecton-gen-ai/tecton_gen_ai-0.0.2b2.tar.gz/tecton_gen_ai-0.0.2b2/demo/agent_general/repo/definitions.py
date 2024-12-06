import os

from pydantic import BaseModel, Field

from tecton_gen_ai.api import Agent, Configs

VERSION = "9_4"


class Output(BaseModel):
    answer: str = Field(description="The answer to the user's question")


Configs(
    llm={"model": "openai/gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]},
    default_timeout="15s",
    bfv_config={
        "tecton_materialization_runtime": "1.1.0b6",
        "environment": f"han-ai-{VERSION}",
    },
    feature_service_config={
        "realtime_environment": f"han-ai-ol-{VERSION}",
    },
).set_default()


def get_company_employee_count(company_name: str) -> int:
    """
    Get the number of employees in a company

    Args:

        company_name: The name of the company

    Returns:

        int: The number of employees in the company, 0 means unknown
    """
    if company_name.lower() == "tecton":
        return 120
    return 0


story_agent = Agent(
    name="story_agent",
    description="The agent that generates stories from the query (which should be the topic of the story)",
    prompt='You should always start from "Once upon a time" and end with "The end". The story should be at most 50 words',
)


general = Agent(
    name="general_agent",
    tools=[story_agent, get_company_employee_count],
    output_schema=Output,
)
