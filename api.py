import os
import openai
from openai import OpenAI
from typing import List, Optional
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

class BotAPI:
    def __init__(self):
        """Initialize the ChatGPT Bot API with empty prompts storage."""
        self.prompts: List[str] = []
        self.client = self.initialize_gpt3()

    def initialize_gpt3(self) -> OpenAI:
        """Initialize OpenAI API client with credentials from .env file."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  
        self.max_tokens = 150  
        return client

    def create_prompt(self, prompt: str) -> int:
        """Store a new prompt and return its index."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string")
        self.prompts.append(prompt.strip())
        return len(self.prompts) - 1

    def get_response(self, prompt_index: int) -> str:
        """Generate and return ChatGPT response for the prompt at given index."""
        if not self._is_valid_index(prompt_index):
            raise IndexError("Invalid prompt index")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": self.prompts[prompt_index]}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7  
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to get response: {str(e)}")

    def update_prompt(self, prompt_index: int, new_prompt: str) -> None:
        """Update an existing prompt at the given index."""
        if not self._is_valid_index(prompt_index):
            raise IndexError("Invalid prompt index")
        if not isinstance(new_prompt, str) or not new_prompt.strip():
            raise ValueError("New prompt must be a non-empty string")
        self.prompts[prompt_index] = new_prompt.strip()

    def _is_valid_index(self, index: int) -> bool:
        """Helper method to validate prompt index."""
        return isinstance(index, int) and 0 <= index < len(self.prompts)