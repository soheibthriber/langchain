"""
Lesson 1 — Hello, Chain (Prompt -> LLM -> Parser)

This demo runs with or without a real LLM key.
By default, it uses a mock LLM to keep the repo runnable out of the box.
Set OPENAI_API_KEY and set USE_OPENAI=1 to use a real model.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict
from pathlib import Path
import sys

# Ensure project root is importable when running this file directly
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from viz.tracer import GraphTracer
from viz.mermaid import to_mermaid


@dataclass
class MockLLM:
    """A tiny stand-in for a chat model so the lesson runs anywhere."""

    model: str = "mock-llm"
    temperature: float = 0.0

    def invoke(self, prompt: str) -> str:
        return f"[MOCK:{self.model}] summary: {prompt[:60]}..."


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


def run() -> Dict[str, Any]:
    tracer = GraphTracer(lesson_id="01_hello_chain")

    prompt = PromptTemplate.from_template("Summarize in one sentence: {text}")

    use_openai = os.getenv("USE_OPENAI") == "1"
    if use_openai:
        try:
            from langchain_openai import ChatOpenAI  # type: ignore
            llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
            llm_label = f"ChatOpenAI:{getattr(llm, 'model', 'openai')}"
            llm_invoke = lambda s: llm.invoke(s).content  # noqa: E731
        except Exception as e:
            print(f"Falling back to MockLLM (reason: {e})")
            llm = MockLLM()
            llm_label = f"MockLLM:{llm.model}"
            llm_invoke = llm.invoke
    else:
        llm = MockLLM()
        llm_label = f"MockLLM:{llm.model}"
        llm_invoke = llm.invoke

    class LLMWrapper:
        def invoke(self, s: str) -> str:
            return llm_invoke(s)

    llm_node = LLMWrapper()
    parser = StrOutputParser()

    # Visual nodes/edges with v1.1 schema
    tracer.node("prompt", "PromptTemplate", "prompt", 
                data={"template": prompt.template}, tags=["core"])
    tracer.node("llm", llm_label, "llm", 
                data={"model": llm.model if hasattr(llm, 'model') else "mock"}, tags=["core"])
    tracer.node("parser", "StrOutputParser", "parser", tags=["core"])
    
    tracer.edge("prompt", "llm")
    tracer.edge("llm", "parser")
    
    # Create a simple group for the chain
    tracer.group("hello_chain", "Hello Chain", ["prompt", "llm", "parser"], "chain")

    chain = Pipe(prompt, llm_node) | parser
    input_data = {"text": "LangChain helps build LLM apps"}

    tracer.begin()
    
    # Event: chain starts
    tracer.event("invoke_start", node_id="prompt", payload={"input": input_data})
    
    # Format the prompt
    formatted_prompt = prompt.format(**input_data)
    tracer.artifact("prompt", prompt=prompt.template, resolved_prompt=formatted_prompt)
    
    # Event: LLM invoke starts
    tracer.event("invoke_start", node_id="llm", payload={"prompt": formatted_prompt})
    
    # Run the chain
    result = chain.invoke(input_data)
    
    # Event: LLM invoke ends
    tracer.event("invoke_end", node_id="llm", payload={"output": result})
    tracer.artifact("llm", output=result)
    
    # Event: parser processes
    tracer.event("invoke_start", node_id="parser")
    tracer.event("invoke_end", node_id="parser", payload={"output": result})
    tracer.artifact("parser", output=result)
    
    latency_ms = tracer.end()

    graphjson = tracer.export(latency_ms)
    print(result)

    # Persist artifacts for the lesson
    out_dir = os.path.dirname(__file__)
    with open(os.path.join(out_dir, "graph.json"), "w", encoding="utf-8") as f:
        json.dump(graphjson, f, indent=2)

    with open(os.path.join(out_dir, "graph.mmd"), "w", encoding="utf-8") as f:
        f.write(to_mermaid(graphjson))

    return graphjson


if __name__ == "__main__":
    run()
