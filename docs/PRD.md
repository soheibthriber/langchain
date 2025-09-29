# Product Requirements Document (PRD): LangChain Agentic AI Course + Visualizer

## 1. Vision
Deliver a visual‑first, hands‑on course that teaches agentic AI with LangChain and MCP. Every lesson produces a runnable script and a visual execution trace (GraphJSON) rendered in a professional React Flow viewer. Groq is the default LLM provider; OpenAI/HF/Pinecone are optional. Local dev uses the FastAPI backend; production is a static viewer on GitHub Pages loading prebuilt graphs.

## 2. Goals
- Visualize real runtime content for each step (input → processing → output).
- Gradually progress from prompts to agents, tools, RAG, LangGraph and MCP.
- Keep setup simple (Lesson 0 keys) and reproducible (CI builds sample graphs).
- Use a clear data contract (GraphJSON v1.1) across lessons → API → viewer.

## 3. Non‑Goals
- Full LangChain surface coverage or vendor parity.
- Private deployments of the viewer; Pages is public.
- Heavy infra (self‑hosted vector DBs, complex auth flows) in the core repo.

## 4. Audience & Outcomes
- Audience: Python developers and AI practitioners.
- Outcomes: Design, build, and visualize agentic workflows with real providers; understand tracing, retrieval, tools, planning, and MCP integration.

## 5. Principles
- Visual first; pedagogy by showing real data.
- Real providers by default (Groq), mockless.
- Minimal moving parts; progressive complexity.
- Clean separation of concerns (lessons • core tracer • API • viewer).

## 6. Architecture (high‑level)
- lessons/: runnable scripts emit GraphJSON + Mermaid per lesson.
- viz/: tracer + exporters (GraphJSON → Mermaid).
- api/: FastAPI to run lessons and serve latest graphs locally.
- viewer/: React Flow viewer that loads GraphJSON and renders runtime node content.
- CI: GitHub Actions builds one or more lesson graphs and deploys viewer to Pages.

## 7. Data Contract (GraphJSON v1.1)
- metadata: { version, lesson_id, run_id?, created_at, tags? }
- nodes: [{ id, label, type, category?, color?, icon?, data? }]
- edges: [{ id?, source, target, label? }]
- events: [{ nodeId, kind: invoke_start|invoke_end|error, input_preview?, output_preview?, execution_time_ms?, timestamp }]
- artifacts: object keyed by nodeId with per‑type details
  - promptTemplate: { template, input_variables, resolved_prompt }
  - llm: { input, output, model_info: { provider, name } }
  - parser: { input, output, parser_type }
  - future types: tool I/O, retriever docs, vector stats, planner steps, MCP messages
- run: { latency_ms?, tokens_in?, tokens_out?, cost?, errors? }
- groups (optional): collapse/expand subgraphs.
- styles (optional): per‑type overrides consumed by the viewer.

Acceptance: viewer must render nodes with meaningful runtime content using artifacts and events; API and CI must output valid GraphJSON with these fields.

## 8. Subsystems (requirements)

### 8.1 Lessons (authoring)
- Each lesson folder contains: code.py, README.md, graph.json, graph.mmd.
- Must call real providers (Groq default). Use load_dotenv; no keys in code.
- Emit GraphJSON with nodes, edges, events, artifacts, run.
- L0: keys setup checker; L1: Prompt → LLM → Parser; later lessons: memory, RAG (Pinecone), tools, agents, LangGraph, MCP.
- Return clear console output, write artifacts to lesson folder.

### 8.2 Core (tracer & adapters)
- Tracer APIs to:
  - define nodes/edges; capture invoke_start/invoke_end events with timing;
  - record artifacts (prompt template+resolved, llm input/output, parser I/O);
  - aggregate run metrics; export GraphJSON v1.1.
- Optional registry metadata for color/icon/category, but runtime content is primary.
- Future adapters: LangGraph, MCP events → GraphJSON.

### 8.3 API (FastAPI)
- GET /api/runs/{lesson_id}/latest: read lessons/{id}/graph.json.
- POST /api/run/{lesson_id}: execute code.py for that lesson and return GraphJSON.
- CORS enabled for dev viewer; JSON errors; never block on long runs.

