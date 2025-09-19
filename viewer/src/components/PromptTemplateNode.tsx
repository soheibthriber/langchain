import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface PromptTemplateData {
  label: string;
  template?: string;
  description?: string;
}

const PromptTemplateNode: React.FC<NodeProps<PromptTemplateData>> = ({ data, isConnectable }) => {
  const nodeStyle: React.CSSProperties = {
    background: 'white',
    border: '2px solid #e5e7eb',
    borderRadius: '8px',
    minWidth: '180px',
    maxWidth: '250px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    position: 'relative',
    transition: 'all 0.2s ease',
  };

  const contentStyle: React.CSSProperties = {
    padding: '12px',
    paddingTop: '16px', // Account for top accent bar
  };

  const headerStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '8px',
    color: '#6366f1',
    fontWeight: 600,
    fontSize: '12px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  };

  const iconStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '20px',
    height: '20px',
    background: '#f3f4f6',
    borderRadius: '4px',
    color: '#6366f1',
  };

  const titleStyle: React.CSSProperties = {
    color: '#6b7280',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '14px',
    fontWeight: 600,
    color: '#111827',
    marginBottom: '4px',
    wordWrap: 'break-word',
  };

  const descriptionStyle: React.CSSProperties = {
    fontSize: '11px',
    color: '#6b7280',
    lineHeight: 1.3,
    maxHeight: '40px',
    overflow: 'hidden',
  };

  const accentBarStyle: React.CSSProperties = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: 'linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%)',
    borderRadius: '6px 6px 0 0',
  };

  return (
    <div style={nodeStyle}>
      {/* Color accent bar on top */}
      <div style={accentBarStyle}></div>
      
      <Handle
        type="target"
        position={Position.Left}
        style={{ background: '#555' }}
        isConnectable={isConnectable}
      />
      
      <div style={contentStyle}>
        {/* Header with icon and title */}
        <div style={headerStyle}>
          <div style={iconStyle}>
            {/* Simple text/document icon */}
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
            </svg>
          </div>
          <span style={titleStyle}>Prompt Template</span>
        </div>
        
        {/* Node name/label */}
        <div style={labelStyle}>
          {data.label || 'Template'}
        </div>
        
        {/* Optional description */}
        {data.description && (
          <div style={descriptionStyle}>
            {data.description}
          </div>
        )}
      </div>

      <Handle
        type="source"
        position={Position.Right}
        style={{ background: '#555' }}
        isConnectable={isConnectable}
      />
    </div>
  );
};

export default PromptTemplateNode;
