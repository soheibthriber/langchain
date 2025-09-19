from time import perf_counter
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime


class GraphTracer:
    """
    GraphJSON v1.1 tracer for LangChain flows with events, artifacts, and groups.
    Usage:
        tracer = GraphTracer(lesson_id="01_hello_chain")
        tracer.node("prompt", "PromptTemplate", "prompt", {"template": "..."})
        tracer.edge("prompt", "llm")
        tracer.begin()
        # ... run your chain ...
        latency_ms = tracer.end()
        graph = tracer.export(latency_ms)
    """

    def __init__(self, lesson_id: str = "unknown") -> None:
        self.lesson_id = lesson_id
        self.run_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat() + "Z"
        
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self.ports: List[Dict[str, Any]] = []
        self.groups: List[Dict[str, Any]] = []
        self.events: List[Dict[str, Any]] = []
        self.artifacts: Dict[str, Dict[str, Any]] = {}
        
        self._ids: set[str] = set()
        self._start: Optional[float] = None
        self.tokens_in: int = 0
        self.tokens_out: int = 0
        self.errors: List[Dict[str, Any]] = []

    def node(self, id: str, label: str, type_: str, data: Optional[Dict[str, Any]] = None, 
             sub_type: Optional[str] = None, tags: Optional[List[str]] = None) -> None:
        if id in self._ids:
            return
        self._ids.add(id)
        self.nodes.append({
            "id": id,
            "label": label,
            "type": type_,
            "subType": sub_type,
            "tags": tags or [],
            "data": data or {}
        })

    def edge(self, src: str, dst: str, label: Optional[str] = None, 
             src_port: Optional[str] = None, dst_port: Optional[str] = None) -> None:
        edge_id = f"{src}->{dst}"
        if src_port:
            edge_id = f"{src}:{src_port}->{dst}"
        if dst_port:
            edge_id = f"{edge_id}:{dst_port}"
            
        self.edges.append({
            "id": edge_id,
            "source": {"nodeId": src, "portId": src_port} if src_port else {"nodeId": src},
            "target": {"nodeId": dst, "portId": dst_port} if dst_port else {"nodeId": dst},
            "label": label
        })

    def port(self, node_id: str, port_id: str, direction: str, label: str) -> None:
        """Add a named port to a node (direction: 'in' or 'out')"""
        self.ports.append({
            "nodeId": node_id,
            "portId": port_id,
            "direction": direction,
            "label": label
        })

    def group(self, id: str, label: str, node_ids: List[str], type_: str, collapsed: bool = False) -> None:
        """Create a collapsible group of nodes"""
        self.groups.append({
            "id": id,
            "label": label,
            "nodeIds": node_ids,
            "type": type_,
            "collapsed": collapsed
        })

    def event(self, kind: str, node_id: Optional[str] = None, edge_id: Optional[str] = None, 
              payload: Optional[Dict[str, Any]] = None) -> None:
        """Record an event with timestamp"""
        if self._start is None:
            ts_ms = 0
        else:
            ts_ms = int((perf_counter() - self._start) * 1000)
            
        self.events.append({
            "ts_ms": ts_ms,
            "kind": kind,
            "nodeId": node_id,
            "edgeId": edge_id,
            "payload": payload or {}
        })

    def artifact(self, node_id: str, **kwargs: Any) -> None:
        """Store artifacts for a node (prompt, resolved_prompt, output, tool_io, docs)"""
        if node_id not in self.artifacts:
            self.artifacts[node_id] = {}
        self.artifacts[node_id].update(kwargs)

    def error(self, node_id: str, message: str) -> None:
        """Record an error for a node"""
        if self._start is None:
            at_ms = 0
        else:
            at_ms = int((perf_counter() - self._start) * 1000)
            
        self.errors.append({
            "nodeId": node_id,
            "message": message,
            "at_ms": at_ms
        })

    def begin(self) -> None:
        self._start = perf_counter()

    def end(self) -> float:
        if self._start is None:
            return 0.0
        delta = perf_counter() - self._start
        self._start = None
        return max(delta * 1000.0, 0.0)

    def export(self, latency_ms: float) -> Dict[str, Any]:
        return {
            "metadata": {
                "version": "1.1",
                "run_id": self.run_id,
                "created_at": self.created_at,
                "lesson_id": self.lesson_id,
                "tags": []
            },
            "nodes": self.nodes,
            "ports": self.ports,
            "edges": self.edges,
            "groups": self.groups,
            "run": {
                "latency_ms": int(latency_ms),
                "tokens_in": self.tokens_in,
                "tokens_out": self.tokens_out,
                "cost": None,
                "errors": self.errors if self.errors else None
            },
            "events": self.events,
            "artifacts": self.artifacts,
            "styles": {}  # Theme tokens will be added later
        }
