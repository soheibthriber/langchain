# LangChain Mastery — Visual-First Course Plan

Author: Course scaffold generated for collaborative iteration
Status: Draft v0.1

This document describes a progressive, visual-first curriculum for mastering LangChain, aligned with this repository’s GraphJSON tracer, FastAPI server, and React Flow viewer. It is intended as a base for LLM-assisted content generation and team collaboration.

## Scope and Philosophy

- Visual-first: Each lesson ships with a diagram (GraphJSON → React Flow) and an optional Mermaid export.
- Progressive complexity: Foundation → Composition → Specialization → Production.
- Hands-on: Every lesson includes runnable code and a practical exercise.
- Production-minded: Telemetry, evals, caching, and deployment patterns appear early.

## How MCP Fits (Model Context Protocol)

MCP is not part of LangChain’s core API surface, but it complements this course in two ways:
- As a tool transport layer: MCP servers expose tools/resources in a standardized way; LangChain tools can wrap MCP clients.
- As an orchestration bridge: You can host tools (search, DB, filesystem) behind MCP and let agents call them safely.

Recommended integration points:
- Module 4 (Tools & Agents): optional lessons showing a LangChain `Tool` wrapper around an MCP client; security/permissions and schema validation.
- Module 7 (Productionization): operational concerns—authentication to MCP servers, rate limits, observability, and failure handling.

Notes:
- Keep MCP as optional tracks so students can complete the course with pure LangChain.
- Favor typed/structured tool schemas and explicit allowlists to avoid over-broad capabilities.

## Modules Overview

- Module 1 — Foundations of LangChain and Visual Flows (4 lessons, ~3–4 hours)
  - Objectives: Understand chains, prompts, LLMs, output parsing, GraphJSON tracing, and the viewer basics.
  - Components: PromptTemplate, ChatModel/LLM, StrOutputParser, callbacks/tracer.

- Module 2 — Composition: Chains, Memory, and Control Flow (4 lessons, ~4–5 hours)
  - Objectives: Compose chains, add memory types, route conditionally, handle input/output schemas.
  - Components: RunnableSequence, ConversationBufferMemory, RouterChain.

- Module 3 — RAG Fundamentals (5 lessons, ~6–7 hours)
  - Objectives: Build mini-RAG: loaders, splitters, embeddings, vector stores, retriever → prompt → LLM.
  - Components: DocumentLoader, TextSplitter, Embeddings, Chroma/FAISS, Retriever.

- Module 4 — Tools and Agents (5 lessons, ~6–7 hours)
  - Objectives: Use tools safely; create an agent that plans, calls tools, and reasons; inject memory.
  - Components: Tool, StructuredTool, ReAct Agent, tool I/O artifacts.
  - Optional MCP Track: Wrap an MCP client as a LangChain tool; auth and capability scoping.

- Module 5 — Workflows at Scale (LangGraph/Flow) (4 lessons, ~5–6 hours)
  - Objectives: Model branching state machines, retries, timeouts, and guards; visualize conditional edges.
  - Components: LangGraph nodes/edges, state policies, error boundaries.

- Module 6 — Retrieval+Generation Excellence (4 lessons, ~5–6 hours)
  - Objectives: Improve retrieval quality, re-ranking, query transforms, multi-vector stores, citations.
  - Components: Context compression, rerankers, retriever chains, citations.

- Module 7 — Productionization and Observability (4 lessons, ~4–5 hours)
  - Objectives: Tracing, metrics, evals, caching, testing, deployment with FastAPI.
  - Components: Callbacks, LLM cache, eval harness, API server integration, GraphJSON multi-run comparison.
  - Optional MCP Track: MCP server/client deployment patterns; health, retries, observability.

- Module 8 — Capstone Projects (3 lessons, ~5–6 hours)
  - Objectives: Build a production app: RAG assistant or multi-agent workflow with tools and monitoring.

## First 10 Lessons (Detailed)

1) Hello Chain: Prompt → LLM → Output
- Objective: Run your first LangChain chain and visualize it.
- Concepts: PromptTemplate, ChatModel/LLM, simple Runnable.
- Visual: Three nodes: PromptTemplate → ChatModel → Parser/Output.
- Code: Build a small chain that greets a user; emit GraphJSON via tracer.
- Exercise: Modify the prompt to include the current day; compare outputs visually.
- Real-World: Foundation for any LLM flow.
- Prerequisites: Python, repo setup.

