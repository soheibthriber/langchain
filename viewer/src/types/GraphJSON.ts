export interface GraphJSONv11 {
  metadata: {
    version: string;
    run_id: string;
    created_at: string;
    lesson_id: string;
    tags: string[];
  };
  nodes: GraphNode[];
  ports: GraphPort[];
  edges: GraphEdge[];
  groups: GraphGroup[];
  run: {
    latency_ms: number;
    tokens_in: number;
    tokens_out: number;
    cost: number | null;
    errors?: GraphError[];
  };
  events: GraphEvent[];
  artifacts: Record<string, GraphArtifact>;
  styles: Record<string, any>;
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  subType?: string;
  tags?: string[];
  style?: Record<string, any>;
  data: Record<string, any>;
}

export interface GraphPort {
  nodeId: string;
  portId: string;
  direction: 'in' | 'out';
  label: string;
}

export interface GraphEdge {
  id: string;
  source: string | { nodeId: string; portId?: string };
  target: string | { nodeId: string; portId?: string };
  label?: string;
  condition?: string;
}

export interface GraphGroup {
  id: string;
  label: string;
  nodeIds: string[];
  type: 'chain' | 'agent' | 'retriever' | 'graph';
  collapsed?: boolean;
}

export interface GraphEvent {
  ts_ms: number;
  kind: 'invoke_start' | 'invoke_end' | 'tool_call' | 'tool_result' | 'retriever_query' | 'retriever_result' | 'parser' | 'error';
  nodeId?: string;
  edgeId?: string;
  payload: Record<string, any>;
}

export interface GraphArtifact {
  prompt?: string;
  resolved_prompt?: string;
  output?: string;
  tool_io?: Record<string, any>;
  docs?: any[];
}

export interface GraphError {
  nodeId: string;
  message: string;
  at_ms: number;
}
