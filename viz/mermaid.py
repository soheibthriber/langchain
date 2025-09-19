from typing import Dict


def to_mermaid(graph: Dict) -> str:
    """Convert GraphJSON to Mermaid flowchart (LR).

    Example output:
        flowchart LR
          prompt[PromptTemplate]
          llm[ChatOpenAI]
          prompt --> llm
    """
    lines = ["flowchart LR"]
    for n in graph.get("nodes", []):
        label = n.get("label", n.get("id", "node"))
        lines.append(f"  {n['id']}[{label}]")
    for e in graph.get("edges", []):
        lines.append(f"  {e['source']} --> {e['target']}")
    return "\n".join(lines)
