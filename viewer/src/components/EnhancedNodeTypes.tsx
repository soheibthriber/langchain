import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

// PromptTemplate Node - Document/Template shape
export const PromptNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div className={`relative bg-gradient-to-br from-blue-50 to-blue-100 border-2 rounded-lg p-0 min-w-48 shadow-lg hover:shadow-xl transition-all duration-200 ${
      selected ? 'border-blue-500 ring-2 ring-blue-200' : 'border-blue-300'
    }`}>
      {/* Header section with icon and title */}
      <div className="bg-blue-500 text-white px-3 py-2 rounded-t-md flex items-center gap-2">
        <div className="w-6 h-6 flex items-center justify-center">
          📝
        </div>
        <div className="font-semibold text-sm">Prompt Template</div>
      </div>
      
      {/* Content section */}
      <div className="p-3">
        <div className="text-sm font-medium text-gray-800 mb-1">{data.label}</div>
        {data.template && (
          <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded border-l-2 border-blue-300 font-mono">
            {data.template.length > 60 ? data.template.substring(0, 60) + '...' : data.template}
          </div>
        )}
        
        {/* Variables indicator */}
        {data.template && data.template.includes('{') && (
          <div className="mt-2 flex items-center gap-1">
            <span className="w-2 h-2 bg-blue-400 rounded-full"></span>
            <span className="text-xs text-blue-600">Variables detected</span>
          </div>
        )}
      </div>
      
      {/* Connection handles */}
      <Handle 
        type="target" 
        position={Position.Left} 
        className="w-3 h-3 bg-blue-400 border-2 border-white"
      />
      <Handle 
        type="source" 
        position={Position.Right} 
        className="w-3 h-3 bg-blue-400 border-2 border-white"
      />
    </div>
  );
};

// LLM Node - Brain/Processing shape  
export const LLMNode: React.FC<NodeProps> = ({ data, selected }) => {
  const getModelIcon = (model: string) => {
    if (model?.includes('gpt')) return '🧠';
    if (model?.includes('claude')) return '🎭';
    if (model?.includes('gemini')) return '💎';
    return '🤖';
  };

  return (
    <div className={`relative bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl p-0 min-w-52 shadow-lg hover:shadow-xl transition-all duration-200 ${
      selected ? 'ring-2 ring-emerald-300' : ''
    }`}>
      {/* Hexagonal header design */}
      <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white px-4 py-3 rounded-t-xl relative">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center text-lg">
            {getModelIcon(data.model)}
          </div>
          <div>
            <div className="font-semibold text-sm">LLM Model</div>
            <div className="text-xs opacity-90">{data.model || 'AI Processor'}</div>
          </div>
        </div>
        
        {/* Processing indicator */}
        <div className="absolute top-2 right-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        </div>
      </div>
      
      {/* Content section */}
      <div className="p-3">
        <div className="text-sm font-medium text-gray-800 mb-2">{data.label}</div>
        
        {/* Model capabilities */}
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs text-gray-600">
            <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
            <span>Text Generation</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-gray-600">
            <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
            <span>Context Understanding</span>
          </div>
        </div>
      </div>
      
      {/* Connection handles with larger targets */}
      <Handle 
        type="target" 
        position={Position.Left} 
        className="w-4 h-4 bg-emerald-400 border-2 border-white rounded-full"
      />
      <Handle 
        type="source" 
        position={Position.Right} 
        className="w-4 h-4 bg-emerald-400 border-2 border-white rounded-full"
      />
    </div>
  );
};

// Parser Node - Transform/Filter shape
export const ParserNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div className={`relative bg-gradient-to-br from-purple-50 to-purple-100 border-2 rounded-lg p-0 min-w-44 shadow-lg hover:shadow-xl transition-all duration-200 ${
      selected ? 'border-purple-500 ring-2 ring-purple-200' : 'border-purple-300'
    }`}>
      {/* Funnel-like header */}
      <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-3 py-2 rounded-t-md">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-white bg-opacity-20 rounded flex items-center justify-center">
            ⚙️
          </div>
          <div className="font-semibold text-sm">Output Parser</div>
        </div>
      </div>
      
      {/* Transform visualization */}
      <div className="p-3">
        <div className="text-sm font-medium text-gray-800 mb-2">{data.label}</div>
        
        {/* Data flow visualization */}
        <div className="flex items-center justify-center py-2">
          <div className="flex items-center gap-2">
            <div className="w-6 h-2 bg-purple-200 rounded-l-full"></div>
            <div className="w-4 h-4 bg-purple-400 rounded border-2 border-white flex items-center justify-center">
              <div className="w-1 h-1 bg-white rounded-full"></div>
            </div>
            <div className="w-6 h-2 bg-purple-300 rounded-r-full"></div>
          </div>
        </div>
        
        <div className="text-xs text-purple-600 text-center">
          Raw → Structured
        </div>
      </div>
      
      {/* Connection handles */}
      <Handle 
        type="target" 
        position={Position.Left} 
        className="w-3 h-3 bg-purple-400 border-2 border-white"
      />
      <Handle 
        type="source" 
        position={Position.Right} 
        className="w-3 h-3 bg-purple-400 border-2 border-white"
      />
    </div>
  );
};

