"""
Lesson 2 — Prompt Patterns (Zero-Shot, Few-Shot, Chain-of-Thought)

This lesson demonstrates three fundamental prompting strategies by creating three separate,
parallel chains for pedagogical comparison. Each strategy gets its own complete chain:
Prompt → LLM → Parser, making it easy to compare approaches and outputs.

It emits GraphJSON v1.1 with three independent chains for educational visualization.

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
    
    # Step 2: Configure LLM and parsers
    llm = setup_groq_llm()
    
    # Create separate parsers for each strategy to show individual outputs
    zero_shot_parser = StrOutputParser()
    few_shot_parser = StrOutputParser()
    cot_parser = StrOutputParser()
    
    # Step 3: Set up visual tracing with separate chains
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
    
    # Create separate LLM nodes for clarity (same model, different instances)
    tracer.node("llm_zero", f"Groq:{llm.model}", "llm",
                data={
                    "model": llm.model,
                    "temperature": llm.temperature,
                    "provider": "groq",
                    "description": "Zero-shot strategy execution",
                    "model_type": "chat",
                    "strategy": "zero_shot"
                },
                tags=["core", "llm", "zero-shot"])
                
    tracer.node("llm_few", f"Groq:{llm.model}", "llm",
                data={
                    "model": llm.model,
                    "temperature": llm.temperature,
                    "provider": "groq",
                    "description": "Few-shot strategy execution",
                    "model_type": "chat",
                    "strategy": "few_shot"
                },
                tags=["core", "llm", "few-shot"])
                
    tracer.node("llm_cot", f"Groq:{llm.model}", "llm",
                data={
                    "model": llm.model,
                    "temperature": llm.temperature,
                    "provider": "groq",
                    "description": "Chain-of-thought strategy execution",
                    "model_type": "chat",
                    "strategy": "chain_of_thought"
                },
                tags=["core", "llm", "chain-of-thought"])
    
    tracer.node("parser_zero", "Zero-Shot Parser", "parser",
                data={
                    "parser_type": "string",
                    "description": "Processes zero-shot strategy output",
                    "strategy": "zero_shot"
                },
                tags=["core", "output", "zero-shot"])
                
    tracer.node("parser_few", "Few-Shot Parser", "parser",
                data={
                    "parser_type": "string",
                    "description": "Processes few-shot strategy output",
                    "strategy": "few_shot"
                },
                tags=["core", "output", "few-shot"])
                
    tracer.node("parser_cot", "Chain-of-Thought Parser", "parser",
                data={
                    "parser_type": "string",
                    "description": "Processes chain-of-thought strategy output",
                    "strategy": "chain_of_thought"
                },
                tags=["core", "output", "chain-of-thought"])
    
    # Step 4: Add edges for three separate chains
    tracer.edge("zero_shot", "llm_zero", "zero-shot prompt")
    tracer.edge("llm_zero", "parser_zero", "zero-shot response")
    
    tracer.edge("few_shot", "llm_few", "few-shot prompt")
    tracer.edge("llm_few", "parser_few", "few-shot response")
    
    tracer.edge("cot", "llm_cot", "chain-of-thought prompt")
    tracer.edge("llm_cot", "parser_cot", "chain-of-thought response")
    
    # Step 5: Create separate groups for each strategy
    tracer.group("zero_shot_chain", "Zero-Shot Strategy",
                 ["zero_shot", "llm_zero", "parser_zero"],
                 "chain", collapsed=False)
                 
    tracer.group("few_shot_chain", "Few-Shot Strategy",
                 ["few_shot", "llm_few", "parser_few"],
                 "chain", collapsed=False)
                 
    tracer.group("cot_chain", "Chain-of-Thought Strategy",
                 ["cot", "llm_cot", "parser_cot"],
                 "chain", collapsed=False)
    
    # Step 6: Execute and trace three separate chains
    tracer.begin()
    
    strategies = [
        ("zero_shot", zero_shot, "Zero-Shot", "llm_zero", "parser_zero", zero_shot_parser),
        ("few_shot", few_shot, "Few-Shot", "llm_few", "parser_few", few_shot_parser), 
        ("cot", chain_of_thought, "Chain-of-Thought", "llm_cot", "parser_cot", cot_parser)
    ]
    
    results = {}
    
    print(f"\n🔗 Lesson 2: Prompt Patterns (Three Separate Chains)")
    print("=" * 55)
    print(f"Question: {question}\n")
    
    for strategy_id, prompt, strategy_name, llm_id, parser_id, parser in strategies:
        print(f"📝 Executing {strategy_name} Strategy Chain:")
        
        # Step 1: Trace prompt formatting
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
        
        # Step 2: Execute via LLM
        tracer.event("invoke_start", llm_id,
                    payload={"strategy": strategy_id, "input_preview": resolved_prompt[:100]})
        
        llm_response = llm.invoke(resolved_prompt)
        
        tracer.event("invoke_end", llm_id, 
                    payload={"strategy": strategy_id, "output_preview": llm_response[:100]})
        
        # Add LLM artifacts
        tracer.artifact(llm_id,
                       input=resolved_prompt,
                       output=llm_response,
                       model_info={
                           "name": llm.model,
                           "provider": "groq",
                           "temperature": llm.temperature
                       },
                       strategy=strategy_id)
        
        # Step 3: Parse the output
        tracer.event("invoke_start", parser_id,
                    payload={"input_preview": llm_response[:100]})
        
        final_output = parser.invoke(llm_response)
        results[strategy_id] = final_output
        
        tracer.event("invoke_end", parser_id,
                    payload={"output_preview": final_output[:100]})
        
        # Add parser artifacts
        tracer.artifact(parser_id,
                       input=llm_response,
                       output=final_output,
                       parser_type="string",
                       strategy=strategy_id,
                       processing_notes=f"Processed {strategy_name.lower()} strategy output")
        
        print(f"   ✓ {strategy_name} Answer: {final_output[:150]}{'...' if len(final_output) > 150 else ''}")
        print()
    
    latency_ms = tracer.end()
    
    print(f"⏱️  Total latency: {latency_ms:.0f}ms")
    print(f"🎯 Comparison Summary:")
    for strategy_id, result in results.items():
        strategy_name = strategy_id.replace('_', '-').title()
        print(f"   • {strategy_name}: {len(result)} characters")
    
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
        description="Lesson 2 — Prompt Patterns: Three Parallel Chains (Zero-Shot, Few-Shot, Chain-of-Thought)",
        epilog="""
This lesson creates three separate chains to compare prompting strategies:

Chain 1: Zero-Shot → LLM → Parser  (Direct questioning)
Chain 2: Few-Shot → LLM → Parser   (Example-driven)  
Chain 3: CoT → LLM → Parser        (Step-by-step reasoning)

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
                       help="Question to analyze with three different prompt strategies (default: about machine learning)")
    args = parser.parse_args()
    
    run(text=args.text)
    print("\n✅ Lesson complete! Check graph.json and graph.mmd files.")
    print("💡 Next: Load the viewer or start the API to explore the three parallel chains.")
    print("🎓 Educational benefit: Compare how each strategy processes the same question.")


if __name__ == "__main__":
    main()
