import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface NodeData {
  label: string;
  description?: string;
  [key: string]: any;
}

// BASE STYLES - Common styling foundation
const getBaseNodeStyle = (accentColor: string): React.CSSProperties => ({
  background: 'white',
  border: '2px solid #e5e7eb',
  borderRadius: '8px',
  minWidth: '160px',
  maxWidth: '220px',
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  position: 'relative',
  transition: 'all 0.2s ease',
});

const getContentStyle = (): React.CSSProperties => ({
  padding: '12px',
  paddingTop: '16px',
});

const getAccentBarStyle = (gradient: string): React.CSSProperties => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  height: '4px',
  background: gradient,
  borderRadius: '6px 6px 0 0',
});

// 1. PROMPT TEMPLATE NODE - Text/Content focused
export const PromptTemplateNode: React.FC<NodeProps<NodeData>> = ({ data, isConnectable }) => {
  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '24px',
    height: '24px',
    background: '#fef3c7',
    borderRadius: '6px',
    color: '#d97706',
    marginBottom: '8px',
  };

  return (
    <div style={getBaseNodeStyle('#d97706')}>
      <div style={getAccentBarStyle('linear-gradient(90deg, #d97706 0%, #f59e0b 100%)')}></div>
      
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} isConnectable={isConnectable} />
      
      <div style={getContentStyle()}>
        <div style={iconStyle}>
          {/* Document/Text icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
        </div>
        <div style={{ fontSize: '13px', fontWeight: 600, color: '#92400e', marginBottom: '4px' }}>
          PROMPT
        </div>
        <div style={{ fontSize: '14px', fontWeight: 600, color: '#111827' }}>
          {data.label || 'Template'}
        </div>
      </div>

      <Handle type="source" position={Position.Right} style={{ background: '#555' }} isConnectable={isConnectable} />
    </div>
  );
};

// 2. LLM NODE - AI/Brain focused
export const LLMNode: React.FC<NodeProps<NodeData>> = ({ data, isConnectable }) => {
  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '24px',
    height: '24px',
    background: '#ddd6fe',
    borderRadius: '6px',
    color: '#7c3aed',
    marginBottom: '8px',
  };

  return (
    <div style={getBaseNodeStyle('#7c3aed')}>
      <div style={getAccentBarStyle('linear-gradient(90deg, #7c3aed 0%, #a855f7 100%)')}></div>
      
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} isConnectable={isConnectable} />
      
      <div style={getContentStyle()}>
        <div style={iconStyle}>
          {/* Brain/AI icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M21.33 12.91C21.42 14.46 20.71 15.95 19.44 16.86L20.21 18.35C20.44 18.8 20.47 19.33 20.27 19.8C20.08 20.27 19.69 20.64 19.21 20.8L18.42 21.05C18.25 21.11 18.06 21.14 17.88 21.14C17.37 21.14 16.89 20.91 16.56 20.5L14.44 18C13.55 17.85 12.71 17.47 12 16.9C11.5 17.05 11 17.13 10.5 17.13C9.53 17.13 8.61 16.81 7.85 16.25L5.64 18.92C5.31 19.33 4.83 19.56 4.32 19.56C4.14 19.56 3.95 19.53 3.78 19.47L2.99 19.22C2.51 19.06 2.12 18.69 1.93 18.22C1.73 17.75 1.76 17.22 1.99 16.77L2.76 15.28C1.49 14.37 0.78 12.88 0.87 11.33C0.95 9.78 1.8 8.38 3.15 7.64C3.39 6.19 4.17 4.88 5.34 4C6.5 3.11 7.96 2.72 9.4 2.91C10.08 2.32 10.91 1.94 11.8 1.8C12.69 1.66 13.6 1.77 14.42 2.13C15.24 2.5 15.93 3.1 16.41 3.85C16.89 4.6 17.13 5.47 17.11 6.35C18.46 7.09 19.31 8.49 19.39 10.04C19.47 10.64 19.47 11.25 19.39 11.85C20.36 12.18 21.08 12.91 21.33 12.91M16.36 7.58C16.08 7.19 15.71 6.88 15.29 6.67C14.87 6.46 14.4 6.35 13.93 6.37C13.46 6.39 13 6.53 12.6 6.78C12.2 7.03 11.87 7.38 11.65 7.8C11.43 8.22 11.33 8.69 11.36 9.16C11.39 9.63 11.55 10.09 11.82 10.48C12.09 10.87 12.46 11.18 12.88 11.39C13.3 11.6 13.77 11.71 14.24 11.69C14.71 11.67 15.17 11.53 15.57 11.28C15.97 11.03 16.3 10.68 16.52 10.26C16.74 9.84 16.84 9.37 16.81 8.9C16.78 8.43 16.62 7.97 16.36 7.58Z" />
          </svg>
        </div>
        <div style={{ fontSize: '13px', fontWeight: 600, color: '#6b21a8', marginBottom: '4px' }}>
          LLM
        </div>
        <div style={{ fontSize: '14px', fontWeight: 600, color: '#111827' }}>
          {data.label || 'Language Model'}
        </div>
      </div>

      <Handle type="source" position={Position.Right} style={{ background: '#555' }} isConnectable={isConnectable} />
    </div>
  );
};

// 3. PARSER NODE - Processing/Transform focused
export const ParserNode: React.FC<NodeProps<NodeData>> = ({ data, isConnectable }) => {
  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '24px',
    height: '24px',
    background: '#dcfce7',
    borderRadius: '6px',
    color: '#16a34a',
    marginBottom: '8px',
  };

  return (
    <div style={getBaseNodeStyle('#16a34a')}>
      <div style={getAccentBarStyle('linear-gradient(90deg, #16a34a 0%, #22c55e 100%)')}></div>
      
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} isConnectable={isConnectable} />
      
      <div style={getContentStyle()}>
        <div style={iconStyle}>
          {/* Transform/Process icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7.27C13.6,7.61 14,8.26 14,9A2,2 0 0,1 12,11A2,2 0 0,1 10,9C10,8.26 10.4,7.61 11,7.27V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M21,9V7L19,8L21,9M15,9A2,2 0 0,1 17,11A2,2 0 0,1 15,13A2,2 0 0,1 13,11A2,2 0 0,1 15,9M5,9A2,2 0 0,1 7,11A2,2 0 0,1 5,13A2,2 0 0,1 3,11A2,2 0 0,1 5,9M12,15A2,2 0 0,1 14,17C14,17.74 13.6,18.39 13,18.73V20.27C13.6,20.61 14,21.26 14,22A2,2 0 0,1 12,24A2,2 0 0,1 10,22C10,21.26 10.4,20.61 11,20.27V18.73C10.4,18.39 10,17.74 10,17A2,2 0 0,1 12,15Z" />
          </svg>
        </div>
        <div style={{ fontSize: '13px', fontWeight: 600, color: '#15803d', marginBottom: '4px' }}>
          PARSER
        </div>
        <div style={{ fontSize: '14px', fontWeight: 600, color: '#111827' }}>
          {data.label || 'Output Parser'}
        </div>
      </div>

      <Handle type="source" position={Position.Right} style={{ background: '#555' }} isConnectable={isConnectable} />
    </div>
  );
};

// 4. MEMORY NODE - Storage/History focused
export const MemoryNode: React.FC<NodeProps<NodeData>> = ({ data, isConnectable }) => {
  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '24px',
    height: '24px',
    background: '#fecaca',
    borderRadius: '6px',
    color: '#dc2626',
    marginBottom: '8px',
  };

  return (
    <div style={getBaseNodeStyle('#dc2626')}>
      <div style={getAccentBarStyle('linear-gradient(90deg, #dc2626 0%, #ef4444 100%)')}></div>
      
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} isConnectable={isConnectable} />
      
      <div style={getContentStyle()}>
        <div style={iconStyle}>
          {/* Memory/Database icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,3C7.58,3 4,4.79 4,7C4,9.21 7.58,11 12,11C16.42,11 20,9.21 20,7C20,4.79 16.42,3 12,3M4,9V12C4,14.21 7.58,16 12,16C16.42,16 20,14.21 20,12V9C20,11.21 16.42,13 12,13C7.58,13 4,11.21 4,9M4,14V17C4,19.21 7.58,21 12,21C16.42,21 20,19.21 20,17V14C20,16.21 16.42,18 12,18C7.58,18 4,16.21 4,14Z" />
          </svg>
        </div>
        <div style={{ fontSize: '13px', fontWeight: 600, color: '#b91c1c', marginBottom: '4px' }}>
          MEMORY
        </div>
        <div style={{ fontSize: '14px', fontWeight: 600, color: '#111827' }}>
          {data.label || 'Memory Buffer'}
        </div>
      </div>

      <Handle type="source" position={Position.Right} style={{ background: '#555' }} isConnectable={isConnectable} />
    </div>
  );
};

// 5. TOOL NODE - Action/Function focused
export const ToolNode: React.FC<NodeProps<NodeData>> = ({ data, isConnectable }) => {
  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '24px',
    height: '24px',
    background: '#e0e7ff',
    borderRadius: '6px',
    color: '#3730a3',
    marginBottom: '8px',
  };

  return (
    <div style={getBaseNodeStyle('#3730a3')}>
      <div style={getAccentBarStyle('linear-gradient(90deg, #3730a3 0%, #4f46e5 100%)')}></div>
      
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} isConnectable={isConnectable} />
      
      <div style={getContentStyle()}>
        <div style={iconStyle}>
          {/* Tool/Wrench icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M22.7,19L13.6,9.9C14.5,7.6 14,4.9 12.1,3C10.1,1 7.1,0.6 4.7,1.7L9,6L6,9L1.6,4.7C0.4,7.1 0.9,10.1 2.9,12.1C4.8,14 7.5,14.5 9.8,13.6L18.9,22.7C19.3,23.1 19.9,23.1 20.3,22.7L22.6,20.4C23.1,20 23.1,19.3 22.7,19Z" />
          </svg>
        </div>
        <div style={{ fontSize: '13px', fontWeight: 600, color: '#312e81', marginBottom: '4px' }}>
          TOOL
        </div>
        <div style={{ fontSize: '14px', fontWeight: 600, color: '#111827' }}>
          {data.label || 'Function Tool'}
        </div>
      </div>

      <Handle type="source" position={Position.Right} style={{ background: '#555' }} isConnectable={isConnectable} />
    </div>
  );
};

// 6. CHAIN NODE - Flow/Sequence focused  
export const ChainNode: React.FC<NodeProps<NodeData>> = ({ data, isConnectable }) => {
  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '24px',
    height: '24px',
    background: '#f3e8ff',
    borderRadius: '6px',
    color: '#9333ea',
    marginBottom: '8px',
  };

  return (
    <div style={getBaseNodeStyle('#9333ea')}>
      <div style={getAccentBarStyle('linear-gradient(90deg, #9333ea 0%, #a855f7 100%)')}></div>
      
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} isConnectable={isConnectable} />
      
      <div style={getContentStyle()}>
        <div style={iconStyle}>
          {/* Chain/Link icon */}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3.9,12C3.9,10.29 5.29,8.9 7,8.9H11V7H7A5,5 0 0,0 2,12A5,5 0 0,0 7,17H11V15.1H7C5.29,15.1 3.9,13.71 3.9,12M8,13H16V11H8V13M17,7H13V8.9H17C18.71,8.9 20.1,10.29 20.1,12C20.1,13.71 18.71,15.1 17,15.1H13V17H17A5,5 0 0,0 22,12A5,5 0 0,0 17,7Z" />
          </svg>
        </div>
        <div style={{ fontSize: '13px', fontWeight: 600, color: '#7e22ce', marginBottom: '4px' }}>
          CHAIN
        </div>
        <div style={{ fontSize: '14px', fontWeight: 600, color: '#111827' }}>
          {data.label || 'Processing Chain'}
        </div>
      </div>

      <Handle type="source" position={Position.Right} style={{ background: '#555' }} isConnectable={isConnectable} />
    </div>
  );
};

// Export all node types
export const specializedNodeTypes = {
  promptTemplate: PromptTemplateNode,
  prompt: PromptTemplateNode, // alias
  llm: LLMNode,
  parser: ParserNode,
  memory: MemoryNode,
  tool: ToolNode,
  chain: ChainNode,
};
