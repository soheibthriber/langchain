# Core Subsystem (Tracer & Registry) Requirements

## Purpose
Provide a minimal, lesson-friendly way to capture execution data as GraphJSON and optional visual metadata for the viewer.

## Tracer Requirements
- API to:
  - register nodes with id/label/type/category/icon/color/data
  - connect edges (source → target with label?)
  - begin/end timing; log invoke_start/invoke_end events with input/output previews
  - attach artifacts per node: prompt (template/input_vars/resolved), llm (input/output/model_info), parser (input/output/type)
  - export GraphJSON v1.1 (metadata/nodes/edges/events/artifacts/run)
- Keep simple and framework-agnostic; no heavy deps.

## Registry (optional)
- Provide defaults for icon/color/category by type (promptTemplate, llm, parser, …).
- Never override runtime content; artifacts and events are primary.

## Adapters / Future
- LangGraph adapter emitting state/conditional edges.
- MCP adapter capturing tool catalogs, calls, and responses as events/artifacts.
- Validation utilities for GraphJSON schema.

## Quality Gates
- GraphJSON exports validate (basic checks for required fields).
- Viewer can render runtime content using artifacts and events without extra transforms.
