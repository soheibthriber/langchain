"""
Registry Loader - Centralized Node Registration
===============================================

This module handles loading all extended node definitions into the registry
without circular import issues.
"""


def load_all_node_definitions():
    """Load all extended node definitions into the global registry"""
    
    from .node_registry import (
        NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, 
        NodeDefinition, node_registry
    )
    
    # Tools
    register_tools(node_registry, NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, NodeDefinition)
    
    # LLMs  
    register_llms(node_registry, NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, NodeDefinition)
    
    # Retrievers & Memory
    register_retrievers_memory(node_registry, NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, NodeDefinition)
    
    print(f"✅ Loaded {len(node_registry._definitions)} total node definitions")
    return node_registry


def register_tools(registry, NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, NodeDefinition):
    """Register tool node definitions"""
    
    # DuckDuckGo Search Tool
    registry.register(NodeDefinition(
        node_type="DuckDuckGoSearchRun",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.BASIC,
            display_name="DuckDuckGo Search",
            description="Search the web using DuckDuckGo search engine",
            icon="🔍",
            color="#F59E0B",
            examples=["Current events lookup", "Fact checking", "Research assistance"]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={"max_results": 5, "region": "wt-wt"},
            performance_hints=["Limit results to avoid token overuse", "Use specific search queries"],
            cost_implications="Free but rate limited"
        )
    ))
    
    # Python REPL Tool
    registry.register(NodeDefinition(
        node_type="PythonREPLTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Python REPL",
            description="Execute Python code in a sandboxed environment",
            icon="🐍",
            color="#F59E0B",
            examples=["Mathematical calculations", "Data analysis", "Code generation"]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={"timeout": 30, "sanitize_input": True},
            performance_hints=["Set reasonable timeout values", "Sanitize user inputs"]
        )
    ))
    
    # Calculator Tool
    registry.register(NodeDefinition(
        node_type="CalculatorTool",
        metadata=NodeMetadata(
            category=NodeCategory.TOOL,
            complexity=NodeComplexity.BASIC,
            display_name="Calculator",
            description="Perform mathematical calculations safely",
            icon="🧮",
            color="#F59E0B"
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={"precision": 10},
            performance_hints=["Use for mathematical operations only", "Validate expressions"]
        )
    ))


def register_llms(registry, NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, NodeDefinition):
    """Register LLM node definitions"""
    
    
    # Claude (Anthropic)
    registry.register(NodeDefinition(
        node_type="ChatAnthropic",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Claude (Anthropic)",
            description="Anthropic's Claude models for advanced reasoning",
            icon="🧠",
            color="#FF6B35",
            examples=["Long-form analysis", "Complex reasoning", "Code review"]
        ),
        configuration=NodeConfiguration(
            required_params=["model"],
            optional_params={"temperature": 0.7, "max_tokens": 4096},
            performance_hints=["claude-3-sonnet for balanced performance", "claude-3-opus for complex reasoning"],
            cost_implications="Premium pricing, varies by model size"
        )
    ))
    
    # Google Gemini
    registry.register(NodeDefinition(
        node_type="ChatGoogleGenerativeAI",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Google Gemini",
            description="Google's multimodal Gemini models",
            icon="💎",
            color="#4285F4",
            examples=["Multimodal analysis", "Code generation", "Mathematical reasoning"]
        ),
        configuration=NodeConfiguration(
            required_params=["model"],
            optional_params={"temperature": 0.7, "max_output_tokens": 2048},
            performance_hints=["gemini-pro for text", "gemini-pro-vision for multimodal"],
            cost_implications="Free tier available, pay-per-token beyond"
        )
    ))
    
    
    # OpenAI Embeddings
    registry.register(NodeDefinition(
        node_type="OpenAIEmbeddings",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.BASIC,
            display_name="OpenAI Embeddings",
            description="High-quality text embeddings from OpenAI",
            icon="🔢",
            color="#74C0FC",
            examples=["Semantic search", "Document similarity", "Clustering"]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={"model": "text-embedding-3-small", "chunk_size": 1000},
            performance_hints=["text-embedding-3-small for cost", "batch embeddings for efficiency"],
            cost_implications="Pay per token, very cost-effective"
        )
    ))


def register_retrievers_memory(registry, NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, NodeDefinition):
    """Register retriever and memory node definitions"""
    
    # Vector Store Retriever
    registry.register(NodeDefinition(
        node_type="VectorStoreRetriever",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Vector Store Retriever",
            description="Retrieve relevant documents from vector databases",
            icon="📊",
            color="#06B6D4",
            examples=["Semantic search", "Knowledge base querying", "RAG context"]
        ),
        configuration=NodeConfiguration(
            required_params=["vectorstore"],
            optional_params={"search_type": "similarity", "search_kwargs": {"k": 4}},
            performance_hints=["Tune k parameter", "Use metadata filtering", "Consider search type"]
        )
    ))
    
    # Chroma Vector Store
    registry.register(NodeDefinition(
        node_type="Chroma",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.BASIC,
            display_name="Chroma Vector Store",
            description="Open-source vector database for embeddings",
            icon="🎨",
            color="#A855F7",
            examples=["Local development", "Document storage", "Prototype RAG"]
        ),
        configuration=NodeConfiguration(
            required_params=["embedding_function"],
            optional_params={"collection_name": "langchain", "persist_directory": None},
            performance_hints=["Use persistent directory", "Configure collection metadata"],
            cost_implications="Free open-source, hosting costs if deployed"
        )
    ))
    
    # Conversation Buffer Memory
    registry.register(NodeDefinition(
        node_type="ConversationBufferMemory",
        metadata=NodeMetadata(
            category=NodeCategory.MEMORY,
            complexity=NodeComplexity.BASIC,
            display_name="Buffer Memory",
            description="Store conversation history in a simple buffer",
            icon="💭",
            color="#10B981",
            examples=["Basic chat memory", "Short conversations", "Simple context"]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={"memory_key": "history", "return_messages": False},
            performance_hints=["Monitor buffer size", "Clear periodically", "Consider summarization"]
        )
    ))
    
    # Conversation Summary Memory
    registry.register(NodeDefinition(
        node_type="ConversationSummaryMemory",
        metadata=NodeMetadata(
            category=NodeCategory.MEMORY,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Summary Memory",
            description="Summarize conversation history to save tokens",
            icon="📝",
            color="#10B981",
            examples=["Long conversations", "Token optimization", "Context summarization"]
        ),
        configuration=NodeConfiguration(
            required_params=["llm"],
            optional_params={"memory_key": "history", "max_token_limit": 2000},
            performance_hints=["Balance frequency vs accuracy", "Monitor quality", "Engineer prompts"],
            cost_implications="Additional LLM calls for summarization"
        )
    ))


# Note: load_all_node_definitions() should be called explicitly when needed
# to avoid circular import issues
