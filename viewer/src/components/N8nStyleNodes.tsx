import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

// Common node wrapper with n8n styling
const N8nNodeWrapper: React.FC<{
  children: React.ReactNode;
  color: string;
  selected?: boolean;
}> = ({ children, color, selected }) => (
  <div
    className={`
      bg-white rounded-lg border-2 shadow-lg min-w-[120px] h-[80px]
      flex flex-col items-center justify-center p-2 relative
      transition-all duration-200 hover:shadow-xl
      ${selected ? 'border-blue-500 shadow-blue-200' : 'border-gray-200'}
    `}
    style={{
      borderTopColor: color,
      borderTopWidth: '4px',
    }}
  >
    <Handle
      type="target"
      position={Position.Left}
      className="w-3 h-3 !bg-gray-400 border-2 border-white"
    />
    {children}
    <Handle
      type="source"
      position={Position.Right}
      className="w-3 h-3 !bg-gray-400 border-2 border-white"
    />
  </div>
);

// Prompt Template Node - Document/Text style
export const N8nPromptNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#3B82F6" selected={selected}>
    <div className="text-2xl mb-1">📝</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Prompt'}
    </div>
  </N8nNodeWrapper>
);

// LLM Node - AI/Brain style  
export const N8nLLMNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#10B981" selected={selected}>
    <div className="text-2xl mb-1">🤖</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.model || 'LLM'}
    </div>
  </N8nNodeWrapper>
);

// Parser Node - Transform/Processing style
export const N8nParserNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#8B5CF6" selected={selected}>
    <div className="text-2xl mb-1">⚙️</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Parser'}
    </div>
  </N8nNodeWrapper>
);

// Memory Node - Storage style
export const N8nMemoryNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#F97316" selected={selected}>
    <div className="text-2xl mb-1">🧠</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Memory'}
    </div>
  </N8nNodeWrapper>
);

// Vector Store Node - Database style
export const N8nVectorStoreNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#6366F1" selected={selected}>
    <div className="text-2xl mb-1">📚</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Vector Store'}
    </div>
  </N8nNodeWrapper>
);

// Chain Node - Workflow/Connection style
export const N8nChainNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#6B7280" selected={selected}>
    <div className="text-2xl mb-1">🔗</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Chain'}
    </div>
  </N8nNodeWrapper>
);

// Agent Node - Human/Robot style  
export const N8nAgentNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#EC4899" selected={selected}>
    <div className="text-2xl mb-1">🕴️</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Agent'}
    </div>
  </N8nNodeWrapper>
);

// Tool Node - Utility/Function style
export const N8nToolNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#F59E0B" selected={selected}>
    <div className="text-2xl mb-1">🔧</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Tool'}
    </div>
  </N8nNodeWrapper>
);

// Retriever Node - Search/Find style
export const N8nRetrieverNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#14B8A6" selected={selected}>
    <div className="text-2xl mb-1">🔍</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Retriever'}
    </div>
  </N8nNodeWrapper>
);

// Document Loader Node - Import/Load style
export const N8nDocumentLoaderNode: React.FC<NodeProps> = ({ data, selected }) => (
  <N8nNodeWrapper color="#EF4444" selected={selected}>
    <div className="text-2xl mb-1">📄</div>
    <div className="text-xs font-medium text-gray-700 text-center leading-tight">
      {data.label || 'Loader'}
    </div>
  </N8nNodeWrapper>
);

// Export all node types for easy registration
export const n8nNodeTypes = {
  prompt: N8nPromptNode,
  promptTemplate: N8nPromptNode,
  llm: N8nLLMNode,
  parser: N8nParserNode,
  memory: N8nMemoryNode,
  vectorstore: N8nVectorStoreNode,
  vectorStore: N8nVectorStoreNode,
  chain: N8nChainNode,
  agent: N8nAgentNode,
  tool: N8nToolNode,
  retriever: N8nRetrieverNode,
  documentLoader: N8nDocumentLoaderNode,
};
