import React, { useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Panel,
  Node,
  Edge,
  NodeTypes,
  OnSelectionChangeParams,
} from 'reactflow';
import 'reactflow/dist/style.css';

// Simple node component
const CustomNode: React.FC<any> = ({ data }) => {
  const colors = {
    prompt: 'bg-blue-100 border-blue-300',
    llm: 'bg-green-100 border-green-300', 
    parser: 'bg-purple-100 border-purple-300'
  };
  
  const color = colors[data.type] || 'bg-gray-100 border-gray-300';
  
  return (
    <div className={`${color} border-2 rounded-lg p-3 min-w-32`}>
      <div className="font-medium text-sm">{data.label}</div>
    </div>
  );
};

// Register custom node types
const nodeTypes: NodeTypes = {
  prompt: CustomNode,
  llm: CustomNode,
  parser: CustomNode,
};

const App: React.FC = () => {
  // Simple rectangular nodes - load immediately
  const [nodes, setNodes, onNodesChange] = useNodesState([
    {
      id: 'prompt',
      type: 'prompt',
      position: { x: 100, y: 200 },
      data: { label: 'PromptTemplate', type: 'prompt' }
    },
    {
      id: 'llm',
      type: 'llm',
      position: { x: 300, y: 200 },
      data: { label: 'ChatOpenAI', type: 'llm' }
    },
    {
      id: 'parser',
      type: 'parser',
      position: { x: 500, y: 200 },
      data: { label: 'StrOutputParser', type: 'parser' }
    }
  ]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([
    { id: 'e1-2', source: 'prompt', target: 'llm', animated: true },
    { id: 'e2-3', source: 'llm', target: 'parser', animated: true }
  ]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const onSelectionChange = useCallback(({ nodes }: OnSelectionChangeParams) => {
    setSelectedNode(nodes.length > 0 ? nodes[0] : null);
  }, []);

  const loadSampleData = useCallback(async () => {
    try {
      const response = await fetch('/api/runs/01_hello_chain/latest');
      if (response.ok) {
        const data = await response.json();
        
        // Convert to simple format
        const reactFlowNodes: Node[] = data.nodes.map((node: any, index: number) => ({
          id: node.id,
          type: node.type,
          position: { x: 100 + (index * 200), y: 200 },
          data: {
            label: node.label,
            type: node.type
          },
        }));

        const reactFlowEdges: Edge[] = data.edges.map((edge: any) => ({
          id: edge.id,
          source: typeof edge.source === 'string' ? edge.source : edge.source.nodeId,
          target: typeof edge.target === 'string' ? edge.target : edge.target.nodeId,
          animated: true,
        }));

        setNodes(reactFlowNodes);
        setEdges(reactFlowEdges);
      }
    } catch (error) {
      console.warn('API not available');
    }
  }, [setNodes, setEdges]);

  return (
    <div className="w-full h-screen flex">
      <div className="flex-1 relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onSelectionChange={onSelectionChange}
          nodeTypes={nodeTypes}
          fitView
          className="bg-gray-50"
          style={{ width: '100%', height: '100%' }}
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
          
          <Panel position="top-left">
            <div className="bg-white p-4 rounded-lg shadow-lg border space-y-3">
              <h1 className="text-xl font-bold text-gray-800">LangChain Visualizer</h1>
              <button
                onClick={loadSampleData}
                className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
              >
                📊 Load Sample (Lesson 1)
              </button>
            </div>
          </Panel>
        </ReactFlow>
      </div>

      <div className="w-80 bg-white border-l border-gray-200 p-4">
        <h2 className="text-lg font-semibold mb-4">Inspector</h2>
        {selectedNode ? (
          <div>
            <h3 className="font-medium mb-2">{selectedNode.data.label}</h3>
            <p className="text-sm text-gray-600">Type: {selectedNode.data.type}</p>
          </div>
        ) : (
          <p className="text-gray-500">Select a node to view details</p>
        )}
      </div>
    </div>
  );
};

export default App;
