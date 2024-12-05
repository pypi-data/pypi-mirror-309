import os
from typing import Any, Dict
import uuid
from pydantic import BaseModel, Field
import httpx


class Agent(BaseModel):
    name: str = Field(..., description="The name of the agent")
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    description: str = Field(default="A helpful assistant.", description="A brief description of the agent")
    endpoint: str = Field(default=None, description="The endpoint of the model provider")
    api_key : str = Field(default=None, description="The API key of the model provider")
    model: str = Field(default=None, description="The name of the model")
    instructions: str = Field(default="You are a helpful assistant.", description="Instructions for the agent")
    temperature: float = Field(default=0.5, description="The temperature of the model")
    top_p: float = Field(default=1.0, description="The top p value of the model")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    def model_post_init(self, __context: Any) -> None:
        if self.endpoint == "openai-v1-chat-completions" and self.model == "gpt-4o-2024-08-06":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if self.api_key is None:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            return

        if self.endpoint == "anthropic-v1-messages" and self.model == "claude-3-5-sonnet-20241022":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if self.api_key is None:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
            return

    def generate_text(self, input: str) -> str:
        # https://platform.openai.com/docs/models#gpt-4o - https://api.openai.com/v1/chat/completions
        if self.endpoint == "openai-v1-chat-completions" and self.model == "gpt-4o-2024-08-06":
            context_window = 128000
            max_output_tokens = 16384
            input_token_price_per_million = 2.50
            output_token_price_per_million = 10.00

            # Define the request URL and headers
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            # Define the request payload
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": input}
                ],
                "temperature": self.temperature,
                "top_p": self.top_p
            }

            # Send the request using httpx
            response = httpx.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            return response_json['choices'][0]['message']['content']

        # https://docs.anthropic.com/en/docs/about-claude/models - https://api.anthropic.com/v1/messages
        if self.endpoint == "anthropic-v1-messages" and self.model == "claude-3-5-sonnet-20241022":
            context_window = 200000
            max_output_tokens = 8192
            input_token_price_per_million = 3.00
            output_token_price_per_million = 15.00

            # Define the request URL and headers
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }

            # Define the request payload
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "system": self.instructions,
                "max_tokens": max_output_tokens,
                "messages": [
                    {"role": "user", "content": input}
                ],
                "temperature": self.temperature,
                "top_p": self.top_p
            }

            # Send the request using httpx
            response = httpx.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            return response_json['content'][0]['text']

        raise Exception(f"An endpoint '{self.endpoint}' and model name '{self.model}' cannot execute the request. Please check the endpoint and model name.")
