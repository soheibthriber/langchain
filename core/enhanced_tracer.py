"""
Enhanced GraphJSON Tracer with Node Registry Integration
=======================================================

This module provides advanced tracing capabilities using the node registry
for rich metadata, configuration tracking, and extensible visualization.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import asdict

from .node_registry import node_registry, NodeCategory


class EnhancedGraphTracer:
    """Advanced tracer with node registry integration and rich metadata capture"""
    
    def __init__(self, lesson_id: str, output_dir: str = "./lessons"):
        self.lesson_id = lesson_id
        self.output_dir = Path(output_dir)
        self.run_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat() + "Z"
        
        # Ensure node definitions are loaded
        self._ensure_registry_loaded()
        
        # Tracking structures
        self.nodes = []
        self.edges = []
        self.events = []
        self.artifacts = {}
        self.token_usage = {}
        self.configuration_snapshot = {}
        self.metrics = {
            "node_count": 0, 
            "total_latency_ms": 0.0,
            "token_usage": {}
        }
        self.execution_trace = []
        self.performance_data = {}
        
        # Performance tracking
        self.start_time = None
        self.total_latency = 0.0
        
    def _ensure_registry_loaded(self):
        """Ensure node registry has all definitions loaded"""
        try:
            from .registry_loader import load_all_node_definitions
            load_all_node_definitions()
        except Exception as e:
            print(f"Warning: Could not load extended node definitions: {e}")
            pass
    
    def trace_component(
        self, 
        component_id: str, 
        instance: Any, 
        label: Optional[str] = None,
        custom_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Trace a LangChain component with rich metadata from registry"""
        
        # Get enhanced node data from registry
        node_data = node_registry.create_node_data(instance, component_id)
        
        # Override label if provided
        if label:
            node_data["label"] = label
        else:
            node_data["label"] = node_data.get("display_name", component_id)
        
        # Add custom data
        if custom_data:
            node_data.update(custom_data)
        
        # Enhanced metadata
        node_data.update({
            "traced_at": datetime.utcnow().isoformat() + "Z",
            "execution_order": len(self.nodes) + 1,
            "run_id": self.run_id
        })
        
        # Store component reference for later analysis
        self.configuration_snapshot[component_id] = {
            "class_name": instance.__class__.__name__,
            "module": instance.__class__.__module__,
            "instance_config": node_data.get("configuration", {})
        }
        
        self.nodes.append(node_data)
        self.metrics["node_count"] += 1
        
        return node_data
    
    def trace_execution(
        self, 
        node_id: str, 
        input_data: Any, 
        output_data: Any,
        execution_time_ms: float = 0,
        metadata: Optional[Dict] = None
    ) -> None:
        """Trace the execution of a node with input/output capture"""
        
        execution_event = {
            "event_id": str(uuid.uuid4()),
            "node_id": node_id,
            "event_type": "execution",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "execution_time_ms": execution_time_ms,
            "input_preview": self._serialize_safely(input_data, max_length=500),
            "output_preview": self._serialize_safely(output_data, max_length=500),
            "metadata": metadata or {}
        }
        
        self.events.append(execution_event)
        self.execution_trace.append({
            "node_id": node_id,
            "order": len(self.execution_trace) + 1,
            "timestamp": execution_event["timestamp"],
            "duration_ms": execution_time_ms
        })
        
        # Update performance metrics
        self.metrics["total_latency_ms"] += execution_time_ms
        self.performance_data[node_id] = {
            "execution_time_ms": execution_time_ms,
            "input_size": len(str(input_data)) if input_data else 0,
            "output_size": len(str(output_data)) if output_data else 0
        }
    
    def add_artifact(
        self, 
        artifact_key: str, 
        content: Any, 
        artifact_type: str = "data",
        description: Optional[str] = None
    ) -> None:
        """Store rich artifacts with metadata"""
        
        artifact = {
            "type": artifact_type,
            "content": content,
            "description": description or f"{artifact_type.title()} artifact",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "size_bytes": len(str(content)) if content else 0,
            "content_preview": self._serialize_safely(content, max_length=200)
        }
        
        self.artifacts[artifact_key] = artifact
    
    def connect_nodes(
        self, 
        source_id: str, 
        target_id: str, 
        edge_type: str = "flow",
        data_flow: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        """Create enhanced edges with data flow information"""
        
        edge = {
            "id": f"{source_id}_{target_id}",
            "source": source_id,
            "target": target_id,
            "type": edge_type,
            "label": edge_type.replace("_", " ").title(),
            "data": {
                "flow_type": edge_type,
                "data_flow": data_flow or {},
                "metadata": metadata or {},
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        self.edges.append(edge)
    
    def add_cost_tracking(self, node_id: str, cost_data: Dict[str, Any]) -> None:
        """Track cost information for LLM calls"""
        self.metrics["cost_estimates"][node_id] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **cost_data
        }
    
    def add_token_usage(self, node_id: str, token_data: Dict[str, int]) -> None:
        """Track token usage for LLM calls"""
        self.metrics["token_usage"][node_id] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **token_data
        }
    
    def export_graph(self, format_type: str = "json") -> Dict[str, Any]:
        """Export complete graph with enhanced metadata"""
        
        graph_data = {
            "metadata": {
                "version": "1.2",  # Enhanced version
                "run_id": self.run_id,
                "created_at": self.created_at,
                "lesson_id": self.lesson_id,
                "node_registry_version": "1.0",
                "tags": [],
                "execution_summary": {
                    "total_nodes": len(self.nodes),
                    "total_edges": len(self.edges),
                    "total_events": len(self.events),
                    "total_artifacts": len(self.artifacts),
                    "execution_time_ms": self.metrics["total_latency_ms"]
                }
            },
            "nodes": self.nodes,
            "edges": self.edges,
            "events": self.events,
            "artifacts": self.artifacts,
            "metrics": self.metrics,
            "execution_trace": self.execution_trace,
            "configuration_snapshot": self.configuration_snapshot
        }
        
        return graph_data
    
    def save_graph(self, filename: Optional[str] = None) -> Path:
        """Save graph to JSON file with enhanced data"""
        
        if not filename:
            lesson_dir = self.output_dir / self.lesson_id
            filename = lesson_dir / "graph.json"
        else:
            filename = Path(filename)
        
        # Ensure directory exists
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        graph_data = self.export_graph()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def generate_node_summary(self) -> Dict[str, Any]:
        """Generate summary of nodes by category and complexity"""
        
        summary = {
            "by_category": {},
            "by_complexity": {},
            "by_type": {},
            "execution_order": [
                {"node_id": trace["node_id"], "order": trace["order"]} 
                for trace in self.execution_trace
            ]
        }
        
        for node in self.nodes:
            category = node.get("category", "unknown")
            complexity = node.get("complexity", "unknown")
            node_type = node.get("type", "unknown")
            
            # Count by category
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1
            
            # Count by complexity
            summary["by_complexity"][complexity] = summary["by_complexity"].get(complexity, 0) + 1
            
            # Count by type
            summary["by_type"][node_type] = summary["by_type"].get(node_type, 0) + 1
        
        return summary
    
    def _serialize_safely(self, data: Any, max_length: int = 1000) -> str:
        """Safely serialize data for storage with length limits"""
        try:
            if data is None:
                return ""
            
            if isinstance(data, str):
                result = data
            elif isinstance(data, (dict, list)):
                result = json.dumps(data, ensure_ascii=False)
            else:
                result = str(data)
            
            # Truncate if too long
            if len(result) > max_length:
                result = result[:max_length] + "... [truncated]"
            
            return result
            
        except Exception as e:
            return f"[Serialization error: {str(e)}]"


def create_enhanced_tracer(lesson_id: str, output_dir: str = "./lessons") -> EnhancedGraphTracer:
    """Factory function to create enhanced tracer instances"""
    return EnhancedGraphTracer(lesson_id, output_dir)
