"""
Extended Node Definitions - Retrievers & Memory
===============================================

This module extends the node registry with retrieval and memory
system definitions for RAG and conversational AI workflows.
"""

from core.node_registry import (
    NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, 
    NodeDefinition, node_registry
)


def register_retriever_nodes():
    """Register all retriever node definitions"""
    
    # Vector Store Retriever
    node_registry.register(NodeDefinition(
        node_type="VectorStoreRetriever",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Vector Store Retriever",
            description="Retrieve relevant documents from vector databases",
            icon="📊",
            color="#06B6D4",
            examples=[
                "Semantic document search",
                "Knowledge base querying",
                "Context retrieval for RAG"
            ],
            common_patterns=[
                "RAG question answering",
                "Document-based chat",
                "Knowledge retrieval systems"
            ],
            troubleshooting={
                "no_results": "Check embedding model compatibility",
                "irrelevant_results": "Adjust similarity threshold",
                "slow_retrieval": "Optimize vector store indexing"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["vectorstore"],
            optional_params={
                "search_type": "similarity",
                "search_kwargs": {"k": 4},
                "tags": [],
                "metadata": {}
            },
            validation_rules={
                "search_kwargs.k": {"type": "integer", "min": 1, "max": 100}
            },
            performance_hints=[
                "Tune k parameter for relevance vs coverage",
                "Use metadata filtering for targeted search",
                "Consider search_type based on use case"
            ]
        )
    ))
    
    # Multi-Query Retriever
    node_registry.register(NodeDefinition(
        node_type="MultiQueryRetriever",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.ADVANCED,
            display_name="Multi-Query Retriever",
            description="Generate multiple queries to improve retrieval coverage",
            icon="🔍",
            color="#06B6D4",
            examples=[
                "Comprehensive document search",
                "Multi-perspective retrieval",
                "Query expansion workflows"
            ],
            common_patterns=[
                "Research assistance",
                "Complex question answering",
                "Diverse perspective gathering"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["retriever", "llm_chain"],
            optional_params={
                "query_count": 3,
                "include_original": True,
                "unique_union": True
            },
            performance_hints=[
                "Balance query_count vs cost",
                "Use with high-quality base retriever",
                "Monitor token usage for query generation"
            ],
            cost_implications="Multiplies LLM calls by query_count"
        )
    ))
    
    # Contextual Compression Retriever
    node_registry.register(NodeDefinition(
        node_type="ContextualCompressionRetriever",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.ADVANCED,
            display_name="Contextual Compression Retriever",
            description="Compress and filter retrieved documents for relevance",
            icon="🗜️",
            color="#06B6D4",
            examples=[
                "Noise reduction in retrieval",
                "Context optimization",
                "Relevant passage extraction"
            ],
            common_patterns=[
                "High-precision RAG",
                "Large document processing",
                "Context window optimization"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["base_compressor", "base_retriever"],
            optional_params={
                "search_kwargs": {}
            },
            performance_hints=[
                "Choose appropriate compressor type",
                "Balance compression vs information loss",
                "Test with target document types"
            ]
        )
    ))
    
    # Ensemble Retriever
    node_registry.register(NodeDefinition(
        node_type="EnsembleRetriever",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.EXPERT,
            display_name="Ensemble Retriever",
            description="Combine multiple retrieval strategies for better results",
            icon="🎭",
            color="#06B6D4",
            examples=[
                "Hybrid search (vector + keyword)",
                "Multi-source retrieval",
                "Fallback retrieval strategies"
            ],
            common_patterns=[
                "Production RAG systems",
                "Multi-modal retrieval",
                "Robust information access"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["retrievers", "weights"],
            optional_params={
                "c": 60,  # RRF constant
                "id_key": "doc_id"
            },
            validation_rules={
                "weights": {"type": "list", "sum_to": 1.0}
            },
            performance_hints=[
                "Balance retriever strengths",
                "Tune weights empirically",
                "Monitor ensemble performance"
            ]
        )
    ))


