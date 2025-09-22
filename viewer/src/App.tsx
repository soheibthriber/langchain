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
import { specializedNodeTypes } from './components/SpecializedNodes';

// Register specialized node renderers that can show execution data
const nodeTypes: NodeTypes = specializedNodeTypes as unknown as NodeTypes;

const App: React.FC = () => {
  // Base URLs from Vite. In production, BASE_URL is '/langchain/' for GH Pages.
  const isDev: boolean = !!(import.meta as any).env?.DEV;
  const API_BASE: string = (import.meta as any).env?.VITE_API_BASE_URL || '';
  const PUBLIC_BASE: string = (import.meta as any).env?.BASE_URL || '/';
  const preferApi = isDev || (typeof API_BASE === 'string' && API_BASE.length > 0);
  const apiPrefix = API_BASE || '';
  // Start empty; populate from API (Load Sample)
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  const onSelectionChange = useCallback(({ nodes }: OnSelectionChangeParams) => {
    setSelectedNode(nodes.length > 0 ? nodes[0] : null);
  }, []);

  const loadSampleData = useCallback(async () => {
    try {
      // Prefer API in dev; fallback to static if unavailable
      const fetchApi = async () => {
        const res = await fetch(`${apiPrefix}/api/runs/01_hello_chain/latest`);
        if (!res.ok) throw new Error(String(res.status));
        return res.json();
      };
      const fetchStatic = async () => {
        const res = await fetch(`${PUBLIC_BASE}graph.json`);
        if (!res.ok) throw new Error(String(res.status));
        return res.json();
      };
      let data: any;
      try {
        data = preferApi ? await fetchApi() : await fetchStatic();
      } catch {
        data = preferApi ? await fetchStatic() : await fetchApi();
      }
        
        // Helpers: normalize node type to renderer keys
        const normalizeType = (t: string): string => {
          const map: Record<string, string> = {
            // prompts
            prompt: 'promptTemplate',
            PromptTemplate: 'promptTemplate',
            promptTemplate: 'promptTemplate',
            // llms
            llm: 'llm',
            chatModel: 'llm',
            ChatOpenAI: 'llm',
            ChatAnthropic: 'llm',
            // Prefer real providers
            Groq: 'llm',
            // parsers
            parser: 'parser',
            StrOutputParser: 'parser',
          };
          return map[t] || t;
        };

        // Helpers: build execution artifacts per node across v1.1 and v1.2
        const version = data?.metadata?.version || '1.1';
        const events: any[] = Array.isArray(data?.events) ? data.events : [];
        const artifactsRoot = data?.artifacts || {};

        const findEvent = (nodeId: string, kind: 'invoke_start' | 'invoke_end') =>
          events.find(e => e.node_id === nodeId || e.nodeId === nodeId && (kind ? e.kind === kind : true));

        const buildNodeArtifacts = (node: any) => {
          const t = node.type;
          const id = node.id;
          // v1.1 direct mapping by id keys
          if (version === '1.1') {
            if (id === 'prompt' || t === 'promptTemplate' || t === 'PromptTemplate') {
              const a = artifactsRoot.prompt || {};
              return {
                template: a.prompt || node?.data?.template,
                input_variables: a.input_variables,
                resolved_prompt: a.resolved_prompt,
              };
            }
            if (id === 'llm' || t === 'chatModel' || t === 'llm') {
              const a = artifactsRoot.llm || {};
              return {
                input: a.input,
                output: a.output,
                model_info: a.model_info,
              };
            }
            if (id === 'parser' || t === 'parser' || t === 'StrOutputParser') {
              const a = artifactsRoot.parser || {};
              return {
                input: a.input,
                output: a.output,
                parser_type: a.parser_type,
              };
            }
            return {};
          }
          // v1.2 mapping via named artifacts + node snapshot
          // Prompt
          if (t === 'PromptTemplate') {
            return {
              template: node?.configuration?.template || node?.template_preview,
              input_variables: node?.configuration?.input_variables,
              resolved_prompt: artifactsRoot?.formatted_prompt?.content,
            };
          }
          // LLM
          if (t === 'ChatOpenAI' || t === 'ChatAnthropic' || t === 'Groq' || t === 'llm' || t === 'chatModel') {
            const start = findEvent(id, 'invoke_start');
            return {
              input: start?.input_preview || artifactsRoot?.formatted_prompt?.content,
              output: artifactsRoot?.llm_output?.content,
              model_info: { name: node?.configuration?.model || node?.label },
            };
          }
          // Parser
          if (t === 'StrOutputParser' || t === 'parser') {
            const start = findEvent(id, 'invoke_start');
            return {
              input: start?.input_preview || artifactsRoot?.llm_output?.content,
              output: artifactsRoot?.final_output?.content,
              parser_type: 'string',
            };
          }
          return {};
        };

        // Convert to ReactFlow nodes
        const reactFlowNodes: Node[] = data.nodes.map((node: any, index: number) => {
          // Normalize by type first, then fall back to heuristics (id/label/data)
          let normalizedType = normalizeType(node.type);
          if (!normalizedType || normalizedType === 'unknown') {
            const label: string = node.label || '';
            const provider: string | undefined = node?.data?.provider;
            const modelType: string | undefined = node?.data?.model_type;
            if (node.id === 'llm' || /^(Groq:|ChatOpenAI:|Anthropic:|OpenAI:)/.test(label) || modelType === 'chat' || provider) {
              normalizedType = 'llm';
            } else if (node.id === 'prompt') {
              normalizedType = 'promptTemplate';
            } else if (node.id === 'parser') {
              normalizedType = 'parser';
            }
          }
          const execArtifacts = buildNodeArtifacts(node);
          return {
            id: node.id,
            type: normalizedType,
            position: { x: 120 + (index * 240), y: 180 },
            data: {
              label: node.label,
              type: normalizedType,
              nodeData: node,
              artifacts: execArtifacts,
            },
          } as Node;
        });

        const reactFlowEdges: Edge[] = data.edges.map((edge: any) => ({
          id: edge.id,
          source: typeof edge.source === 'string' ? edge.source : edge.source.nodeId,
          target: typeof edge.target === 'string' ? edge.target : edge.target.nodeId,
          animated: true,
          label: edge.label || ''
        }));

        setNodes(reactFlowNodes);
        setEdges(reactFlowEdges);
        
    console.log('Loaded GraphJSON data:', data);
    } catch (error) {
      console.warn('Load sample failed:', error);
    }
  }, [setNodes, setEdges, API_BASE, PUBLIC_BASE, preferApi, apiPrefix]);

  const runLesson = useCallback(async () => {
    try {
  if (!preferApi) {
        // Static mode: no API. Just load the sample graph from the static file.
        await loadSampleData();
        return;
      }
  const response = await fetch(`${apiPrefix}/api/run/01_hello_chain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: 'Explain how neural networks learn from data' }),
      });
      if (response.ok) {
        const data = await response.json();
        // Reuse the same mapping logic by faking a minimal GraphJSON container if needed
        const graph = data?.nodes ? data : { ...data };

        const normalizeType = (t: string): string => {
          const map: Record<string, string> = {
            prompt: 'promptTemplate',
            PromptTemplate: 'promptTemplate',
            promptTemplate: 'promptTemplate',
            llm: 'llm',
            chatModel: 'llm',
            ChatOpenAI: 'llm',
            ChatAnthropic: 'llm',
            Groq: 'llm',
            parser: 'parser',
            StrOutputParser: 'parser',
          };
          return map[t] || t;
        };

  const version = graph?.metadata?.version || '1.1';
        const artifactsRoot = graph?.artifacts || {};
        const buildNodeArtifacts = (node: any) => {
          const t = node.type;
          const id = node.id;
          if (version === '1.1') {
            if (id === 'prompt' || t === 'promptTemplate' || t === 'PromptTemplate') {
              const a = artifactsRoot.prompt || {};
              return { template: a.prompt || node?.data?.template, input_variables: a.input_variables, resolved_prompt: a.resolved_prompt };
            }
            if (id === 'llm' || t === 'chatModel' || t === 'llm') {
              const a = artifactsRoot.llm || {};
              return { input: a.input, output: a.output, model_info: a.model_info };
            }
            if (id === 'parser' || t === 'parser' || t === 'StrOutputParser') {
              const a = artifactsRoot.parser || {};
              return { input: a.input, output: a.output, parser_type: a.parser_type };
            }
          }
          return {};
        };

        const reactFlowNodes: Node[] = graph.nodes.map((node: any, index: number) => {
          let normalizedType = normalizeType(node.type);
          if (!normalizedType || normalizedType === 'unknown') {
            const label: string = node.label || '';
            const provider: string | undefined = node?.data?.provider;
            const modelType: string | undefined = node?.data?.model_type;
            if (node.id === 'llm' || /^(Groq:|ChatOpenAI:|Anthropic:|OpenAI:)/.test(label) || modelType === 'chat' || provider) {
              normalizedType = 'llm';
            } else if (node.id === 'prompt') {
              normalizedType = 'promptTemplate';
            } else if (node.id === 'parser') {
              normalizedType = 'parser';
            }
          }
          const execArtifacts = buildNodeArtifacts(node);
          return {
            id: node.id,
            type: normalizedType,
            position: { x: 120 + (index * 240), y: 180 },
            data: { label: node.label, type: normalizedType, nodeData: node, artifacts: execArtifacts },
          } as Node;
        });
        const reactFlowEdges: Edge[] = graph.edges.map((edge: any) => ({
          id: edge.id,
          source: typeof edge.source === 'string' ? edge.source : edge.source.nodeId,
          target: typeof edge.target === 'string' ? edge.target : edge.target.nodeId,
          animated: true,
          label: edge.label || ''
        }));
        setNodes(reactFlowNodes);
        setEdges(reactFlowEdges);
      }
    } catch (e) {
      console.warn('Run lesson failed:', e);
      await loadSampleData();
    }
  }, [setNodes, setEdges, API_BASE, apiPrefix, preferApi, loadSampleData]);

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
              <button
                onClick={runLesson}
                className="w-full mt-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium text-sm"
              >
                ▶️ Run Lesson (Groq)
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
                {selectedNode.data.nodeData?.description && (
                  <div>
                    <span className="font-medium text-gray-600">Description:</span>
                    <div className="ml-2 text-gray-700 text-xs mt-1">
                      {selectedNode.data.nodeData.description}
                    </div>
                  </div>
                )}
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

            {/* Node Details */}
            {selectedNode.data.nodeData && (
              <div className="p-3 bg-gray-50 rounded-lg">
                <h4 className="font-medium mb-2">Configuration</h4>
                <div className="text-sm space-y-1">
                  {Object.entries(selectedNode.data.nodeData).map(([key, value]) => (
                    <div key={key}>
                      <span className="font-medium text-gray-600 capitalize">{key.replace(/_/g, ' ')}:</span>
                      <span className="ml-2 text-gray-700">
                        {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Artifacts */}
            {selectedNode.data.artifacts && Object.keys(selectedNode.data.artifacts).length > 0 && (
              <div className="p-3 bg-yellow-50 rounded-lg">
                <h4 className="font-medium mb-2 flex items-center">
                  <span className="mr-1">📋</span>
                  Execution Data
                </h4>
                <div className="text-sm space-y-2">
                  {selectedNode.data.artifacts.user_input && (
                    <div>
                      <span className="font-medium text-gray-600">User Input:</span>
                      <div className="ml-2 p-2 bg-white rounded border text-xs font-mono">
                        "{selectedNode.data.artifacts.user_input}"
                      </div>
                    </div>
                  )}
                  {selectedNode.data.artifacts.template && (
                    <div>
                      <span className="font-medium text-gray-600">Template:</span>
                      <div className="ml-2 p-2 bg-white rounded border text-xs font-mono">
                        {selectedNode.data.artifacts.template}
                      </div>
                    </div>
                  )}
                  {selectedNode.data.artifacts.resolved_prompt && (
                    <div>
                      <span className="font-medium text-gray-600">Resolved Prompt:</span>
                      <div className="ml-2 p-2 bg-white rounded border text-xs">
                        {selectedNode.data.artifacts.resolved_prompt}
                      </div>
                    </div>
                  )}
                  {selectedNode.data.artifacts.output && (
                    <div>
                      <span className="font-medium text-gray-600">Output:</span>
                      <div className="ml-2 p-2 bg-green-50 rounded border text-xs">
                        {selectedNode.data.artifacts.output}
                      </div>
                    </div>
                  )}
                  {selectedNode.data.artifacts.model_info && (
                    <div>
                      <span className="font-medium text-gray-600">Model Info:</span>
                      <div className="ml-2 text-xs text-gray-700">
                        {JSON.stringify(selectedNode.data.artifacts.model_info, null, 2)}
                      </div>
                    </div>
                  )}
                  {(selectedNode.data.artifacts.input_length || selectedNode.data.artifacts.output_length) && (
                    <div className="flex gap-4 text-xs text-gray-600">
                      {selectedNode.data.artifacts.input_length && (
                        <span>Input: {selectedNode.data.artifacts.input_length} chars</span>
                      )}
                      {selectedNode.data.artifacts.output_length && (
                        <span>Output: {selectedNode.data.artifacts.output_length} chars</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}
            
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
