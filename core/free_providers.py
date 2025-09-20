"""
Free LLM Provider Configuration
==============================

This module provides free API alternatives to OpenAI with automatic fallback.
All providers offer free tiers suitable for learning and development.

Supported Free Providers:
1. Hugging Face Inference API (free tier)
2. Google Gemini (free tier) 
3. Groq (free tier - very fast)
"""

import os
import requests
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    """Configuration for each LLM provider"""
    name: str
    requires_key: bool
    setup_url: str
    free_limits: str
    models: list
    description: str


# Provider configurations
PROVIDERS = {
    "huggingface": ProviderConfig(
        name="Hugging Face",
        requires_key=True,
        setup_url="https://huggingface.co/settings/tokens",
        free_limits="1000 requests/hour",
        models=["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill"],
        description="Free inference API with good models"
    ),
    
    "gemini": ProviderConfig(
        name="Google Gemini",
        requires_key=True, 
        setup_url="https://makersuite.google.com/app/apikey",
        free_limits="60 requests/minute",
        models=["gemini-pro", "gemini-pro-vision"],
        description="Google's latest LLM with generous free tier"
    ),
    
    "groq": ProviderConfig(
        name="Groq",
        requires_key=True,
        setup_url="https://console.groq.com/keys",
        free_limits="Very fast inference, good free tier",
        models=["llama2-70b-4096", "mixtral-8x7b-32768"],
        description="Ultra-fast inference with free tier"
    ),
    
    # Local providers removed (favor real APIs)
}


def test_huggingface_api(api_key: str) -> Tuple[bool, str]:
    """Test Hugging Face Inference API"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": "Hello"},
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Hugging Face API working"
        else:
            return False, f"HF API error: {response.status_code}"
            
    except Exception as e:
        return False, f"HF API error: {str(e)}"


def test_gemini_api(api_key: str) -> Tuple[bool, str]:
    """Test Google Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")
        
        if response.text:
            return True, "Gemini API working"
        else:
            return False, "Gemini API: No response"
            
    except ImportError:
        return False, "Gemini API: google-generativeai package not installed"
    except Exception as e:
        return False, f"Gemini API error: {str(e)}"


def test_groq_api(api_key: str) -> Tuple[bool, str]:
    """Test Groq API"""
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}],
            model="llama2-70b-4096",
            max_tokens=5
        )
        
        if response.choices[0].message.content:
            return True, "Groq API working"
        else:
            return False, "Groq API: No response"
            
    except ImportError:
        return False, "Groq API: groq package not installed"
    except Exception as e:
        return False, f"Groq API error: {str(e)}"


# Local provider tests removed


def detect_available_providers() -> Dict[str, Dict[str, Any]]:
    """Detect which providers are available and working"""
    results = {}
    
    # Test Hugging Face
    hf_key = os.getenv("HUGGINGFACE_API_TOKEN")
    if hf_key:
        working, message = test_huggingface_api(hf_key)
        results["huggingface"] = {
            "available": working,
            "message": message,
            "config": PROVIDERS["huggingface"]
        }
    
    # Test Gemini
    gemini_key = os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        working, message = test_gemini_api(gemini_key)
        results["gemini"] = {
            "available": working,
            "message": message,
            "config": PROVIDERS["gemini"]
        }
    
    # Test Groq
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        working, message = test_groq_api(groq_key)
        results["groq"] = {
            "available": working,
            "message": message,
            "config": PROVIDERS["groq"]
        }
    
    # Local providers removed
    
    return results


def print_provider_setup_guide():
    """Print setup instructions for free API providers"""
    print("\n🆓 Free LLM API Setup Guide")
    print("=" * 50)
    
    for provider_id, config in PROVIDERS.items():
        print(f"\n📡 {config.name}")
        print(f"   • Description: {config.description}")
        print(f"   • Free limits: {config.free_limits}")
        print(f"   • Models: {', '.join(config.models[:2])}...")
        if config.requires_key:
            print(f"   • Setup: Get API key at {config.setup_url}")
            env_var = f"{provider_id.upper()}_API_KEY"
            if provider_id == "gemini":
                env_var = "GOOGLE_API_KEY"
            elif provider_id == "huggingface":
                env_var = "HUGGINGFACE_API_TOKEN"
            print(f"   • Environment: {env_var}=your_key_here")
        else:
            print(f"   • Setup: Install from {config.setup_url}")
        print()
    
    print("💡 Recommended for beginners:")
    print("   1. Hugging Face (easiest setup)")
    print("   2. Google Gemini (best free tier)")
    # Local providers removed


def get_working_provider() -> Tuple[Optional[str], Optional[Dict]]:
    """Get the first working provider"""
    providers = detect_available_providers()
    
    for provider_id, info in providers.items():
        if info["available"]:
            return provider_id, info
    
    return None, None


if __name__ == "__main__":
    print("🔍 Checking available free LLM providers...")
    
    providers = detect_available_providers()
    
    if not providers:
        print("❌ No providers configured")
        print_provider_setup_guide()
    else:
        print(f"\n📊 Provider Status:")
        working_count = 0
        
        for provider_id, info in providers.items():
            status = "✅ Working" if info["available"] else "❌ Not available"
            print(f"   • {info['config'].name}: {status} - {info['message']}")
            if info["available"]:
                working_count += 1
        
        print(f"\n🎯 Summary: {working_count}/{len(providers)} providers working")
        
        if working_count == 0:
            print("\n💡 No working providers found!")
            print_provider_setup_guide()
        else:
            working_provider, info = get_working_provider()
            print(f"\n🚀 Recommended: Use {info['config'].name}")
