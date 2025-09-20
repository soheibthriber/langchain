"""Deprecated: use code.py as the single entry point for Lesson 1."""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add the parent directory to Python path for imports  
sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# Import enhanced tracing system
from core.enhanced_tracer import create_enhanced_tracer
from viz.mermaid import to_mermaid as export_to_mermaid

# Environment setup
from dotenv import load_dotenv
load_dotenv()


def setup_llm():
    """Setup LLM with real providers only (OpenAI or Groq)."""
    use_openai = os.getenv("USE_OPENAI") == "1"
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if use_openai and openai_key and openai_key != "sk-your-actual-openai-key-here":
        from langchain_openai import ChatOpenAI
        model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        llm = ChatOpenAI(model=model_name, temperature=0, api_key=openai_key)
        print(f"🤖 Using OpenAI API with model: {model_name}")
        return llm, True, model_name

    def setup_llm():
        raise RuntimeError("code_enhanced.py is deprecated; use code.py")
                    temperature=self.temperature,
                def run_enhanced_lesson(text: str) -> Dict[str, Any]:
                    raise RuntimeError("code_enhanced.py is deprecated; use code.py")
    except Exception as e:
        print(f"⚠️  Mermaid export failed: {e}")
    
    # Print node summary
    summary = tracer.generate_node_summary()
    print(f"\n📊 Enhanced Analysis:")
    print(f"   • Nodes by category: {dict(summary['by_category'])}")
    print(f"   • Nodes by complexity: {dict(summary['by_complexity'])}")
    print(f"   • Total artifacts: {len(tracer.artifacts)}")
    print(f"   • Total events: {len(tracer.events)}")
    
    print("\n✅ Enhanced lesson complete! Check graph.json for rich metadata.")
    print("💡 Next: Load the viewer to explore enhanced visualizations.")
    
    return execution_summary


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Run enhanced Hello Chain lesson")
    parser.add_argument("--text", "-t", 
                       default="Explain how neural networks learn from data",
                       help="Text to process through the chain")
    
    args = parser.parse_args()
    
    print("code_enhanced.py is deprecated; use code.py")
    return 1


if __name__ == "__main__":
    exit(main())
