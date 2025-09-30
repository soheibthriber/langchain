# Lesson 2: Prompt Patterns (Zero-Shot, Few-Shot, Chain-of-Thought)

## Overview

This lesson explores three fundamental prompting strategies and compares their effectiveness. You'll see how different prompt patterns can dramatically change LLM behavior and output quality, all visualized in the course viewer.

**What you'll learn:**
- Zero-shot prompting (direct questions)
- Few-shot prompting (examples-based)
- Chain-of-thought prompting (step-by-step reasoning)
- How to compare prompt strategies visually
- When to use each pattern

## Visual Flow Diagram

```
[Question] → [Zero-Shot Prompt] ↘
[Question] → [Few-Shot Prompt]  → [LLM] → [Parser] → [Results]
[Question] → [CoT Prompt]      ↗
```

**Nodes:**
- **Zero-Shot Prompt** (`promptTemplate`): Direct question without examples
- **Few-Shot Prompt** (`promptTemplate`): Question with examples 
- **Chain-of-Thought** (`promptTemplate`): Question with reasoning instructions
- **LLM** (`llm`): Groq model processes all three strategies
- **Parser** (`parser`): Clean string output

**Edges:**
- All prompts → LLM: Different strategy inputs
- LLM → Parser: Combined outputs for comparison

## Prerequisites

```bash
export GROQ_API_KEY=... # from https://console.groq.com/keys
```

## How to Run

### Basic Usage

```bash
# Default question about machine learning
python3 lessons/02_prompt_patterns/code.py

# Custom question
python3 lessons/02_prompt_patterns/code.py --text "What is quantum computing?"
```

### Expected Output

```
🔗 Lesson 2: Prompt Patterns
========================================

📝 Zero-Shot Strategy:
   Question: What is machine learning?
   Answer: Machine learning is a subset of artificial intelligence...

📝 Few-Shot Strategy:
   Question: What is machine learning?
   Answer: Based on the examples provided, machine learning is...

📝 Chain-of-Thought Strategy:
   Question: What is machine learning?
   Answer: Let me think through this step by step...

⏱️  Total latency: 850ms
💾 Saved GraphJSON: lessons/02_prompt_patterns/graph.json
🎨 Saved Mermaid: lessons/02_prompt_patterns/graph.mmd
✅ Lesson complete! Check graph.json and graph.mmd files.
```

## Generated Artifacts

### graph.json (GraphJSON v1.1)

Contains execution data for all three prompt strategies:

- **Nodes**: Three prompt templates + LLM + parser
- **Events**: Timing data for each strategy execution
- **Artifacts**: 
  - Each prompt: template, resolved prompt, strategy type
  - LLM: inputs from all strategies, combined output, model info
  - Parser: final processed results

### Viewer Visualization

In the course viewer, you'll see:
- Three prompt nodes showing different templates
- Runtime content: original templates and resolved prompts
- LLM node displaying model info and combined processing
- Clear flow showing how strategies feed into the same model

## Key Concepts

### Zero-Shot Prompting
- Direct question without context or examples
- Fastest but potentially least accurate
- Good for simple, well-defined tasks

### Few-Shot Prompting  
- Includes 2-3 examples of desired input/output format
- Better accuracy through pattern demonstration
- Good for specific formats or styles

### Chain-of-Thought (CoT)
- Encourages step-by-step reasoning
- Best for complex problems requiring logic
- Higher token usage but better reasoning

## Next Steps

- **Lesson 3**: Structured Output (JSON schema validation)
- **Lesson 4**: Chat Memory (maintaining conversation context)

## Troubleshooting

**Different results each time?**
- LLM responses vary naturally; temperature=0 reduces but doesn't eliminate variation

**Poor performance on your question?**
- Try rephrasing or adding more context
- Some questions work better with specific strategies

**GraphJSON not generating?**
- Ensure GROQ_API_KEY is set and valid
- Check internet connection and API quotas
