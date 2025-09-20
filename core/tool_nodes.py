"""
Extended Node Definitions - Tools & Function Calling
===================================================

This module extends the node registry with comprehensive tool definitions
for building agent-based LangChain workflows.
"""

def register_tool_nodes():
    """Register all tool-related node definitions"""
    
    # Import here to avoid circular imports
    from .node_registry import (
        NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, 
        NodeDefinition, node_registry
    )
    
    # Base Tool
    node_registry.register(NodeDefinition(
        node_type="BaseTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.BASIC,
            display_name="Base Tool",
            description="Foundation class for creating custom tools",
            icon="🔨",
            color="#F59E0B",
            examples=[
                "Custom function wrapper",
                "API integration tool",
                "Data processing tool"
            ],
            common_patterns=[
                "Single function tools",
                "Stateful tools with memory",
                "Async tool execution"
            ],
            troubleshooting={
                "tool_not_called": "Check tool description clarity",
                "wrong_parameters": "Validate tool schema definition",
                "execution_error": "Add proper error handling"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["name", "description", "func"],
            optional_params={
                "return_direct": False,
                "verbose": False,
                "args_schema": None,
                "coroutine": None
            },
            validation_rules={
                "name": {"type": "string", "max_length": 50},
                "description": {"type": "string", "min_length": 10}
            },
            performance_hints=[
                "Keep tool descriptions concise but specific",
                "Use clear parameter names",
                "Handle errors gracefully"
            ]
        )
    ))
    
    # DuckDuckGo Search Tool
    node_registry.register(NodeDefinition(
        node_type="DuckDuckGoSearchRun",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.BASIC,
            display_name="DuckDuckGo Search",
            description="Search the web using DuckDuckGo search engine",
            icon="🔍",
            color="#F59E0B",
            examples=[
                "Current events lookup",
                "Fact checking",
                "Research assistance"
            ],
            common_patterns=[
                "Question answering with search",
                "Multi-step research",
                "Fact verification"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={
                "max_results": 5,
                "region": "wt-wt",
                "time": "y",
                "safesearch": "moderate"
            },
            performance_hints=[
                "Limit results to avoid token overuse",
                "Use specific search queries",
                "Cache results for repeated queries"
            ],
            cost_implications="Free but rate limited"
        )
    ))
    
    # Python REPL Tool
    node_registry.register(NodeDefinition(
        node_type="PythonREPLTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Python REPL",
            description="Execute Python code in a sandboxed environment",
            icon="🐍",
            color="#F59E0B",
            examples=[
                "Mathematical calculations",
                "Data analysis",
                "Code generation and testing"
            ],
            common_patterns=[
                "Multi-step calculations",
                "Data processing pipelines",
                "Visualization generation"
            ],
            troubleshooting={
                "import_error": "Check available packages",
                "syntax_error": "Validate code before execution",
                "security_risk": "Code runs in sandboxed environment"
            }
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={
                "globals": {},
                "locals": {},
                "sanitize_input": True,
                "timeout": 30
            },
            validation_rules={
                "timeout": {"type": "integer", "min": 1, "max": 300}
            },
            performance_hints=[
                "Set reasonable timeout values",
                "Sanitize user inputs",
                "Monitor memory usage"
            ]
        )
    ))
    
    # Calculator Tool
    node_registry.register(NodeDefinition(
        node_type="CalculatorTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.BASIC,
            display_name="Calculator",
            description="Perform mathematical calculations safely",
            icon="🧮",
            color="#F59E0B",
            examples=[
                "Basic arithmetic",
                "Complex expressions",
                "Unit conversions"
            ],
            common_patterns=[
                "Financial calculations",
                "Engineering computations",
                "Statistical analysis"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={
                "precision": 10,
                "allow_functions": ["sin", "cos", "tan", "log", "sqrt"]
            },
            performance_hints=[
                "Use for mathematical operations only",
                "Validate expressions before calculation",
                "Consider precision requirements"
            ]
        )
    ))
    
    # File System Tool
    node_registry.register(NodeDefinition(
        node_type="FileSystemTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="File System",
            description="Read and write files safely",
            icon="📁",
            color="#F59E0B",
            examples=[
                "Document processing",
                "Configuration file handling",
                "Data file operations"
            ],
            common_patterns=[
                "Document analysis workflows",
                "Configuration management",
                "Data pipeline operations"
            ],
            troubleshooting={
                "permission_denied": "Check file permissions",
                "file_not_found": "Verify file path exists",
                "encoding_error": "Specify correct file encoding"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["root_dir"],
            optional_params={
                "allowed_extensions": [".txt", ".md", ".json", ".csv"],
                "max_file_size": 10485760,  # 10MB
                "encoding": "utf-8"
            },
            validation_rules={
                "root_dir": {"type": "string", "must_exist": True},
                "max_file_size": {"type": "integer", "min": 1024}
            },
            performance_hints=[
                "Restrict file access to safe directories",
                "Limit file sizes to prevent memory issues",
                "Validate file types before processing"
            ]
        )
    ))
    
    # API Request Tool
    node_registry.register(NodeDefinition(
        node_type="APIRequestTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.ADVANCED,
            display_name="API Request",
            description="Make HTTP requests to external APIs",
            icon="🌐",
            color="#F59E0B",
            examples=[
                "REST API integration",
                "Data fetching from services",
                "Webhook handling"
            ],
            common_patterns=[
                "Multi-API data aggregation",
                "Service integration workflows",
                "Real-time data retrieval"
            ],
            troubleshooting={
                "connection_timeout": "Check network and endpoint",
                "auth_failed": "Verify API credentials",
                "rate_limited": "Implement backoff strategy"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["base_url"],
            optional_params={
                "headers": {},
                "auth": None,
                "timeout": 30,
                "max_retries": 3,
                "allowed_methods": ["GET", "POST", "PUT", "DELETE"]
            },
            validation_rules={
                "base_url": {"type": "string", "format": "url"},
                "timeout": {"type": "integer", "min": 1, "max": 300}
            },
            performance_hints=[
                "Use connection pooling for multiple requests",
                "Implement proper error handling",
                "Cache responses when appropriate"
            ],
            cost_implications="Depends on API provider pricing"
        )
    ))


