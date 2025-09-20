# LangChain Course + Visualizer

A pragmatic, hands-on course with professional React Flow visualization of LangChain flows. This implementation uses GraphJSON v1.1 schema with events, artifacts, and interactive playback.

## Features

- **GraphJSON v1.1**: Structured format with metadata, events, artifacts, groups, ports
- **Professional Viewer**: React Flow with semantic node types, sidebar inspection, playback controls
- **Mock-friendly**: Lessons run without API keys; viewer loads local JSON or API data
- **Interactive**: Hover metrics, timeline playback, node details, prompt inspection

## Quickstart

### 1) Setup Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### 2) Run Lesson 1 (generates GraphJSON v1.1)

```bash
python3 lessons/01_hello_chain/code.py
```

Outputs:
- `lessons/01_hello_chain/graph.json` (GraphJSON v1.1 with events/artifacts)
- `lessons/01_hello_chain/graph.mmd` (Mermaid export)

### 3) Start API Server

```bash
python3 -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

API endpoints:
- `GET /api/lessons` - List available lessons
- `GET /api/runs/01_hello_chain/latest` - Get latest run for lesson
- `GET /api/mermaid/01_hello_chain` - Get Mermaid diagram

### 4) Start React Flow Viewer (optional)

```bash
cd viewer
npm install
npm run dev
```

Open http://localhost:3000

Features:
- Load GraphJSON via file upload or API
- Interactive nodes with hover metrics
- Sidebar with Overview, Prompt, Output, Events tabs
- Playback controls for event timeline
- Professional semantic node types (prompt, llm, parser)

### 5) Quick Mermaid Viewer (alternative)

```bash
python3 -m uvicorn viz.serve_mermaid:app --reload --port 8080
```

Open http://127.0.0.1:8080

### 6) OpenAI Demo (optional)

```bash
export OPENAI_API_KEY=sk-...
export USE_OPENAI=1
python3 lessons/01_hello_chain/code.py
```

## Structure

```
langchain/
  lessons/
    01_hello_chain/
      code.py          # GraphJSON v1.1 with events/artifacts
      graph.json       # Generated output
      graph.mmd        # Mermaid export
  viewer/              # React Flow app
    src/
      components/      # NodeTypes, Sidebar, PlaybackControls
      types/           # GraphJSON v1.1 schema
  api/
    main.py           # FastAPI with /runs endpoints
  viz/
    tracer.py         # GraphJSON v1.1 tracer
    mermaid.py        # Export converter
    serve_mermaid.py  # Simple viewer
  requirements.txt    # Full dependencies
```

## GraphJSON v1.1 Schema

Core fields:
- `metadata`: version, run_id, created_at, lesson_id, tags
- `nodes`: id, label, type, subType, tags, data
- `edges`: source/target with optional ports, labels
- `events`: timestamped with kind (invoke_start/end, tool_call, etc.)
- `artifacts`: per-node prompt/resolved_prompt/output/tool_io/docs
- `groups`: collapsible node collections (chain/agent/retriever)

## Course Vision

Each lesson ships with:
- **Visual**: Semantic nodes, ports, groups; clear flow representation
- **Interactive**: Hover metrics, sidebar inspection, timeline playback
- **Artifacts**: Prompts, outputs, tool I/O, retriever hits with expandable details

Planned:
- Lesson 3: RAG Mini (splitter → embeddings → vectorstore → retriever → prompt → llm)
- Tools & Agent visualization with tool call/observation edges
- Multi-run comparison and diff mode
- LangGraph state nodes with conditional edges

## Course Plan Document

For the full curriculum (modules, first 10 lessons, milestones, capstones, and optional MCP integration), see:

- docs/COURSE_PLAN.md

Use it as shared context for LLMs and collaborators to generate lesson code, visuals, and artifacts aligned with this repo.
