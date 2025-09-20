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
    
    # Add nodes
    for n in graph.get("nodes", []):
        label = n.get("label", n.get("id", "node"))
        lines.append(f"  {n['id']}[{label}]")
    
    # Add edges, handling both simple strings and structured objects
    for e in graph.get("edges", []):
        source = e.get("source", "")
        target = e.get("target", "")
        
        # Handle structured source/target objects
        if isinstance(source, dict):
            source = source.get("nodeId", "unknown")
        if isinstance(target, dict):
            target = target.get("nodeId", "unknown")
            
        # Add edge label if present
        label = e.get("label", "")
        if label:
            lines.append(f"  {source} -->|{label}| {target}")
        else:
            lines.append(f"  {source} --> {target}")
    
    return "\n".join(lines)
