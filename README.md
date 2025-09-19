# LangChain Course + Visualizer (MVP)

A pragmatic, hands-on mini-curriculum. This MVP ships a tiny tracer that emits GraphJSON and converts it to Mermaid for quick visual graphs. Lesson 1 runs with a mock LLM by default, so you can try it without any keys.

## Quickstart

Requirements:
- Python 3.10+ (use `python3` on Linux)
- Optional: `langchain-openai` if you want real OpenAI calls

### 1) Create and activate a virtualenv (recommended)

```
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```
pip install -U pip
pip install -r requirements.txt
```

### 3) Run Lesson 1 (mock LLM by default)

```
python3 lessons/01_hello_chain/code.py
```

Artifacts created:
- `lessons/01_hello_chain/graph.json` (GraphJSON)
- `lessons/01_hello_chain/graph.mmd` (Mermaid)

### 4) Run with OpenAI (optional)

Export your key and flip the switch:

```
export OPENAI_API_KEY=sk-...
export USE_OPENAI=1
python3 lessons/01_hello_chain/code.py
```

Optionally pick a model:

```
export OPENAI_MODEL=gpt-4o-mini
```

> If import fails, the script automatically falls back to the mock LLM.

## Structure (current)

```
langchain/
  lessons/
    01_hello_chain/
      code.py          # runnable example, outputs GraphJSON + Mermaid
  viz/
    tracer.py          # minimal GraphJSON tracer
    mermaid.py         # GraphJSON -> Mermaid converter
  requirements.txt     # deps for current + planned lessons
  README.md
```

## Optional: Docs site (MkDocs)

After installing requirements, you can start a local docs site later:

```
# Example (to be scaffolded in a next step)
# mkdocs serve
```

## Optional: API server (FastAPI)

A tiny `/trace` endpoint will be added soon. Once available:

```
# Example (to be added)
# uvicorn app:app --reload
```

## Visualize the graph

Serve the Mermaid diagram locally (after running Lesson 1):

```
source .venv/bin/activate
python3 -m uvicorn viz.serve_mermaid:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Next Steps (planned)

- Lesson 3 (RAG mini) with the same tracer, emitting a larger graph.
- Tiny FastAPI endpoint `/trace` to serve GraphJSON for a React Flow app.
- MkDocs site scaffolding with Mermaid enabled for lesson docs.
- React Flow viewer (Phase 2) with node types and a side panel.
