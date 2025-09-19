import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

export const PromptNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-4 min-w-40 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-blue-500 text-white rounded-lg flex items-center justify-center text-sm font-bold">
          📝
        </div>
        <div>
          <div className="font-semibold text-sm text-gray-800">{data.label}</div>
          {data.template && (
            <div className="text-xs text-gray-600 truncate max-w-32">
              {data.template}
            </div>
          )}
        </div>
      </div>
      {data.tags && data.tags.length > 0 && (
        <div className="mt-2">
          {data.tags.map((tag: string) => (
            <span key={tag} className="inline-block bg-blue-200 text-blue-800 text-xs px-2 py-1 rounded mr-1">
              {tag}
            </span>
          ))}
        </div>
      )}
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export const LLMNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="bg-green-50 border-2 border-green-300 rounded-lg p-4 min-w-40 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-green-500 text-white rounded-lg flex items-center justify-center text-lg">
          🤖
        </div>
        <div>
          <div className="font-semibold text-sm text-gray-800">{data.label}</div>
          {data.model && (
            <div className="text-xs text-gray-600">
              {data.model}
            </div>
          )}
        </div>
      </div>
      {data.tags && data.tags.length > 0 && (
        <div className="mt-2">
          {data.tags.map((tag: string) => (
            <span key={tag} className="inline-block bg-green-200 text-green-800 text-xs px-2 py-1 rounded mr-1">
              {tag}
            </span>
          ))}
        </div>
      )}
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export const ParserNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="bg-purple-50 border-2 border-purple-300 rounded-lg p-4 min-w-40 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-purple-500 text-white rounded-lg flex items-center justify-center text-lg">
          ⚙️
        </div>
        <div>
          <div className="font-semibold text-sm text-gray-800">{data.label}</div>
          <div className="text-xs text-gray-600">Output Parser</div>
        </div>
      </div>
      {data.tags && data.tags.length > 0 && (
        <div className="mt-2">
          {data.tags.map((tag: string) => (
            <span key={tag} className="inline-block bg-purple-200 text-purple-800 text-xs px-2 py-1 rounded mr-1">
              {tag}
            </span>
          ))}
        </div>
      )}
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
};
