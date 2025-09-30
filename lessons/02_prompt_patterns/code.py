"""
Lesson 2 — Prompt Patterns (Zero-Shot, Few-Shot, Chain-of-Thought)

This lesson demonstrates three fundamental prompting strategies and compares their effectiveness.
It emits GraphJSON v1.1 with multiple prompt templates feeding into a single LLM.

Execution mode:
- Groq (default): set GROQ_API_KEY

CLI:
    python3 lessons/02_prompt_patterns/code.py --text "Your question here"
"""
from __future__ import annotations

import json
import os
import sys
import argparse
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from pathlib import Path
from time import perf_counter

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
    """Minimal prompt template implementation for the lesson."""
    template: str
    
    @classmethod
    def from_template(cls, template: str) -> 'PromptTemplate':
        return cls(template=template)
    
    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)


class StrOutputParser:
    """Simple string output parser."""
    def invoke(self, text: str) -> str:
        return text.strip() if isinstance(text, str) else str(text).strip()


def setup_groq_llm():
    """Setup Groq LLM client."""
    try:
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # Test available models and pick a good default
        try:
            models = client.models.list()
            available_models = [m.id for m in models.data if m.id]
            preferred_models = ["llama-3.1-8b-instant", "llama3-8b-8192", "mixtral-8x7b-32768"]
            
            model_name = None
            for preferred in preferred_models:
                if preferred in available_models:
                    model_name = preferred
                    break
            
            if not model_name and available_models:
                model_name = available_models[0]  # fallback to first available
            
            if not model_name:
                model_name = "llama-3.1-8b-instant"  # final fallback
                
        except Exception:
            model_name = "llama-3.1-8b-instant"  # fallback if listing fails
            
        print(f"⚡ Using Groq API with model: {model_name}")
        
        class GroqLLM:
            def __init__(self, client, model):
                self.client = client
                self.model = model
                self.temperature = 0
                
            def invoke(self, prompt: str) -> str:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature
                )
                return response.choices[0].message.content
        
        return GroqLLM(client, model_name)
        
    except ImportError:
        raise ImportError("groq package not installed. Run: pip install groq")
    except KeyError:
        raise KeyError("GROQ_API_KEY not found in environment variables")