2) Output Parsers and Robustness
- Objective: Structure outputs safely.
- Concepts: StrOutputParser vs JSONOutputParser, schema-aware parsing.
- Visual: Prompt → LLM → Parser with error lane.
- Code: Two variants: freeform vs structured outputs; log artifacts.
- Exercise: Convert a list of tasks into JSON; visualize artifacts.
- Real-World: Reliable outputs power downstream steps.

3) RunnableSequence and Composition
- Objective: Compose multiple transforms.
- Concepts: RunnableSequence, input mapping, partials.
- Visual: Input → template → LLM → parser inside a group.
- Code: Build a transformation pipeline; pass structured inputs.
- Exercise: Add post-processing step and visualize.

4) Memory Basics: ConversationBufferMemory
- Objective: Add short-term memory to chat.
- Concepts: ConversationBufferMemory.
- Visual: Memory node feeding context into ChatModel.
- Code: Chat loop with memory; show artifacts.
- Exercise: Reset memory vs continue; see graph differences.

5) RouterChain: Conditional Prompting
- Objective: Route inputs to different prompts/models.
- Concepts: RouterChain; simple intent classifier.
- Visual: Router with branching edges to prompt/LLM subflows.
- Code: Route based on keyword; merge outputs.
- Exercise: Add a third route; instrument timing.

6) Loaders and Splitters: Preparing a Corpus
- Objective: Prepare documents for retrieval.
- Concepts: DocumentLoader, RecursiveCharacterTextSplitter.
- Visual: Loader → Splitter → chunk stats artifacts.
- Code: Load a folder; split; serialize artifacts.
- Exercise: Adjust chunk size/overlap; compare distributions.

7) Embeddings + Vector Store (Chroma/FAISS)
- Objective: Build an index.
- Concepts: Embeddings; Chroma/FAISS VectorStore.
- Visual: Embeddings → VectorStore; index metrics.
- Code: Create index; persist; inspect metadata.
- Exercise: Swap embeddings model; compare quality.

8) Retriever → Prompt → LLM (RAG Mini)
- Objective: Close the loop with retrieval.
- Concepts: VectorStoreRetriever; context injection.
- Visual: Retriever → Prompt (context slot) → ChatModel → Parser.
- Code: Answer with citations; store doc artifacts and scores.
- Exercise: Add top_k slider; visualize effect on docs.

9) Tools 101: Calculator and a Simple API Tool
- Objective: Use tools in a controlled chain (no agent yet).
- Concepts: StructuredTool, safe tool I/O.
- Visual: Tool invocation edges and tool I/O artifacts.
- Code: Wire a calculator tool; call it when a flag is set.
- Exercise: Add a weather mock API tool; log tool input/output.

10) ReAct Agent with Tools
- Objective: Reason-act loop with tools and observations.
- Concepts: ReAct Agent, tool selection, observation feedback.
- Visual: Agent node connected to tools, observation edges.
- Code: Agent that picks calculator or weather; emit stepwise events.
- Exercise: Add rate limit and retry; visualize retries.

## Progression and Capstone

Milestones:
- A: Conversational assistant with memory and structured outputs (after L4).
- B: RAG mini with citations and persisted index (after L8).
- C: Agent with tools and observable reasoning (after L10).

Capstones:
1) Domain RAG Assistant: end-to-end pipeline with citations, cache, evals, and cost telemetry.
2) Multi-Agent Researcher: planner → tools → critic → finalizer with guardrails and retries.

## Practical Guidance

- Prereqs: M1 Python basics; M2 JSON & composition; M3 vector concepts; M4 API/tooling; M5 async/errors; M6 IR basics; M7 deployment & testing.
- Pitfalls: Prompt brittleness, context stuffing, tool misuse, hidden costs, flaky chains.
- Extensions: Local models (Ollama), rerankers, multimodal prompts, streaming to viewer.
- Assessment: Per-lesson tasks; milestone rubrics; capstone scored on correctness, reliability, observability.

## Appendix: Prompt for LLM Content Generation

"""
You are assisting in authoring a visual-first LangChain course. Use the repo’s structure (lessons/, api/, viz/, viewer/) and GraphJSON v1.1 conventions. For the requested lesson, generate:
- A concise concept brief (what/why)
- Step-by-step code with comments that runs without external keys by default
- GraphJSON-emitting tracer hooks and sample artifacts
- A viewer-ready node/edge map (types: promptTemplate, chatModel, parser, retriever, vectorStore, tool, agent, memory)
- A practical exercise with success criteria
- Optional extension for advanced students
Return: code blocks, file paths, and a short test command.
"""
