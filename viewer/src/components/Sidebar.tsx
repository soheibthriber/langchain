import React from 'react';
import { Node } from 'reactflow';
import { GraphJSONv11 } from '../types/GraphJSON';

interface SidebarProps {
  selectedNode: Node | null;
  graphData: GraphJSONv11 | null;
  currentEventIndex: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ selectedNode, graphData, currentEventIndex }) => {
  if (!selectedNode || !graphData) {
    return (
      <div className="w-80 bg-white border-l border-gray-200 p-4">
        <h2 className="text-lg font-semibold mb-4">Inspector</h2>
        <p className="text-gray-500">Select a node to view details</p>
      </div>
    );
  }

  const nodeArtifacts = graphData.artifacts[selectedNode.id];
  const nodeEvents = graphData.events.filter(event => event.nodeId === selectedNode.id);

  return (
    <div className="w-80 bg-white border-l border-gray-200 p-4 overflow-y-auto">
      <h2 className="text-lg font-semibold mb-4">Inspector</h2>
      
      <div className="space-y-4">
        {/* Overview Tab */}
        <div>
          <h3 className="text-md font-medium mb-2">Overview</h3>
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm space-y-1">
              <div><strong>ID:</strong> {selectedNode.id}</div>
              <div><strong>Type:</strong> {selectedNode.type}</div>
              <div><strong>Label:</strong> {selectedNode.data?.label}</div>
              {selectedNode.data?.tags && selectedNode.data.tags.length > 0 && (
                <div>
                  <strong>Tags:</strong>{' '}
                  {selectedNode.data.tags.map((tag: string) => (
                    <span key={tag} className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-1">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Prompt Tab */}
        {nodeArtifacts?.prompt && (
          <div>
            <h3 className="text-md font-medium mb-2">Prompt</h3>
            <div className="bg-gray-50 p-3 rounded text-sm">
              <div className="mb-2">
                <strong>Template:</strong>
                <pre className="mt-1 bg-white p-2 rounded border text-xs overflow-x-auto">
                  {nodeArtifacts.prompt}
                </pre>
              </div>
              {nodeArtifacts.resolved_prompt && (
                <div>
                  <strong>Resolved:</strong>
                  <pre className="mt-1 bg-white p-2 rounded border text-xs overflow-x-auto">
                    {nodeArtifacts.resolved_prompt}
                  </pre>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Output Tab */}
        {nodeArtifacts?.output && (
          <div>
            <h3 className="text-md font-medium mb-2">Output</h3>
            <div className="bg-gray-50 p-3 rounded">
              <pre className="text-sm bg-white p-2 rounded border overflow-x-auto">
                {typeof nodeArtifacts.output === 'string' 
                  ? nodeArtifacts.output 
                  : JSON.stringify(nodeArtifacts.output, null, 2)
                }
              </pre>
            </div>
          </div>
        )}

        {/* Events Tab */}
        {nodeEvents.length > 0 && (
          <div>
            <h3 className="text-md font-medium mb-2">Events</h3>
            <div className="space-y-2">
              {nodeEvents.map((event, index) => (
                <div 
                  key={index} 
                  className={`p-2 rounded text-sm border ${
                    index <= currentEventIndex ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                  }`}
                >
                  <div className="font-medium">{event.kind}</div>
                  <div className="text-gray-600 text-xs">{event.ts_ms}ms</div>
                  {Object.keys(event.payload).length > 0 && (
                    <pre className="mt-1 text-xs bg-white p-1 rounded overflow-x-auto">
                      {JSON.stringify(event.payload, null, 2)}
                    </pre>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