### 8.4 Viewer (React + React Flow)
- Dev mode: prefer API; fallback to static graph.json.
- Pages mode: load ${BASE_URL}graph.json (CI copies it to viewer/public).
- Node types: promptTemplate, llm, parser (+ retriever, embeddings, vectorstore, tool, agent, memory, planner as needed).
- Render runtime content:
  - Prompt: template, variables, resolved prompt.
  - LLM: provider badge (Groq), model, input, output.
  - Parser: input, output, type.
- Inspector shows metadata; nodes show concise execution content.
- Optional enhancements: timing/token chips, error toasts, lesson selector.

## 9. Provider Strategy & Secrets
- Default: Groq; set GROQ_API_KEY in .env (local) or GitHub Secrets (CI).
- Optional: OpenAI, HF, Pinecone; add only when a lesson needs them.
- Never expose keys in the frontend; keys live in CI or local .env only.

## 10. MCP Integration Plan
- Phase 1: Treat MCP tools as LangChain Tools via a thin client adapter.
  - Node/edge semantics: agent → (tool_call) → mcp_tool → observation.
  - Artifacts: tool catalogs, request/response, timing.
- Phase 2: Agent + MCP loop.
  - Events: tool_call, tool_result, errors; per‑step inspector.
  - Safety: tool allowlists, rate limits, redaction.
- Phase 3: MCP server demo (filesystem/HTTP) + adapter; visualize session lifecycle.

## 11. Curriculum Roadmap
- Phase 0 (Setup)
  - L00 Keys: Groq (default), Pinecone/HF optional, checker script.
  - L01 Hello Chain: Prompt → LLM → Parser; artifacts rendered.
- Phase 1 (Prompting & Structure)
  - L02 Prompt Patterns; L03 Structured JSON outputs.
- Phase 2 (Memory)
  - L04 Buffer memory; L05 Summary memory.
- Phase 3 (RAG with Pinecone)
  - L06 Build index; L07 Basic RAG; L08 Reranking/Context management.
- Phase 4 (Tools)
  - L09 Function calling; L10 Web search; L11 Python tool (safe eval).
- Phase 5 (Agents)
  - L12 ReAct single‑tool; L13 Multi‑tool planning.
- Phase 6 (Planning & Multi‑Agent)
  - L14 Planner/Executor; L15 Critic/Refine; L16 Multi‑agent collaboration.
- Phase 7 (MCP)
  - L17 MCP basics; L18 MCP‑powered agent.
- Phase 8 (Eval & Observability)
  - L19 Judge/rubric; L20 Metrics (time/tokens/cost) surfaced in viewer.

Each lesson ships code.py, README.md, and renders node runtime content; viewer must show meaningful artifacts from the GraphJSON.

## 12. CI/CD (GitHub‑only)
- Steps: install → run lesson(s) → copy graph.json to viewer/public → vite build with base '/langchain/' → deploy Pages.
- Secrets: set GROQ_API_KEY in GitHub Secrets; never in client.
- For multiple lessons on Pages, copy files to viewer/public/lessons/{id}/graph.json and add a lesson selector in the viewer.

## 13. Security
- .env is gitignored; rotate any exposed keys immediately.
- Sanitize logs and artifacts; avoid leaking keys in outputs.
- Do not embed secrets in Vite env (VITE_*).

## 14. Quality Gates
- Lesson runs locally; graph.json validates (basic schema checks).
- Viewer renders nodes with runtime content for that lesson.
- API returns 200 for GET latest; POST run executes and returns GraphJSON.
- Pages site loads static graph.json under BASE_URL.

## 15. Risks & Mitigations
- Provider quotas/availability → allow provider swap; clear errors.
- Schema drift → centralize GraphJSON helpers; minimal versioning.
- Pages base path bugs → enforce BASE_URL in fetches and favicon.

## 16. Glossary
- GraphJSON: JSON document representing a run (nodes, edges, events, artifacts).
- Artifact: per‑node data blob (template, llm I/O, etc.).
- Event: timestamped step with input/output previews and timing.
- MCP: Model Context Protocol (tool transport).