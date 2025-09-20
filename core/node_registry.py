"""
Node Abstraction System for LangChain Visualization
===================================================

This module provides a comprehensive abstraction layer for all LangChain components,
enabling rich visualization metadata, configuration management, and extensible
node type definitions.
"""

from typing import Dict, Any, List, Optional, Type, Union
from dataclasses import dataclass, field
from enum import Enum
import inspect
from abc import ABC, abstractmethod


class NodeCategory(Enum):
    """High-level categories for organizing nodes"""
    INPUT = "input"
    LLM = "llm" 
    PROMPT = "prompt"
    PARSER = "parser"
    TOOL = "tool"
    RETRIEVER = "retriever"
    MEMORY = "memory"
    CHAIN = "chain"
    OUTPUT = "output"
    UTILITY = "utility"


class NodeComplexity(Enum):
    """Complexity levels for learning progression"""
    BASIC = "basic"         # Fundamental building blocks
    INTERMEDIATE = "intermediate"  # Common patterns
    ADVANCED = "advanced"   # Complex workflows
    EXPERT = "expert"       # Custom implementations


@dataclass
class NodeMetadata:
    """Rich metadata for visualization and documentation"""
    category: NodeCategory
    complexity: NodeComplexity
    display_name: str
    description: str
    icon: str = "🔗"
    color: str = "#4F46E5"
    documentation_url: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    common_patterns: List[str] = field(default_factory=list)
    troubleshooting: Dict[str, str] = field(default_factory=dict)


@dataclass
class NodeConfiguration:
    """Configuration schema for node instances"""
    required_params: List[str] = field(default_factory=list)
    optional_params: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    performance_hints: List[str] = field(default_factory=list)
    cost_implications: Optional[str] = None


class NodeDefinition:
    """Complete definition of a visualizable node type"""
    
    def __init__(
        self,
        node_type: str,
        metadata: NodeMetadata,
        configuration: NodeConfiguration,
        langchain_class: Optional[Type] = None,
        custom_tracer: Optional[callable] = None
    ):
        self.node_type = node_type
        self.metadata = metadata
        self.configuration = configuration
        self.langchain_class = langchain_class
        self.custom_tracer = custom_tracer
    
    def create_instance_data(self, instance: Any) -> Dict[str, Any]:
        """Extract visualization data from a LangChain instance"""
        base_data = {
            "type": self.node_type,
            "category": self.metadata.category.value,
            "complexity": self.metadata.complexity.value,
            "description": self.metadata.description,
            "icon": self.metadata.icon,
            "color": self.metadata.color
        }
        
        # Add instance-specific configuration
        if hasattr(instance, '__dict__'):
            instance_config = {}
            for attr_name, attr_value in instance.__dict__.items():
                if not attr_name.startswith('_'):
                    # Serialize safely
                    if isinstance(attr_value, (str, int, float, bool, list, dict)):
                        instance_config[attr_name] = attr_value
                    elif hasattr(attr_value, '__name__'):
                        instance_config[attr_name] = attr_value.__name__
                    else:
                        instance_config[attr_name] = str(attr_value)
            
            base_data["configuration"] = instance_config
        
        return base_data