// Memory Node - Database/Storage shape
export const MemoryNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div className={`relative bg-gradient-to-br from-orange-50 to-orange-100 border-2 rounded-lg p-0 min-w-46 shadow-lg hover:shadow-xl transition-all duration-200 ${
      selected ? 'border-orange-500 ring-2 ring-orange-200' : 'border-orange-300'
    }`}>
      <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white px-3 py-2 rounded-t-md">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-white bg-opacity-20 rounded flex items-center justify-center">
            🧠
          </div>
          <div className="font-semibold text-sm">Memory</div>
        </div>
      </div>
      
      <div className="p-3">
        <div className="text-sm font-medium text-gray-800 mb-2">{data.label}</div>
        
        {/* Memory visualization */}
        <div className="space-y-1">
          <div className="w-full h-1.5 bg-orange-200 rounded-full overflow-hidden">
            <div className="w-3/4 h-full bg-orange-400 rounded-full"></div>
          </div>
          <div className="text-xs text-orange-600">Context stored</div>
        </div>
      </div>
      
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-orange-400 border-2 border-white" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-orange-400 border-2 border-white" />
    </div>
  );
};

// Vector Store Node - Database with search capability
export const VectorStoreNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div className={`relative bg-gradient-to-br from-indigo-50 to-indigo-100 border-2 rounded-lg p-0 min-w-48 shadow-lg hover:shadow-xl transition-all duration-200 ${
      selected ? 'border-indigo-500 ring-2 ring-indigo-200' : 'border-indigo-300'
    }`}>
      <div className="bg-gradient-to-r from-indigo-500 to-indigo-600 text-white px-3 py-2 rounded-t-md">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-white bg-opacity-20 rounded flex items-center justify-center">
            📚
          </div>
          <div className="font-semibold text-sm">Vector Store</div>
        </div>
      </div>
      
      <div className="p-3">
        <div className="text-sm font-medium text-gray-800 mb-2">{data.label}</div>
        
        {/* Vector visualization */}
        <div className="grid grid-cols-3 gap-1 mb-2">
          {[...Array(9)].map((_, i) => (
            <div key={i} className="w-2 h-2 bg-indigo-300 rounded-sm"></div>
          ))}
        </div>
        <div className="text-xs text-indigo-600">Embeddings ready</div>
      </div>
      
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-indigo-400 border-2 border-white" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-indigo-400 border-2 border-white" />
    </div>
  );
};

// Chain Node - Sequential workflow container
export const ChainNode: React.FC<NodeProps> = ({ data, selected }) => {
  return (
    <div className={`relative bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-dashed rounded-lg p-0 min-w-52 shadow-lg hover:shadow-xl transition-all duration-200 ${
      selected ? 'border-gray-500 ring-2 ring-gray-200' : 'border-gray-400'
    }`}>
      <div className="bg-gradient-to-r from-gray-600 to-gray-700 text-white px-3 py-2 rounded-t-md">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-white bg-opacity-20 rounded flex items-center justify-center">
            🔗
          </div>
          <div className="font-semibold text-sm">Chain</div>
        </div>
      </div>
      
      <div className="p-3">
        <div className="text-sm font-medium text-gray-800 mb-2">{data.label}</div>
        
        {/* Chain steps visualization */}
        <div className="flex items-center gap-1">
          {[...Array(4)].map((_, i) => (
            <React.Fragment key={i}>
              <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
              {i < 3 && <div className="w-2 h-0.5 bg-gray-300"></div>}
            </React.Fragment>
          ))}
        </div>
        <div className="text-xs text-gray-600 mt-1">Sequential workflow</div>
      </div>
      
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-gray-400 border-2 border-white" />
      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-gray-400 border-2 border-white" />
    </div>
  );
};
