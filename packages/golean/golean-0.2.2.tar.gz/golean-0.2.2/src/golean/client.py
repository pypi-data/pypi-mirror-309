import os
from typing import Optional, Dict, Any
import requests
import tiktoken
from dotenv import load_dotenv

load_dotenv()

class GoLean:
    """Client for interacting with the GoLean API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GoLean client.

        Args:
            api_key (str, optional): The API key for authentication. If not provided,
                                     it will be read from the GOLEAN_API_KEY environment variable.

        Raises:
            ValueError: If the API key is not provided and not found in environment variables.
        """
        self.api_key = api_key or os.getenv("GOLEAN_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it as GOLEAN_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://prompt-compression-api.golean.ai"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def compress_with_context(self, context: str) -> str:
        """
        Compresses a context string using the GoLean API and calculates token statistics.

        Args:
            context (str): The input context string to be compressed.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "compressed_result": The compressed context string.
                - "original_tokens": The number of tokens in the original context.
                - "compressed_tokens": The number of tokens in the compressed context.
                - "compression_rate": The ratio of compressed tokens to original tokens.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/compress_prompt/"
        payload = {"context": context}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        response = response.json()
        original_tokens, compressed_tokens, compression_rate = self._calculate_stats(context, response["compressed_context"])
        return {
            "compressed_result": response["compressed_context"],
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_rate": compression_rate
        }

    def compress_with_template(self, template: str, data: Dict[str, Any]) -> str:
        """
        Compresses a template string by replacing placeholders with compressed values and calculates token statistics.

        Args:
            template (str): A prompt template string with placeholders (e.g., "Summarize the following article: {article}.").
            data (dict): A dictionary where keys match the placeholders in the template, and values are strings to be compressed.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "compressed_result": The populated template with compressed values.
                - "original_tokens": The number of tokens in the original populated template.
                - "compressed_tokens": The number of tokens in the compressed populated template.
                - "compression_rate": The ratio of compressed tokens to original tokens.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        # Compress each variable in the data dictionary
        compressed_data = {}
        for key, value in data.items():
            compressed_data[key] = self.compress_with_context(value)["compressed_result"]
        
        # Populate the template with compressed data
        compressed_result = template.format(**compressed_data)
        original_tokens, compressed_tokens, compression_rate = self._calculate_stats(template.format(**data), template.format(**compressed_data))
        return {
            "compressed_result": compressed_result,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "compression_rate": compression_rate
        }

    def _calculate_stats(self, original_text, compressed_text): 
        """
        Calculates token statistics for the original and compressed texts.

        Args:
            original_text (str): The original input text.
            compressed_text (str): The compressed output text.

        Returns:
            tuple: A tuple containing:
                - original_tokens (int): The number of tokens in the original text.
                - compressed_tokens (int): The number of tokens in the compressed text.
                - compression_rate (float): The ratio of compressed tokens to original tokens.
        """
        enc = tiktoken.encoding_for_model("gpt-4o")
        original_tokens = len(enc.encode(original_text))
        compressed_tokens = len(enc.encode(compressed_text))
        compression_rate = compressed_tokens / original_tokens
        return original_tokens, compressed_tokens, compression_rate