def run(text: Optional[str] = None) -> Dict[str, Any]:
    """Run the Prompt Patterns lesson with visual tracing."""
    tracer = GraphTracer(lesson_id="02_prompt_patterns")
    
    # Step 1: Create three prompt strategies
    question = text or "What is machine learning?"
    
    zero_shot = PromptTemplate.from_template(
        "Answer this question clearly and concisely: {question}"
    )
    
    few_shot = PromptTemplate.from_template("""Examples of good answers:
Q: What is artificial intelligence?
A: Artificial intelligence (AI) is a field of computer science focused on creating systems that can perform tasks typically requiring human intelligence, such as learning, reasoning, and problem-solving.

Q: What is deep learning?
A: Deep learning is a subset of machine learning that uses neural networks with multiple layers to learn complex patterns in large amounts of data.

Q: {question}
A:""")
    
    chain_of_thought = PromptTemplate.from_template(
        "Think step by step to answer this question: {question}\n\nLet me break this down:"
    )
    
    # Step 2: Configure LLM
    llm = setup_groq_llm()
    parser = StrOutputParser()
    
    # Step 3: Set up visual tracing
    tracer.node("zero_shot", "Zero-Shot Prompt", "promptTemplate",
                data={
                    "strategy": "zero_shot",
                    "template": zero_shot.template,
                    "description": "Direct question without examples or guidance"
                },
                tags=["prompt", "zero-shot"])
    
    tracer.node("few_shot", "Few-Shot Prompt", "promptTemplate", 
                data={
                    "strategy": "few_shot",
                    "template": few_shot.template,
                    "description": "Question with examples to demonstrate desired format"
                },
                tags=["prompt", "few-shot"])
    
    tracer.node("cot", "Chain-of-Thought", "promptTemplate",
                data={
                    "strategy": "chain_of_thought", 
                    "template": chain_of_thought.template,
                    "description": "Question encouraging step-by-step reasoning"
                },
                tags=["prompt", "chain-of-thought"])
    
    tracer.node("llm", f"Groq:{llm.model}", "llm",
                data={
                    "model": llm.model,
                    "temperature": llm.temperature,
                    "provider": "groq",
                    "description": "Language model processing all three strategies",
                    "model_type": "chat"
                },
                tags=["core", "llm"])
    
    tracer.node("parser", "StrOutputParser", "parser",
                data={
                    "parser_type": "string",
                    "description": "Ensures clean string output from all strategies"
                },
                tags=["core", "output"])
    
    # Step 4: Add edges
    tracer.edge("zero_shot", "llm", "zero-shot strategy")
    tracer.edge("few_shot", "llm", "few-shot strategy") 
    tracer.edge("cot", "llm", "chain-of-thought strategy")
    tracer.edge("llm", "parser", "combined outputs")
    
    # Step 5: Create group
    tracer.group("prompt_comparison", "Prompt Strategy Comparison",
                 ["zero_shot", "few_shot", "cot", "llm", "parser"],
                 "chain", collapsed=False)
    
    # Step 6: Execute and trace
    tracer.begin()
    
    strategies = [
        ("zero_shot", zero_shot, "Zero-Shot"),
        ("few_shot", few_shot, "Few-Shot"), 
        ("cot", chain_of_thought, "Chain-of-Thought")
    ]
    
    results = {}
    
    print(f"\n🔗 Lesson 2: Prompt Patterns")
    print("=" * 40)
    print(f"Question: {question}\n")
    
    for strategy_id, prompt, strategy_name in strategies:
        # Trace prompt formatting
        tracer.event("invoke_start", strategy_id, 
                    payload={"input": {"question": question}})
        
        resolved_prompt = prompt.format(question=question)
        
        tracer.artifact(strategy_id,
                       template=prompt.template,
                       input_variables=["question"],
                       resolved_prompt=resolved_prompt,
                       strategy_type=strategy_id,
                       user_input=question)
        
        tracer.event("invoke_end", strategy_id,
                    payload={"resolved_prompt": resolved_prompt[:100] + "..."})
        
        # Execute via LLM
        tracer.event("invoke_start", "llm",
                    payload={"strategy": strategy_id, "input_preview": resolved_prompt[:100]})
        
        response = llm.invoke(resolved_prompt)
        results[strategy_id] = response
        
        tracer.event("invoke_end", "llm", 
                    payload={"strategy": strategy_id, "output_preview": response[:100]})
        
        print(f"📝 {strategy_name} Strategy:")
        print(f"   Answer: {response[:150]}{'...' if len(response) > 150 else ''}")
        print()
    
    # Trace final parsing
    tracer.event("invoke_start", "parser",
                payload={"strategies_processed": len(results)})
    
    combined_output = "\n\n".join([f"{k}: {v}" for k, v in results.items()])
    final_output = parser.invoke(combined_output)
    
    tracer.event("invoke_end", "parser",
                payload={"output_preview": "Processed all strategy outputs"})
    
    # Add comprehensive artifacts
    tracer.artifact("llm",
                   input=f"Processed {len(results)} different prompt strategies",
                   output=combined_output,
                   model_info={
                       "name": llm.model,
                       "provider": "groq",
                       "temperature": llm.temperature
                   },
                   strategies_used=list(results.keys()),
                   total_strategies=len(results))
    
    tracer.artifact("parser",
                   input=combined_output,
                   output=final_output,
                   parser_type="string",
                   strategies_count=len(results),
                   processing_notes="Combined outputs from all prompt strategies")
    
    latency_ms = tracer.end()
    
    print(f"⏱️  Total latency: {latency_ms:.0f}ms")
    
    # Step 7: Export GraphJSON and Mermaid
    graphjson = tracer.export(latency_ms)
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
    """CLI entry point for Lesson 2."""
    parser = argparse.ArgumentParser(
        description="Lesson 2 — Prompt Patterns (Zero-Shot, Few-Shot, Chain-of-Thought)",
        epilog="""
Examples:
  python3 code.py --text "What is quantum computing?"
  python3 code.py --text "How do neural networks work?"
  
API usage:
  export GROQ_API_KEY=your_key_here
  python3 code.py --text "Explain blockchain technology"
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--text", type=str, default=None,
                       help="Question to analyze with different prompt strategies (default: about machine learning)")
    args = parser.parse_args()
    
    run(text=args.text)
    print("\n✅ Lesson complete! Check graph.json and graph.mmd files.")
    print("💡 Next: Load the viewer or start the API to explore the visual comparison.")


if __name__ == "__main__":
    main()
