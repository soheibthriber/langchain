"""
Extended Node Definitions - Advanced LLMs & Embeddings
======================================================

This module extends the node registry with comprehensive LLM provider
definitions including local models, embeddings, and specialized models.
"""

from core.node_registry import (
    NodeCategory, NodeComplexity, NodeMetadata, NodeConfiguration, 
    NodeDefinition, node_registry
)


def register_llm_nodes():
    """Register all LLM provider node definitions"""
    
    # Claude (Anthropic)
    node_registry.register(NodeDefinition(
        node_type="ChatAnthropic",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Claude (Anthropic)",
            description="Anthropic's Claude models for advanced reasoning",
            icon="🧠",
            color="#FF6B35",
            documentation_url="https://docs.anthropic.com/claude/docs",
            examples=[
                "Long-form analysis",
                "Complex reasoning tasks",
                "Code review and explanation"
            ],
            common_patterns=[
                "Constitutional AI workflows",
                "Large context processing",
                "Ethical AI applications"
            ],
            troubleshooting={
                "context_length": "Claude supports up to 200k tokens",
                "safety_filters": "Content may be filtered for safety",
                "rate_limits": "Check API tier limits"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["model"],
            optional_params={
                "temperature": 0.7,
                "max_tokens": 4096,
                "top_p": 1.0,
                "top_k": 250,
                "streaming": False
            },
            validation_rules={
                "temperature": {"type": "float", "min": 0.0, "max": 1.0},
                "max_tokens": {"type": "integer", "min": 1, "max": 8192}
            },
            performance_hints=[
                "Use claude-3-sonnet for balanced performance",
                "claude-3-opus for complex reasoning",
                "claude-3-haiku for speed"
            ],
            cost_implications="Premium pricing, varies by model size"
        )
    ))
    
    # Google Gemini
    node_registry.register(NodeDefinition(
        node_type="ChatGoogleGenerativeAI",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Google Gemini",
            description="Google's multimodal Gemini models",
            icon="💎",
            color="#4285F4",
            documentation_url="https://ai.google.dev/docs",
            examples=[
                "Multimodal analysis",
                "Code generation",
                "Mathematical reasoning"
            ],
            common_patterns=[
                "Vision + text workflows",
                "Scientific computing",
                "Educational applications"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["model"],
            optional_params={
                "temperature": 0.7,
                "top_p": 1.0,
                "top_k": 40,
                "max_output_tokens": 2048,
                "safety_settings": {}
            },
            performance_hints=[
                "gemini-pro for text tasks",
                "gemini-pro-vision for multimodal",
                "Generous free tier available"
            ],
            cost_implications="Free tier available, pay-per-token beyond limits"
        )
    ))
    
    # Groq (Fast Inference)
    node_registry.register(NodeDefinition(
        node_type="ChatGroq",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Groq (Fast LLM)",
            description="Ultra-fast LLM inference with Groq hardware",
            icon="⚡",
            color="#FF4444",
            examples=[
                "Real-time chat applications",
                "Interactive demos",
                "High-throughput processing"
            ],
            common_patterns=[
                "Speed-critical applications",
                "Streaming responses",
                "Batch processing"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["model"],
            optional_params={
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 1.0,
                "stream": False
            },
            performance_hints=[
                "llama2-70b-4096 for quality",
                "mixtral-8x7b-32768 for speed",
                "Excellent free tier"
            ],
            cost_implications="Very competitive pricing, generous free tier"
        )
    ))
    
    # Hugging Face Models
    node_registry.register(NodeDefinition(
        node_type="HuggingFacePipeline",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.ADVANCED,
            display_name="Hugging Face Pipeline",
            description="Open-source models via Hugging Face transformers",
            icon="🤗",
            color="#FFD21E",
            documentation_url="https://huggingface.co/docs/transformers",
            examples=[
                "Local model deployment",
                "Custom fine-tuned models",
                "Specialized model architectures"
            ],
            common_patterns=[
                "Privacy-first deployments",
                "Custom model workflows",
                "Research applications"
            ],
            troubleshooting={
                "model_not_found": "Check model name and availability",
                "gpu_memory": "Reduce batch size or use smaller model",
                "slow_inference": "Consider GPU acceleration"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["model_id"],
            optional_params={
                "task": "text-generation",
                "device": "auto",
                "model_kwargs": {},
                "pipeline_kwargs": {},
                "batch_size": 1
            },
            validation_rules={
                "batch_size": {"type": "integer", "min": 1, "max": 32}
            },
            performance_hints=[
                "Use GPU for faster inference",
                "Cache models locally",
                "Consider quantized models for efficiency"
            ],
            cost_implications="Free for inference, costs for compute resources"
        )
    ))
    
    # Ollama (Local Models)
    node_registry.register(NodeDefinition(
        node_type="ChatOllama",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Ollama (Local)",
            description="Run LLMs locally with Ollama",
            icon="🦙",
            color="#2DD4BF",
            documentation_url="https://ollama.ai/docs",
            examples=[
                "Privacy-sensitive applications",
                "Offline usage",
                "Development and testing"
            ],
            common_patterns=[
                "Local development workflows",
                "Air-gapped deployments",
                "Cost-free inference"
            ],
            troubleshooting={
                "connection_failed": "Ensure Ollama server is running",
                "model_not_found": "Pull model with 'ollama pull'",
                "slow_performance": "Consider hardware requirements"
            }
        ),
        configuration=NodeConfiguration(
            required_params=["model"],
            optional_params={
                "base_url": "http://localhost:11434",
                "temperature": 0.7,
                "top_p": 1.0,
                "top_k": 40,
                "repeat_penalty": 1.1
            },
            performance_hints=[
                "Use llama2 for general tasks",
                "codellama for programming",
                "mistral for efficiency"
            ],
            cost_implications="Free - only local compute costs"
        )
    ))


