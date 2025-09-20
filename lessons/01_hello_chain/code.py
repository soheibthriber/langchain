"""
Lesson 1 — Hello, Chain (Prompt → LLM → Parser)

This lesson demonstrates the fundamental LangChain pattern: PromptTemplate → ChatModel → StrOutputParser.
It emits GraphJSON v1.1 and Mermaid for visual exploration in the course viewer.

Execution modes (real only):
- OpenAI: set USE_OPENAI=1 and OPENAI_API_KEY
- Groq (default): set GROQ_API_KEY (uses e.g., llama3-8b-8192)

CLI:
    python3 lessons/01_hello_chain/code.py --text "Your input here"
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from pathlib import Path
import sys

# Ensure project root is importable when running this file directly
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from viz.tracer import GraphTracer
from viz.mermaid import to_mermaid
from dotenv import load_dotenv
load_dotenv()



@dataclass
class PromptTemplate:
    template: str

    @classmethod
    def from_template(cls, template: str) -> "PromptTemplate":
        return cls(template=template)

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)


class StrOutputParser:
    def invoke(self, text: str) -> str:
        return str(text)


class Pipe:
    """Minimal pipe operator emulation: a | b | c"""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def invoke(self, input_: Any) -> Any:
        out = self._invoke_one(self.left, input_)
        return self._invoke_one(self.right, out)

    def _invoke_one(self, fn, val):
        if hasattr(fn, "invoke"):
            return fn.invoke(val)
        # For prompt template formatting, expect dict input
        if isinstance(fn, PromptTemplate):
            return fn.format(**val)
        return fn(val)

    def __or__(self, other):
        return Pipe(self, other)


def run(text: Optional[str] = None) -> Dict[str, Any]:
    """Run the Hello Chain lesson with visual tracing."""
    tracer = GraphTracer(lesson_id="01_hello_chain")

    # Step 1: Create prompt template
    prompt = PromptTemplate.from_template("Summarize in one sentence: {text}")

    # Step 2: Configure LLM (Real providers only)
    use_openai = os.getenv("USE_OPENAI") == "1"
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    llm_label = ""
    provider = ""

    if use_openai and openai_key:
        try:
            from langchain_openai import ChatOpenAI  # type: ignore
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            llm = ChatOpenAI(model=model_name, temperature=0)
            print(f"🤖 Using OpenAI API with model: {model_name}")

            def llm_invoke(s: str) -> str:
                response = llm.invoke(s)
                return response.content if hasattr(response, 'content') else str(response)

            llm_label = f"ChatOpenAI:{model_name}"
            provider = "openai"
        except Exception as e:
            raise RuntimeError(f"OpenAI setup failed: {e}. Tip: check langchain-openai install and OPENAI_API_KEY.")
    elif groq_key:
        from groq import Groq  # type: ignore
        client = Groq(api_key=groq_key)

        # Decide model: use env override if set, else pick from available models
        model_name = os.getenv("GROQ_MODEL")
        if not model_name:
            try:
                models = client.models.list()
                ids = []
                if hasattr(models, "data"):
                    ids = [getattr(m, "id", None) or (m.get("id") if isinstance(m, dict) else None) for m in models.data]
                    ids = [i for i in ids if i]
                # Preference order
                prefs = [
                    "llama-3.1-8b-instant",
                    "llama-3.1-70b-versatile",
                    "gemma2-9b-it",
                    "mixtral-8x7b",
                ]
                chosen = None
                for p in prefs:
                    chosen = next((i for i in ids if p in i), None)
                    if chosen:
                        break
                model_name = chosen or (ids[0] if ids else "")
            except Exception:
                model_name = "llama-3.1-8b-instant"  # best-effort default
        if not model_name:
            raise RuntimeError("Groq: no available models found. Set GROQ_MODEL env to a valid model.")

        def llm_invoke(s: str) -> str:
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": s}],
                max_tokens=256,
                temperature=0,
            )
            return resp.choices[0].message.content or ""

        llm = type("_GroqLLM", (), {"model": model_name, "temperature": 0})()
        llm_label = f"Groq:{model_name}"
        provider = "groq"
        print(f"⚡ Using Groq API with model: {model_name}")
    else:
        raise RuntimeError("No real LLM configured. Set USE_OPENAI=1 with OPENAI_API_KEY or set GROQ_API_KEY. See lessons/00_setup_keys.")

    # Step 3: Create parser
    parser = StrOutputParser()

    # Step 4: Set up visual tracing
    # Add nodes with viewer-compatible types and rich data
    tracer.node("prompt", "PromptTemplate", "promptTemplate",
                data={
                    "template": prompt.template,
                    "input_variables": ["text"],
                    "template_format": "f-string",
                    "description": "Formats user input into a summarization prompt"
                }, 
                tags=["core", "input"])
    
    tracer.node("llm", llm_label, "chatModel",
                data={
                    "model": getattr(llm, 'model', ''),
                    "temperature": getattr(llm, 'temperature', 0),
                    "provider": provider,
                    "description": "Language model that generates text completions",
                    "model_type": "chat"
                }, 
                tags=["core", "llm"])
    
    tracer.node("parser", "StrOutputParser", "parser", 
                data={
                    "parser_type": "string",
                    "output_format": "str",
                    "description": "Ensures clean string output from LLM response"
                }, 
                tags=["core", "output"])

    # Add ports for explicit edge connections
    tracer.port("prompt", "in", "in", "input")
    tracer.port("prompt", "out", "out", "formatted_prompt")
    tracer.port("llm", "in", "in", "prompt")
    tracer.port("llm", "out", "out", "completion")
    tracer.port("parser", "in", "in", "text")
    tracer.port("parser", "out", "out", "parsed_output")

    # Add edges with port connections
    tracer.edge("prompt", "llm", src_port="out", dst_port="in", label="formatted prompt")
    tracer.edge("llm", "parser", src_port="out", dst_port="in", label="raw completion")
    
    # Group the chain for visual organization
    tracer.group("hello_chain", "Hello Chain", ["prompt", "llm", "parser"], "chain")

    # Step 5: Execute the chain with tracing
    input_data = {"text": text or "LangChain helps build LLM applications with modular components"}
    
    tracer.begin()
    
    # Event: Start prompt formatting
    tracer.event("invoke_start", node_id="prompt", payload={"input": input_data})
    formatted_prompt = prompt.format(**input_data)
    tracer.event("invoke_end", node_id="prompt", payload={"formatted_prompt": formatted_prompt})
    tracer.artifact("prompt", 
                   prompt=prompt.template, 
                   resolved_prompt=formatted_prompt,
                   input_variables=list(input_data.keys()),
                   input_data=input_data,
                   user_input=input_data.get("text", ""))
    
    # Event: Start LLM invocation
    tracer.event("invoke_start", node_id="llm", payload={"prompt": formatted_prompt})
    llm_output = llm_invoke(formatted_prompt)
    tracer.event("invoke_end", node_id="llm", payload={"output": llm_output})
    tracer.artifact("llm", 
                   input=formatted_prompt,
                   output=llm_output,
                   model_info={
                       "name": getattr(llm, 'model', ''), 
                       "provider": provider,
                       "temperature": getattr(llm, 'temperature', 0)
                   },
                   prompt_length=len(formatted_prompt),
                   output_length=len(llm_output))
    
    # Event: Start parsing
    tracer.event("invoke_start", node_id="parser", payload={"input": llm_output})
    final_output = parser.invoke(llm_output)
    tracer.event("invoke_end", node_id="parser", payload={"output": final_output})
    tracer.artifact("parser", 
                   input=llm_output,
                   output=final_output,
                   parser_type="string",
                   input_length=len(llm_output),
                   output_length=len(final_output),
                   processing_notes="Converted to clean string format")
    
    latency_ms = tracer.end()

    # Step 6: Export GraphJSON and Mermaid
    graphjson = tracer.export(latency_ms)
    
    # Display result
    print(f"\n📝 Result: {final_output}")
    print(f"⏱️  Total latency: {latency_ms:.1f}ms")

    # Step 7: Persist artifacts
    out_dir = os.path.dirname(__file__)
    
    # Write GraphJSON v1.1
    graph_path = os.path.join(out_dir, "graph.json")
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graphjson, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved GraphJSON: {graph_path}")

    # Write Mermaid diagram
    mermaid_path = os.path.join(out_dir, "graph.mmd")
    with open(mermaid_path, "w", encoding="utf-8") as f:
        f.write(to_mermaid(graphjson))
    print(f"🎨 Saved Mermaid: {mermaid_path}")

    return graphjson


def main() -> None:
    """CLI entry point for Lesson 1."""
    import argparse
    parser = argparse.ArgumentParser(
        description="Lesson 1 — Hello, Chain (Prompt → LLM → Parser)",
        epilog="""
Examples:
  python3 code.py --text "Explain machine learning"
  
Real API usage:
    export OPENAI_API_KEY=sk-...
    export USE_OPENAI=1
  python3 code.py --text "Summarize quantum computing"
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--text", type=str, default=None, 
                       help="Input text to summarize (default: about LangChain)")
    args = parser.parse_args()
    
    print("🔗 Lesson 1: Hello, Chain")
    print("=" * 40)
    run(text=args.text)
    print("\n✅ Lesson complete! Check graph.json and graph.mmd files.")
    print("💡 Next: Load the viewer or start the API to explore the visual flow.")


if __name__ == "__main__":
    main()
