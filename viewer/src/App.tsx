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
import { ProfessionalNode } from './components/ProfessionalNodes';

// Register custom node types - using ProfessionalNode for all types
const nodeTypes: NodeTypes = {
  prompt: ProfessionalNode,
  promptTemplate: ProfessionalNode,
  llm: ProfessionalNode,
  chatModel: ProfessionalNode,
  parser: ProfessionalNode,
  embeddings: ProfessionalNode,
  textSplitter: ProfessionalNode,
  documentLoader: ProfessionalNode,
  retriever: ProfessionalNode,
  vectorStore: ProfessionalNode,
  conversationBufferMemory: ProfessionalNode,
  conversationSummaryMemory: ProfessionalNode,
  entityMemory: ProfessionalNode,
  customMemory: ProfessionalNode,
  sequentialChain: ProfessionalNode,
  routerChain: ProfessionalNode,
  mapReduceChain: ProfessionalNode,
  agent: ProfessionalNode,
  planner: ProfessionalNode,
  executor: ProfessionalNode,
  tool: ProfessionalNode,
  calculatorTool: ProfessionalNode,
  apiTool: ProfessionalNode,
  input: ProfessionalNode,
  output: ProfessionalNode,
  callbacks: ProfessionalNode,
  monitoring: ProfessionalNode,
  logging: ProfessionalNode,
  custom: ProfessionalNode,
};

const App: React.FC = () => {
  // Professional LangChain nodes - showcasing different component types
  const [nodes, setNodes, onNodesChange] = useNodesState([
    {
      id: 'prompt',
      type: 'promptTemplate',
      position: { x: 50, y: 100 },
      data: { label: 'PromptTemplate', type: 'promptTemplate' }
    },
    {
      id: 'llm',
      type: 'chatModel',
      position: { x: 350, y: 100 },
      data: { label: 'ChatOpenAI', type: 'chatModel' }
    },
    {
      id: 'parser',
      type: 'parser',
      position: { x: 650, y: 100 },
      data: { label: 'StrOutputParser', type: 'parser' }
    },
    {
      id: 'vectorstore',
      type: 'vectorStore',
      position: { x: 50, y: 250 },
      data: { label: 'ChromaDB', type: 'vectorStore' }
    },
    {
      id: 'retriever',
      type: 'retriever',
      position: { x: 350, y: 250 },
      data: { label: 'VectorRetriever', type: 'retriever' }
    },
    {
      id: 'memory',
      type: 'conversationBufferMemory',
      position: { x: 650, y: 250 },
      data: { label: 'ConversationMemory', type: 'conversationBufferMemory' }
    },
    {
      id: 'agent',
      type: 'agent',
      position: { x: 200, y: 400 },
      data: { label: 'ReActAgent', type: 'agent', isActive: true }
    },
    {
      id: 'tool',
      type: 'calculatorTool',
      position: { x: 500, y: 400 },
      data: { label: 'Calculator', type: 'calculatorTool', isRunning: true }
    }
  ]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([
    // Main chain flow
    { id: 'e1-2', source: 'prompt', target: 'llm', animated: true },
    { id: 'e2-3', source: 'llm', target: 'parser', animated: true },
    // RAG flow
    { id: 'e4-5', source: 'vectorstore', target: 'retriever', animated: true },
    { id: 'e5-2', source: 'retriever', target: 'llm', animated: true },
    // Memory connection
    { id: 'e6-2', source: 'memory', target: 'llm', animated: true },
    // Agent workflow
    { id: 'e7-8', source: 'agent', target: 'tool', animated: true },
    { id: 'e2-7', source: 'llm', target: 'agent', animated: true }
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
          <Background gap={12} size={1} />
          
          <Panel position="top-left">
            <div className="bg-white p-4 rounded-lg shadow-lg border space-y-3 max-w-xs">
              <h1 className="text-xl font-bold text-gray-800 flex items-center">
                <span className="mr-2">🔗</span>
                LangChain Visualizer
              </h1>
              <div className="text-sm text-gray-600 mb-2">
                Professional node design system showcasing different LangChain component types
              </div>
              <button
                onClick={loadSampleData}
                className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm"
              >
                📊 Load Sample (Lesson 1)
              </button>
              <div className="text-xs text-gray-500 pt-2 border-t">
                {nodes.length} nodes • {edges.length} connections
              </div>
            </div>
          </Panel>
        </ReactFlow>
      </div>

      <div className="w-80 bg-white border-l border-gray-200 p-4 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-4 flex items-center">
          <span className="mr-2">🔍</span>
          Inspector
        </h2>
        {selectedNode ? (
          <div className="space-y-4">
            {/* Node Info */}
            <div className="p-3 bg-gray-50 rounded-lg">
              <h3 className="font-medium text-lg mb-2">{selectedNode.data.label}</h3>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium text-gray-600">Type:</span>
                  <span className="ml-2 px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                    {selectedNode.data.type}
                  </span>
                </div>
                <div>
                  <span className="font-medium text-gray-600">ID:</span>
                  <span className="ml-2 font-mono text-xs text-gray-500">{selectedNode.id}</span>
                </div>
                {selectedNode.data.isActive && (
                  <div className="flex items-center text-blue-600">
                    <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
                    Active Node
                  </div>
                )}
                {selectedNode.data.isRunning && (
                  <div className="flex items-center text-green-600">
                    <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                    Currently Running
                  </div>
                )}
              </div>
            </div>
            
            {/* Connection Info */}
            <div className="p-3 bg-gray-50 rounded-lg">
              <h4 className="font-medium mb-2">Connections</h4>
              <div className="text-sm space-y-1">
                <div>
                  <span className="text-gray-600">Inputs:</span>
                  <span className="ml-2">{edges.filter(e => e.target === selectedNode.id).length}</span>
                </div>
                <div>
                  <span className="text-gray-600">Outputs:</span>
                  <span className="ml-2">{edges.filter(e => e.source === selectedNode.id).length}</span>
                </div>
              </div>
            </div>
            
            {/* Position Info */}
            <div className="p-3 bg-gray-50 rounded-lg">
              <h4 className="font-medium mb-2">Position</h4>
              <div className="text-sm space-y-1">
                <div>X: {Math.round(selectedNode.position.x)}</div>
                <div>Y: {Math.round(selectedNode.position.y)}</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="text-4xl mb-2">👆</div>
            <p className="text-gray-500">Select a node to view details</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
