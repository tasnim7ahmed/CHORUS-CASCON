"""
LLM Helper for OpenRouter API
==============================

This module provides a unified interface for calling OpenRouter API
(compatible with OpenAI API format) for text generation tasks.
"""

from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL, LLM_TEMPERATURE


class OpenRouterLLM:
    """
    Wrapper for OpenRouter API that mimics Ollama LLM interface.

    This class provides a consistent interface for LLM calls across the tutorial,
    making it easy to swap between different LLM providers.
    """

    def __init__(self, model=None, temperature=None):
        """
        Initialize OpenRouter LLM client.

        Args:
            model: OpenRouter model name (default: from config)
            temperature: Sampling temperature (default: from config)
        """
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found in .env file. "
                "Please add your OpenRouter API key to tutorial/.env"
            )

        self.client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY
        )
        self.model = model or OPENROUTER_MODEL
        self.temperature = temperature if temperature is not None else LLM_TEMPERATURE

    def invoke(self, prompt: str) -> str:
        """
        Generate text from a prompt (compatible with Ollama LLM interface).

        Args:
            prompt: Input text prompt

        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
            )
            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"OpenRouter API call failed: {str(e)}")

    def __call__(self, prompt: str) -> str:
        """Allow calling the instance directly like a function."""
        return self.invoke(prompt)


def get_llm():
    """
    Factory function to get an LLM instance.

    Returns:
        OpenRouterLLM instance configured from environment variables
    """
    return OpenRouterLLM()


# For backward compatibility with existing code
def create_llm(model=None, temperature=None):
    """
    Create an LLM instance with custom parameters.

    Args:
        model: Model name (default: from config)
        temperature: Sampling temperature (default: from config)

    Returns:
        OpenRouterLLM instance
    """
    return OpenRouterLLM(model=model, temperature=temperature)