def register_embedding_nodes():
    """Register embedding model node definitions"""
    
    # OpenAI Embeddings
    node_registry.register(NodeDefinition(
        node_type="OpenAIEmbeddings",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.BASIC,
            display_name="OpenAI Embeddings",
            description="High-quality text embeddings from OpenAI",
            icon="🔢",
            color="#74C0FC",
            examples=[
                "Semantic search",
                "Document similarity",
                "Clustering and classification"
            ],
            common_patterns=[
                "RAG system embeddings",
                "Semantic search engines",
                "Content recommendation"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={
                "model": "text-embedding-3-small",
                "dimensions": None,
                "chunk_size": 1000,
                "max_retries": 2
            },
            performance_hints=[
                "text-embedding-3-small for cost efficiency",
                "text-embedding-3-large for quality",
                "Batch embeddings for efficiency"
            ],
            cost_implications="Pay per token, very cost-effective"
        )
    ))
    
    # Hugging Face Embeddings
    node_registry.register(NodeDefinition(
        node_type="HuggingFaceEmbeddings",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.INTERMEDIATE,
            display_name="Hugging Face Embeddings",
            description="Open-source embedding models via Hugging Face",
            icon="🤗",
            color="#74C0FC",
            examples=[
                "Local embedding generation",
                "Custom domain embeddings",
                "Privacy-preserving embeddings"
            ],
            common_patterns=[
                "Local RAG systems",
                "Custom embedding pipelines",
                "Research applications"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=[],
            optional_params={
                "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                "model_kwargs": {},
                "encode_kwargs": {},
                "multi_process": False
            },
            performance_hints=[
                "Use sentence-transformers models",
                "Enable multi_process for large datasets",
                "Consider model size vs quality tradeoffs"
            ],
            cost_implications="Free for inference, compute costs only"
        )
    ))


def register_specialized_models():
    """Register specialized model node definitions"""
    
    # Code Generation Models
    node_registry.register(NodeDefinition(
        node_type="CodeLlama",
        metadata=NodeMetadata(
            category=NodeCategory.LLM,
            complexity=NodeComplexity.ADVANCED,
            display_name="Code Llama",
            description="Specialized code generation and understanding model",
            icon="💻",
            color="#00D2FF",
            examples=[
                "Code completion",
                "Code explanation",
                "Debugging assistance"
            ],
            common_patterns=[
                "IDE integrations",
                "Code review workflows",
                "Programming education"
            ]
        ),
        configuration=NodeConfiguration(
            required_params=["model_size"],
            optional_params={
                "variant": "base",  # base, instruct, python
                "temperature": 0.1,
                "max_tokens": 2048
            },
            performance_hints=[
                "Use lower temperature for code",
                "python variant for Python-specific tasks",
                "instruct variant for explanations"
            ]
        )
    ))


# Auto-register all LLM nodes when module is imported
register_llm_nodes()
register_embedding_nodes() 
register_specialized_models()


# Export for convenience
__all__ = [
    "register_llm_nodes",
    "register_embedding_nodes", 
    "register_specialized_models"
]
