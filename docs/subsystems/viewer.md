# Viewer Subsystem Requirements (React + Vite + React Flow)

This document reflects the current implementation under `viewer/` and sets expectations for future work. It is accurate to the checked-in files:
- Vite config: `vite.config.ts` (base '/langchain/', dev proxy `/api` → 127.0.0.1:8000)
- App shell and data loading: `src/App.tsx`
- Node renderers: `src/components/SpecializedNodes.tsx`
- Entry/CSS: `src/main.tsx`, `src/index.css`
- Docs: this file and `DESIGN_PLAN.md`, `N8N_STYLE_ANALYSIS.md`

## Goals
- Render runtime execution content inside nodes using GraphJSON artifacts/events.
- Work in both environments:
  - Dev: API-first (FastAPI) with static fallback
  - GitHub Pages: static graph under `${BASE_URL}` (no API)
- Keep UI simple and readable; per-node content over heavy metadata.

## Current Implementation Snapshot
- React 18 + Vite + React Flow 11
- Vite base is set to `/langchain/` for Pages; dev proxy maps `/api` to `http://127.0.0.1:8000`.
- `App.tsx` buttons:
  - "📊 Load Sample (Lesson 1)": loads from API (dev) or static `${BASE_URL}graph.json` (Pages), with fallback.
  - "▶️ Run Lesson (Groq)": POSTs `/api/run/01_hello_chain` (dev); falls back to sample loader if API fails.
- `SpecializedNodes.tsx` provides compact, content-first nodes:
  - `promptTemplate`: shows template, inputs, resolved prompt
  - `llm`: shows provider badge (⚡ GROQ), model, prompt and response
  - `parser`: shows input, output, parser type
  - `memory`, `tool`, `chain`: stylistic shells (execution data TBD for those lessons)

## Data Loading & Environment
- Env sources used in `App.tsx`:
  - `import.meta.env.DEV` → sets `preferApi` in dev
  - `import.meta.env.VITE_API_BASE_URL` → if present, force API mode to that origin
  - `import.meta.env.BASE_URL` → to resolve static assets/graph on Pages (`/langchain/`)
- URL selection logic:
  - API-first: `${apiPrefix}/api/runs/01_hello_chain/latest` (dev, via proxy unless VITE_API_BASE_URL set)
  - Static fallback: `${BASE_URL}graph.json` (Pages build copies here in CI)
- Error handling: Try primary source then fallback; warn in console on failure.

## GraphJSON Ingestion Pipeline
- Accepts GraphJSON v1.1 (current lessons) and includes minimal support for v1.2 hints.
- Normalizes node types to renderer keys:
  - `PromptTemplate|promptTemplate|prompt` → `promptTemplate`
  - `llm|chatModel|ChatOpenAI|ChatAnthropic|Groq` → `llm`
  - `parser|StrOutputParser` → `parser`
- Edges: supports `source/target` as strings or `{ nodeId, portId? }` objects; edges are animated and show labels when present.

### Building Execution Artifacts (what nodes display)
In `App.tsx`, after fetching the graph:
- Determine version: `data.metadata.version` (defaults to `1.1`).
- Collect `events` and `artifacts` from the graph.
- For v1.1, artifacts are keyed by node id names; we map:
  - prompt → `{ template|prompt, input_variables, resolved_prompt }`
  - llm → `{ input, output, model_info }`
  - parser → `{ input, output, parser_type }`
- These are injected into each node’s `data.artifacts` and consumed by `SpecializedNodes` components.

## Node Rendering Contract (exact fields)
Each React Flow `Node.data` contains:
- `label`: string (node label)
- `type`: normalized viewer type (`promptTemplate|llm|parser|…`)
- `nodeData`: the original GraphJSON node object (for inspector)
- `artifacts`: execution data injected by the loader

`SpecializedNodes` currently read `artifacts` as follows:
- PromptTemplateNode
  - `template` (or `prompt`), `input_variables`, `resolved_prompt`
- LLMNode
  - `input`, `output`, `model_info { provider?, name? }`
  - Provider badge: if `provider==='groq'`, show ⚡ GROQ
- ParserNode
  - `parser_type`, `input`, `output`

## UI & Interaction
- Nodes are compact cards with a colored top accent, icon, label, and concise execution content.
- Inspector panel shows the selected node’s `data`, including `nodeData` and `artifacts` (raw view).
- React Flow features enabled: `MiniMap`, `Controls`, dotted `Background`, selection tracking.

## Build & Deploy
- `vite.config.ts`:
  - `base: '/langchain/'` ensures assets resolve to `/langchain/*` on GitHub Pages.
  - Dev server `proxy: { '/api': 'http://127.0.0.1:8000' }`.
- `index.html` favicon path uses `%BASE_URL%vite.svg` (works in dev and Pages).
- GitHub Actions (Pages workflow) must:
  1) Run `lessons/01_hello_chain/code.py` to regenerate `lessons/01_hello_chain/graph.json`.
  2) Copy it to `viewer/public/graph.json`.
  3) `npm ci && npm run build` in `viewer/`.
  4) Deploy `viewer/dist/` to Pages.

## Local Dev Procedure
1) Start API: `python3 -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000`
2) Start viewer: `cd viewer && npm run dev`
3) Click "Run Lesson (Groq)" to POST/execute via API, or "Load Sample (Lesson 1)" (falls back to static if API fails).

Optional: create `viewer/.env.development` with `VITE_API_BASE_URL=http://127.0.0.1:8000` to force API mode without relying on proxy.

## Error Handling & Troubleshooting
- 404 `/graph.json` in dev: means static fallback attempted; ensure API is running or set `VITE_API_BASE_URL`.
- 404 assets on Pages: ensure `vite.config.ts` has `base: '/langchain/'` and favicon uses `%BASE_URL%`.
- Pending `/api/...` in dev: restart API; verify CORS (already enabled for 3000/3001).

## Extensibility Plan
- Lessons selector:
  - Dev: `/api/runs/{id}/latest` and `/api/run/{id}`.
  - Pages: `${BASE_URL}lessons/{id}/graph.json` (CI copies multiple graphs).
- New node types (retriever, embeddings, vectorstore, tool, agent, memory, planner):
  - Extend `SpecializedNodes` with execution-aware components for each type.
  - Extend artifacts building logic in `App.tsx` to map new per-node artifacts.
- Visual enhancements: timing/token chips; expand/collapse long text; error toasts; active-edge highlighting during playback.

## Acceptance Criteria
- Dev: Clicking "Run Lesson (Groq)" performs a POST run and updates the canvas; "Load Sample" loads latest via API and falls back to static.
- Pages: Clicking "Load Sample" fetches `${BASE_URL}graph.json` and renders nodes with execution content.
- LLM nodes display a provider badge and model name when available; Prompt/Parser nodes show their execution data.