def register_agent_nodes():
    """Register agent-related node definitions"""
    
    # Import here to avoid circular imports
    from .node_registry import (
        NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, 
        NodeDefinition, node_registry
    )
    
    # Tool Router/Selector
    node_registry.register(NodeDefinition(
        node_type="ToolRouter",
        metadata=NodeMetadata(
            category=NodeCategory.UTILITY,
            complexity=NodeComplexity.ADVANCED,
            display_name="Tool Router",
            description="Routes queries to appropriate tools based on content",
            icon="🔀",
            color="#6366F1",
            examples=[
                "Multi-tool agent systems",
                "Conditional tool selection",
                "Tool orchestration"
            ],
            common_patterns=[
                "Agent with specialized tools",
                "Workflow branching",
                "Dynamic tool selection"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["tools", "routing_strategy"],
            optional_params={
                "fallback_tool": None,
                "max_iterations": 10,
                "confidence_threshold": 0.7
            },
            performance_hints=[
                "Define clear tool descriptions",
                "Implement fallback strategies",
                "Monitor routing accuracy"
            ]
        )
    ))
    
    # Function Calling Assistant
    node_registry.register(NodeDefinition(
        node_type="FunctionCallingAgent",
        metadata=NodeMetadata(
            category=NodeCategory.CHAIN,
            complexity=NodeComplexity.EXPERT,
            display_name="Function Calling Agent",
            description="Advanced agent that uses OpenAI function calling",
            icon="🤖",
            color="#8B5CF6",
            examples=[
                "Multi-step reasoning with tools",
                "Complex problem solving",
                "Autonomous task execution"
            ],
            common_patterns=[
                "Research and analysis workflows",
                "Data processing pipelines",
                "Interactive assistants"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["llm", "tools"],
            optional_params={
                "system_message": "You are a helpful assistant with access to tools.",
                "max_iterations": 20,
                "return_intermediate_steps": True,
                "early_stopping_method": "generate"
            },
            performance_hints=[
                "Use models that support function calling",
                "Design tools with clear schemas",
                "Monitor token usage in complex workflows"
            ],
            cost_implications="High token usage for complex reasoning"
        )
    ))


# Auto-register all tool nodes when module is imported
if __name__ != "__main__":
    register_tool_nodes()
    register_agent_nodes()


# Export for convenience
__all__ = [
    "register_tool_nodes",
    "register_agent_nodes"
]