class NodeRegistry:
    """Central registry for all node types and their visualization configurations"""
    
    def __init__(self):
        self._definitions: Dict[str, NodeDefinition] = {}
        self._category_index: Dict[NodeCategory, List[str]] = {cat: [] for cat in NodeCategory}
        self._complexity_index: Dict[NodeComplexity, List[str]] = {comp: [] for comp in NodeComplexity}
        
        # Initialize with built-in definitions
        self._register_builtin_definitions()
    
    def register(self, definition: NodeDefinition) -> None:
        """Register a new node definition"""
        self._definitions[definition.node_type] = definition
        self._category_index[definition.metadata.category].append(definition.node_type)
        self._complexity_index[definition.metadata.complexity].append(definition.node_type)
    
    def get_definition(self, node_type: str) -> Optional[NodeDefinition]:
        """Get definition for a specific node type"""
        return self._definitions.get(node_type)
    
    def get_by_category(self, category: NodeCategory) -> List[NodeDefinition]:
        """Get all definitions in a category"""
        return [self._definitions[nt] for nt in self._category_index[category]]
    
    def get_by_complexity(self, complexity: NodeComplexity) -> List[NodeDefinition]:
        """Get all definitions of a complexity level"""
        return [self._definitions[nt] for nt in self._complexity_index[complexity]]
    
    def detect_node_type(self, instance: Any) -> Optional[str]:
        """Auto-detect node type from LangChain instance"""
        class_name = instance.__class__.__name__
        module_name = instance.__class__.__module__
        
        # Try exact class name match first
        if class_name in self._definitions:
            return class_name
        
        # Try pattern matching for common LangChain patterns
        for node_type, definition in self._definitions.items():
            if definition.langchain_class and isinstance(instance, definition.langchain_class):
                return node_type
            
            # Fallback pattern matching
            if node_type.lower() in class_name.lower():
                return node_type
        
        return None
    
    def create_node_data(self, instance: Any, node_id: str) -> Dict[str, Any]:
        """Create complete node data for visualization"""
        node_type = self.detect_node_type(instance)
        
        if not node_type:
            # Fallback for unknown types
            return {
                "id": node_id,
                "type": "unknown",
                "category": "utility",
                "description": f"Unknown component: {instance.__class__.__name__}",
                "icon": "❓",
                "color": "#6B7280"
            }
        
        definition = self._definitions[node_type]
        node_data = definition.create_instance_data(instance)
        node_data["id"] = node_id
        
        return node_data
    
    def _register_builtin_definitions(self):
        """Register built-in LangChain component definitions"""
        
        # Prompt Templates
        self.register(NodeDefinition(
            node_type="PromptTemplate",
            metadata=NodeMetadata(
                category=NodeCategory.PROMPT,
                complexity=NodeComplexity.BASIC,
                display_name="Prompt Template",
                description="Formats input variables into structured prompts for LLMs",
                icon="📝",
                color="#10B981",
                examples=[
                    "Simple text formatting",
                    "Multi-variable templates", 
                    "Conditional prompting"
                ],
                common_patterns=[
                    "Few-shot examples",
                    "System + user messages",
                    "Chain-of-thought prompting"
                ]
            ),
            configuration=NodeConfiguration(
                required_params=["template"],
                optional_params={
                    "input_variables": [],
                    "template_format": "f-string",
                    "validate_template": True
                },
                performance_hints=[
                    "Keep templates concise",
                    "Use clear variable names",
                    "Test with various inputs"
                ]
            )
        ))
        
        # Chat Models
        self.register(NodeDefinition(
            node_type="ChatOpenAI",
            metadata=NodeMetadata(
                category=NodeCategory.LLM,
                complexity=NodeComplexity.BASIC,
                display_name="OpenAI Chat Model",
                description="OpenAI's GPT models for conversational AI",
                icon="🤖",
                color="#FF6B35",
                documentation_url="https://docs.langchain.com/docs/modules/models/llms/integrations/openai",
                common_patterns=[
                    "Single completion",
                    "Conversation chains",
                    "Function calling"
                ]
            ),
            configuration=NodeConfiguration(
                required_params=["model"],
                optional_params={
                    "temperature": 0.7,
                    "max_tokens": None,
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0
                },
                cost_implications="Pay per token (input + output)",
                performance_hints=[
                    "Lower temperature for consistent outputs",
                    "Set max_tokens to control response length",
                    "Use system messages for behavior control"
                ]
            )
        ))
        
        # Output Parsers
        self.register(NodeDefinition(
            node_type="StrOutputParser",
            metadata=NodeMetadata(
                category=NodeCategory.PARSER,
                complexity=NodeComplexity.BASIC,
                display_name="String Output Parser",
                description="Extracts string content from LLM responses",
                icon="🔧",
                color="#8B5CF6"
            ),
            configuration=NodeConfiguration(
                required_params=[],
                optional_params={},
                performance_hints=["Use for simple text extraction"]
            )
        ))
        
        # Add more advanced parsers
        self.register(NodeDefinition(
            node_type="PydanticOutputParser",
            metadata=NodeMetadata(
                category=NodeCategory.PARSER,
                complexity=NodeComplexity.INTERMEDIATE,
                display_name="Pydantic Output Parser",
                description="Parses LLM output into structured Pydantic models",
                icon="🏗️",
                color="#8B5CF6",
                examples=[
                    "JSON object extraction",
                    "Data validation",
                    "Type-safe parsing"
                ]
            ),
            configuration=NodeConfiguration(
                required_params=["pydantic_object"],
                performance_hints=[
                    "Define clear schema",
                    "Handle parsing errors",
                    "Validate output format"
                ]
            )
        ))
        
        # Import extended node definitions
        try:
            from .registry_loader import load_all_node_definitions
            # Don't call here to avoid double-loading, will be called when module imports registry_loader
            
        except ImportError as e:
            # Graceful fallback if extended modules aren't available
            print(f"Warning: Could not import extended node definitions: {e}")
            pass


# Global registry instance
node_registry = NodeRegistry()


def register_custom_node(
    node_type: str,
    category: NodeCategory,
    complexity: NodeComplexity,
    display_name: str,
    description: str,
    **kwargs
) -> None:
    """Convenient function to register custom node types"""
    metadata = NodeMetadata(
        category=category,
        complexity=complexity,
        display_name=display_name,
        description=description,
        **{k: v for k, v in kwargs.items() if k in NodeMetadata.__dataclass_fields__}
    )
    
    config = NodeConfiguration(
        **{k: v for k, v in kwargs.items() if k in NodeConfiguration.__dataclass_fields__}
    )
    
    definition = NodeDefinition(node_type, metadata, config)
    node_registry.register(definition)
