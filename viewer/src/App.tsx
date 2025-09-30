import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
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
  const apiPrefix = API_BASE || '';
  
  // Lesson state
  const [currentLesson, setCurrentLesson] = useState('01_hello_chain');
  const [availableLessons, setAvailableLessons] = useState<Array<{
    id: string;
    lesson_id: string;
    title: string;
    latency_ms?: number;
    events_count?: number;
    created_at?: string;
  }>>([]);
  const [isPanelMinimized, setIsPanelMinimized] = useState(false);
  
  // Start empty; populate from API (Load Sample)
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);

  // Load available lessons on component mount
  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const baseUrl = isDev ? '' : apiPrefix;
        const response = await fetch(`${baseUrl}/api/lessons`);
        if (response.ok) {
          const data = await response.json();
          const lessonList = data.lessons.map((lesson: any) => ({
            id: lesson.id || lesson.lesson_id,
            lesson_id: lesson.lesson_id,
            title: formatLessonTitle(lesson.lesson_id),
            latency_ms: lesson.latency_ms,
            events_count: lesson.events_count,
            created_at: lesson.created_at
          }));
          // Sort lessons by lesson_id to ensure proper order (01_hello_chain before 02_prompt_patterns)
          lessonList.sort((a: any, b: any) => a.lesson_id.localeCompare(b.lesson_id));
          setAvailableLessons(lessonList);
        }
      } catch (error) {
        console.error('Failed to fetch lessons:', error);
        // Fallback to default lessons in correct order
        setAvailableLessons([
          { id: '01_hello_chain', lesson_id: '01_hello_chain', title: 'Hello Chain' },
          { id: '02_prompt_patterns', lesson_id: '02_prompt_patterns', title: 'Prompt Patterns' }
        ]);
      }
    };
    
    fetchLessons();
  }, [isDev, apiPrefix]);

  // Helper function to format lesson titles
  const formatLessonTitle = (lessonId: string) => {
    return lessonId
      .replace(/_/g, ' ')
      .replace(/^\d+\s*/, '')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Auto-load lesson data when lesson changes
  const loadLessonData = useCallback(async (lessonId: string) => {
    try {
      // In dev mode, use proxy; in production use API_BASE
      const baseUrl = isDev ? '' : apiPrefix;
      const url = `${baseUrl}/api/runs/${lessonId}/latest`;
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        
        // Normalization logic (copied from loadSampleData)
        const normalizeType = (type: string): string => {
          const lowerType = type.toLowerCase();
          if (lowerType.includes('prompt')) return 'promptTemplate';
          if (lowerType.includes('llm') || lowerType.includes('chat') || lowerType.includes('groq') || lowerType.includes('openai') || lowerType.includes('anthropic')) return 'llm';
          if (lowerType.includes('parser')) return 'parser';
          return 'unknown';
        };

        // Build node artifacts helper
        const buildNodeArtifacts = (node: any) => {
          const events: any[] = data.events || [];
          const artifacts: any = data.artifacts || {}; // artifacts is an object, not array
          const id = node.id;
          const findEvent = (nodeId: string, eventType: string) => 
            events.find(e => e.node_id === nodeId && e.event_type === eventType);
          const artifactsRoot = artifacts[id]; // Use object access instead of find
          const t = node.type;
          
          // PromptTemplate
          if (t === 'PromptTemplate' || t === 'promptTemplate' || t === 'prompt') {
            const start = findEvent(id, 'invoke_start');
            return {
              input: start?.input_preview,
              output: artifactsRoot?.resolved_prompt,
              template: node?.configuration?.template || artifactsRoot?.prompt,
            };
          }
          // LLM
          if (t === 'ChatOpenAI' || t === 'ChatAnthropic' || t === 'Groq' || t === 'llm' || t === 'chatModel') {
            const start = findEvent(id, 'invoke_start');
            return {
              input: start?.input_preview || artifactsRoot?.input,
              output: artifactsRoot?.output,
              model_info: artifactsRoot?.model_info || { name: node?.configuration?.model || node?.label },
            };
          }
          // Parser
          if (t === 'StrOutputParser' || t === 'parser') {
            const start = findEvent(id, 'invoke_start');
            return {
              input: start?.input_preview || artifactsRoot?.input,
              output: artifactsRoot?.output,
              parser_type: artifactsRoot?.parser_type || 'string',
            };
          }
          return {};
        };

        // Convert to ReactFlow nodes
        const reactFlowNodes: Node[] = data.nodes.map((node: any, index: number) => {
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
      } else {
        console.error('Failed to load lesson data:', response.status);
      }
    } catch (error) {
      console.error('Error loading lesson data:', error);
    }
  }, [isDev, apiPrefix, setNodes, setEdges]);

  // Load lesson data when currentLesson changes
  useEffect(() => {
    if (currentLesson) {
      loadLessonData(currentLesson);
    }
  }, [currentLesson, loadLessonData]);

  const onSelectionChange = useCallback(({ nodes }: OnSelectionChangeParams) => {
    setSelectedNode(nodes.length > 0 ? nodes[0] : null);
  }, []);

  return (
    <div className="w-full h-screen flex">
      {/* Fixed Left Panel */}
      <div className={`
        fixed top-0 left-0 h-full bg-white border-r border-gray-200 shadow-lg z-10 transition-all duration-300
        ${isPanelMinimized ? 'w-12' : 'w-80'}
      `}>
        {/* Header with minimize toggle */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          {!isPanelMinimized && (
            <h1 className="text-lg font-bold text-gray-800 flex items-center">
              <span className="mr-2">🔗</span>
              LangChain Lessons
            </h1>
          )}
          <button
            onClick={() => setIsPanelMinimized(!isPanelMinimized)}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            title={isPanelMinimized ? 'Expand panel' : 'Minimize panel'}
          >
            {isPanelMinimized ? '▶️' : '◀️'}
          </button>
        </div>

        {/* Panel Content */}
        {!isPanelMinimized && (
          <div className="p-4 overflow-y-auto h-[calc(100vh-80px)]">
            <div className="space-y-4">
              <div className="text-sm text-gray-600">
                Professional node design system showcasing different LangChain component types
              </div>
              
              {/* Lesson Chapters */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Available Lessons:</label>
                <div className="space-y-1">
                  {availableLessons.map((lesson, index) => (
                    <div
                      key={lesson.id}
                      onClick={() => setCurrentLesson(lesson.lesson_id)}
                      className={`
                        p-3 rounded-lg border cursor-pointer transition-all duration-200
                        ${currentLesson === lesson.lesson_id 
                          ? 'bg-indigo-50 border-indigo-300 shadow-sm' 
                          : 'bg-white border-gray-200 hover:bg-gray-50 hover:border-gray-300'
                        }
                      `}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`
                            w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold
                            ${currentLesson === lesson.lesson_id 
                              ? 'bg-indigo-600 text-white' 
                              : 'bg-gray-200 text-gray-600'
                            }
                          `}>
                            {index + 1}
                          </div>
                          <div>
                            <div className="font-medium text-gray-900 text-sm">
                              {lesson.title}
                            </div>
                            <div className="text-xs text-gray-500">
                              {lesson.lesson_id}
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          {lesson.events_count && (
                            <div className="text-xs text-gray-500">
                              {lesson.events_count} events
                            </div>
                          )}
                          {lesson.latency_ms && (
                            <div className="text-xs text-gray-400">
                              {lesson.latency_ms}ms
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="text-xs text-gray-500 pt-2 border-t">
                {nodes.length} nodes • {edges.length} connections
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div className={`flex-1 transition-all duration-300 ${isPanelMinimized ? 'ml-12' : 'ml-80'}`}>
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
                      {/* Check if this is lesson 2 with multiple strategies */}
                      {selectedNode.data.artifacts.output.includes('zero_shot:') && 
                       selectedNode.data.artifacts.output.includes('few_shot:') && 
                       selectedNode.data.artifacts.output.includes('cot:') ? (
                        <div className="ml-2 space-y-3">
                          {selectedNode.data.artifacts.output.split('\n\n').map((section: string, index: number) => {
                            if (section.trim().startsWith('zero_shot:')) {
                              return (
                                <div key={index} className="p-2 bg-red-50 rounded border border-red-200">
                                  <div className="font-semibold text-red-700 text-xs mb-1">🎯 Zero-Shot Strategy</div>
                                  <div className="text-xs text-gray-700">{section.replace('zero_shot:', '').trim()}</div>
                                </div>
                              );
                            } else if (section.trim().startsWith('few_shot:')) {
                              return (
                                <div key={index} className="p-2 bg-blue-50 rounded border border-blue-200">
                                  <div className="font-semibold text-blue-700 text-xs mb-1">📚 Few-Shot Strategy</div>
                                  <div className="text-xs text-gray-700">{section.replace('few_shot:', '').trim()}</div>
                                </div>
                              );
                            } else if (section.trim().startsWith('cot:')) {
                              return (
                                <div key={index} className="p-2 bg-amber-50 rounded border border-amber-200">
                                  <div className="font-semibold text-amber-700 text-xs mb-1">🧠 Chain-of-Thought Strategy</div>
                                  <div className="text-xs text-gray-700 whitespace-pre-wrap">{section.replace('cot:', '').trim()}</div>
                                </div>
                              );
                            }
                            return null;
                          })}
                        </div>
                      ) : (
                        <div className="ml-2 p-2 bg-green-50 rounded border text-xs">
                          {selectedNode.data.artifacts.output}
                        </div>
                      )}
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
