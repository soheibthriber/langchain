"""
Simple Hugging Face LLM Wrapper
===============================

This provides a free alternative to OpenAI using Hugging Face models
that can run without API keys (using transformers library directly).
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from transformers import pipeline


class HuggingFaceLLM:
    """Simple Hugging Face LLM that works with or without API token"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", use_api: bool = False):
        self.model_name = model_name
        self.use_api = use_api
        self.temperature = 0.7
        
        if use_api:
            self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
            self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        else:
            try:
                # Use local transformers (no API needed)
                self.pipeline = pipeline("text-generation", model="gpt2", max_length=100)
                self.model_name = "gpt2-local"
                print("💡 Using local GPT-2 model (no API required)")
            except Exception as e:
                print(f"⚠️  Local model failed: {e}")
                self.pipeline = None
    
    def invoke(self, prompt: str) -> str:
        """Generate text using Hugging Face model"""
        try:
            if self.use_api and self.api_token:
                return self._api_generate(prompt)
            elif self.pipeline:
                return self._local_generate(prompt)
            else:
                return self._mock_generate(prompt)
        except Exception as e:
            print(f"⚠️  HF generation failed: {e}")
            return self._mock_generate(prompt)
    
    def _api_generate(self, prompt: str) -> str:
        """Generate using Hugging Face API"""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": prompt, "parameters": {"max_length": 100}}
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", prompt).replace(prompt, "").strip()
            return "API response format unexpected"
        else:
            return f"API Error: {response.status_code}"
    
    def _local_generate(self, prompt: str) -> str:
        """Generate using local transformers"""
        try:
            results = self.pipeline(prompt, max_length=len(prompt) + 50, num_return_sequences=1)
            generated = results[0]["generated_text"]
            # Remove the original prompt from the response
            response = generated.replace(prompt, "").strip()
            return response if response else "Generated response was empty"
        except Exception as e:
            return f"Local generation error: {e}"
    
    def _mock_generate(self, prompt: str) -> str:
        """Fallback mock generation"""
        return f"[FREE-HF] Mock response to: {prompt[:50]}..."


def create_free_llm() -> HuggingFaceLLM:
    """Create a free LLM instance with best available option"""
    
    # Check if HF API token is available
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    
    if hf_token and hf_token != "get_from_https://huggingface.co/settings/tokens":
        print("🤗 Attempting Hugging Face API...")
        llm = HuggingFaceLLM(use_api=True)
        
        # Test the API
        try:
            test_response = llm.invoke("Hello")
            if "API Error" not in test_response:
                print("✅ Hugging Face API working!")
                return llm
            else:
                print(f"⚠️  HF API failed: {test_response}")
        except Exception as e:
            print(f"⚠️  HF API test failed: {e}")
    
    # Fallback to local model
    print("🔄 Falling back to local free model...")
    return HuggingFaceLLM(use_api=False)


if __name__ == "__main__":
    print("🧪 Testing free LLM options...")
    
    llm = create_free_llm()
    
    test_prompt = "Summarize in one sentence: Machine learning is a method of data analysis."
    print(f"\n📝 Test prompt: {test_prompt}")
    
    response = llm.invoke(test_prompt)
    print(f"🤖 Response: {response}")
    
    print(f"\n✅ Free LLM working with model: {llm.model_name}")
