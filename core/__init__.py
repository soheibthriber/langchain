"""
Core Module for Enhanced LangChain Visualization
===============================================

This module provides comprehensive abstractions for tracing, visualizing,
and analyzing LangChain workflows with rich metadata and configuration
management.

Components:
- node_registry: Central registry for node types and metadata
- enhanced_tracer: Advanced tracing with performance and cost tracking
- graph_tracer: Backward compatibility with existing GraphJSON format
"""

from .node_registry import (
    NodeCategory,
    NodeComplexity, 
    NodeMetadata,
    NodeConfiguration,
    NodeDefinition,
    NodeRegistry,
    node_registry,
    register_custom_node
)

from .enhanced_tracer import (
    EnhancedGraphTracer,
    create_enhanced_tracer
)

__version__ = "2.0.0"
__author__ = "LangChain Course Team"

__all__ = [
    # Node Registry
    "NodeCategory",
    "NodeComplexity",
    "NodeMetadata", 
    "NodeConfiguration",
    "NodeDefinition",
    "NodeRegistry",
    "node_registry",
    "register_custom_node",
    
    # Enhanced Tracer
    "EnhancedGraphTracer", 
    "create_enhanced_tracer"
]
