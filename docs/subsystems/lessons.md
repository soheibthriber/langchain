# Lessons Authoring Requirements

## Structure
Each lesson lives under `lessons/{nn_name}/` and contains:
- `code.py` (runnable; generates `graph.json` and `graph.mmd`)
- `README.md` (what it teaches, how to run)
- `graph.json` (GraphJSON v1.1 artifact)
- `graph.mmd` (Mermaid flowchart, optional but recommended)

## Runtime Rules
- Use real providers (Groq default). Load keys via `.env` (local) or CI Secrets.
- Do not include secrets in code or artifacts.
- Emit GraphJSON fields:
  - nodes, edges, run
  - events: invoke_start/invoke_end with input/output previews and timing
  - artifacts: per-node data (prompt template/resolved; llm input/output/model_info; parser input/output)

## Required Lessons
- L00 Setup Keys: guide + checker for GROQ_API_KEY (and Pinecone/HF optional).
- L01 Hello Chain: Prompt → LLM (Groq) → Parser; graph renders runtime content.

## Roadmap Lessons
- Prompting & Structure: L02 Prompt patterns; L03 Structured outputs.
- Memory: L04 Buffer; L05 Summary memory.
- RAG with Pinecone: L06 Build index; L07 Basic RAG; L08 Reranking/context.
- Tools: L09 Function calling; L10 Web search; L11 Python tool (safe eval).
- Agents: L12 ReAct; L13 Multi‑tool planning.
- Planning & Multi‑Agent: L14 Planner/Executor; L15 Critic/Refine; L16 Multi‑agent.
- MCP: L17 MCP basics; L18 MCP‑powered agent.
- Eval & Observability: L19 Judge/rubric; L20 Metrics (time/tokens/cost).

## Authoring Checklist
- `load_dotenv()`; read provider keys from env.
- Create prompt/llm/parser chain; instrument tracer events and artifacts.
- Write outputs to lesson folder; print result to stdout.
- Keep README concise: overview, keys, run commands, expected outputs.