def register_vectorstore_nodes():
    """Register vector store node definitions"""
    
    # Chroma
    node_registry.register(NodeDefinition(
        node_type="Chroma",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.BASIC,
            display_name="Chroma Vector Store",
            description="Open-source vector database for embeddings",
            icon="🎨",
            color="#A855F7",
            documentation_url="https://docs.trychroma.com/",
            examples=[
                "Local development vector store",
                "Document embedding storage",
                "Prototype RAG systems"
            ],
            common_patterns=[
                "Local RAG development",
                "Small to medium datasets",
                "Quick prototyping"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["embedding_function"],
            optional_params={
                "collection_name": "langchain",
                "persist_directory": None,
                "client_settings": {},
                "collection_metadata": {}
            },
            performance_hints=[
                "Use persistent directory for data retention",
                "Configure appropriate collection metadata",
                "Consider memory usage for large collections"
            ],
            cost_implications="Free open-source, hosting costs if deployed"
        )
    ))
    
    # Pinecone
    node_registry.register(NodeDefinition(
        node_type="Pinecone",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Pinecone Vector Store",
            description="Managed vector database service",
            icon="🌲",
            color="#A855F7",
            examples=[
                "Production vector search",
                "Large-scale embeddings",
                "High-performance retrieval"
            ],
            common_patterns=[
                "Production RAG systems",
                "Enterprise applications",
                "Scalable vector search"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["index_name", "embedding"],
            optional_params={
                "environment": "us-west1-gcp",
                "namespace": "",
                "text_key": "text",
                "pool_threads": 1
            },
            performance_hints=[
                "Choose appropriate pod type",
                "Use namespaces for multi-tenancy",
                "Monitor query performance"
            ],
            cost_implications="Subscription-based pricing by pod size"
        )
    ))
    
    # FAISS
    node_registry.register(NodeDefinition(
        node_type="FAISS",
        metadata=NodeMetadata(
            category=NodeCategory.RETRIEVER,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="FAISS Vector Store",
            description="Facebook's efficient similarity search library",
            icon="⚡",
            color="#A855F7",
            examples=[
                "High-performance local search",
                "Large-scale similarity search",
                "Research applications"
            ],
            common_patterns=[
                "Local high-performance retrieval",
                "Research and experimentation",
                "Custom deployment scenarios"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["embedding_function"],
            optional_params={
                "index": None,
                "docstore": {},
                "index_to_docstore_id": {},
                "normalize_L2": False
            },
            performance_hints=[
                "Choose appropriate FAISS index type",
                "Consider index training for large datasets",
                "Use GPU acceleration when available"
            ],
            cost_implications="Free library, compute costs only"
        )
    ))


def register_memory_nodes():
    """Register memory system node definitions"""
    
    # Conversation Buffer Memory
    node_registry.register(NodeDefinition(
        node_type="ConversationBufferMemory",
        metadata=NodeMetadata(
            category=NodeCategory.MEMORY,
            complexity=NodeComplexity.BASIC,
            display_name="Buffer Memory",
            description="Store conversation history in a simple buffer",
            icon="💭",
            color="#10B981",
            examples=[
                "Basic chat memory",
                "Short conversation tracking",
                "Simple context retention"
            ],
            common_patterns=[
                "Basic chatbots",
                "Short conversations",
                "Development and testing"
            ],
            troubleshooting={
                "memory_overflow": "Messages exceed context window",
                "context_loss": "Buffer cleared or not persisted"
            }
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={
                "memory_key": "history",
                "chat_memory": None,
                "output_key": None,
                "input_key": None,
                "return_messages": False
            },
            performance_hints=[
                "Monitor buffer size vs context limits",
                "Clear buffer periodically for long sessions",
                "Consider conversation summarization"
            ]
        )
    ))
    
    # Conversation Summary Memory
    node_registry.register(NodeDefinition(
        node_type="ConversationSummaryMemory",
        metadata=NodeMetadata(
            category=NodeCategory.MEMORY,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Summary Memory",
            description="Summarize conversation history to save tokens",
            icon="📝",
            color="#10B981",
            examples=[
                "Long conversation tracking",
                "Token-efficient memory",
                "Context summarization"
            ],
            common_patterns=[
                "Extended conversations",
                "Token optimization",
                "Intelligent context management"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["llm"],
            optional_params={
                "memory_key": "history",
                "return_messages": False,
                "buffer": "",
                "max_token_limit": 2000
            },
            performance_hints=[
                "Balance summary frequency vs accuracy",
                "Monitor summarization quality",
                "Consider summary prompt engineering"
            ],
            cost_implications="Additional LLM calls for summarization"
        )
    ))
    
    # Vector Store Retriever Memory
    node_registry.register(NodeDefinition(
        node_type="VectorStoreRetrieverMemory",
        metadata=NodeMetadata(
            category=NodeCategory.MEMORY,
            complexity=NodeComplexity.ADVANCED,
            display_name="Vector Memory",
            description="Store and retrieve memories using vector similarity",
            icon="🧠",
            color="#10B981",
            examples=[
                "Semantic memory retrieval",
                "Long-term memory systems",
                "Context-aware recall"
            ],
            common_patterns=[
                "Personalized assistants",
                "Knowledge-based conversations",
                "Contextual memory systems"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["retriever"],
            optional_params={
                "memory_key": "history",
                "input_key": None,
                "return_docs": True,
                "exclude_input_keys": []
            },
            performance_hints=[
                "Optimize retriever for memory patterns",
                "Consider memory indexing strategies",
                "Balance recall vs relevance"
            ]
        )
    ))
    
    # Conversation Knowledge Graph Memory
    node_registry.register(NodeDefinition(
        node_type="ConversationKGMemory",
        metadata=NodeMetadata(
            category=NodeCategory.MEMORY,
            complexity=NodeComplexity.EXPERT,
            display_name="Knowledge Graph Memory",
            description="Extract and store entities and relationships",
            icon="🕸️",
            color="#10B981",
            examples=[
                "Entity relationship tracking",
                "Structured knowledge extraction",
                "Graph-based reasoning"
            ],
            common_patterns=[
                "Knowledge-intensive applications",
                "Entity-centric conversations",
                "Structured information systems"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["llm"],
            optional_params={
                "memory_key": "history",
                "kg": None,
                "return_messages": False,
                "entity_extraction_prompt": None
            },
            performance_hints=[
                "Tune entity extraction prompts",
                "Monitor knowledge graph quality",
                "Consider graph database integration"
            ],
            cost_implications="High LLM usage for entity extraction"
        )
    ))


# Auto-register all nodes when module is imported
register_retriever_nodes()
register_vectorstore_nodes()
register_memory_nodes()


# Export for convenience
__all__ = [
    "register_retriever_nodes",
    "register_vectorstore_nodes",
    "register_memory_nodes"
]
