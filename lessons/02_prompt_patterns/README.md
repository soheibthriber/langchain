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
[Question] → [Zero-Shot Prompt] → [LLM Zero] → [Parser Zero] → [Zero-Shot Result]

[Question] → [Few-Shot Prompt] → [LLM Few] → [Parser Few] → [Few-Shot Result]

[Question] → [CoT Prompt] → [LLM CoT] → [Parser CoT] → [CoT Result]
```

**Three Independent Chains:**

**Chain 1 - Zero-Shot Strategy:**
- **Zero-Shot Prompt** (`promptTemplate`): Direct question without examples
- **LLM Zero** (`llm`): Dedicated model instance for zero-shot processing
- **Parser Zero** (`parser`): Clean zero-shot output

**Chain 2 - Few-Shot Strategy:**
- **Few-Shot Prompt** (`promptTemplate`): Question with examples
- **LLM Few** (`llm`): Dedicated model instance for few-shot processing  
- **Parser Few** (`parser`): Clean few-shot output

**Chain 3 - Chain-of-Thought Strategy:**
- **CoT Prompt** (`promptTemplate`): Question with reasoning instructions
- **LLM CoT** (`llm`): Dedicated model instance for CoT processing
- **Parser CoT** (`parser`): Clean CoT output

**Edges:**
- Three independent flows: Prompt → LLM → Parser for each strategy
- Parallel execution allows direct comparison of individual strategy results

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

Contains execution data for all three independent prompt strategies:

- **Nodes**: Three prompt templates + three LLMs + three parsers (9 total)
- **Events**: Timing data for each strategy's complete chain execution
- **Artifacts**: 
  - Each prompt: template, resolved prompt, strategy type
  - Each LLM: individual inputs, outputs, model info for each strategy
  - Each parser: individual processed results for direct comparison

### Viewer Visualization

In the course viewer, you'll see:
- Three separate chains running in parallel
- Each chain shows: Prompt → LLM → Parser flow
- Runtime content for each individual strategy execution
- Clear comparison of how each strategy processes the same question
- Individual timing and output data for each approach

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
