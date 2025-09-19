import React from 'react';
import { Handle, Position } from 'reactflow';
import {
  AlignLeft,
  Bot,
  Filter,
  Network,
  Scissors,
  FileText,
  Search,
  Database,
  Layers,
  BookOpen,
  Contact,
  Archive,
  Workflow,
  GitBranch,
  GitMerge,
  Compass,
  Play,
  Wrench,
  Calculator,
  Plug,
  LogIn,
  LogOut,
  Radio,
  Activity,
  Code,
  Brain,
  Eye
} from 'lucide-react';

// Component type configuration mapping
export const nodeTypeConfig = {
  // Core Building Blocks
  prompt: {
    category: 'Core Building Blocks',
    icon: AlignLeft,
    colors: {
      bg: 'bg-blue-100',
      border: 'border-blue-400',
      text: 'text-blue-700',
      hover: 'hover:bg-blue-200'
    }
  },
  promptTemplate: {
    category: 'Core Building Blocks',
    icon: AlignLeft,
    colors: {
      bg: 'bg-blue-100',
      border: 'border-blue-400',
      text: 'text-blue-700',
      hover: 'hover:bg-blue-200'
    }
  },
  llm: {
    category: 'Core Building Blocks',
    icon: Bot,
    colors: {
      bg: 'bg-green-100',
      border: 'border-green-400',
      text: 'text-green-700',
      hover: 'hover:bg-green-200'
    }
  },
  chatModel: {
    category: 'Core Building Blocks',
    icon: Brain,
    colors: {
      bg: 'bg-green-100',
      border: 'border-green-400',
      text: 'text-green-700',
      hover: 'hover:bg-green-200'
    }
  },
  parser: {
    category: 'Core Building Blocks',
    icon: Filter,
    colors: {
      bg: 'bg-purple-100',
      border: 'border-purple-400',
      text: 'text-purple-700',
      hover: 'hover:bg-purple-200'
    }
  },
  
  // Knowledge & Data
  embeddings: {
    category: 'Knowledge & Data',
    icon: Network,
    colors: {
      bg: 'bg-orange-100',
      border: 'border-orange-400',
      text: 'text-orange-700',
      hover: 'hover:bg-orange-200'
    }
  },
  textSplitter: {
    category: 'Knowledge & Data',
    icon: Scissors,
    colors: {
      bg: 'bg-gray-100',
      border: 'border-gray-400',
      text: 'text-gray-700',
      hover: 'hover:bg-gray-200'
    }
  },
  documentLoader: {
    category: 'Knowledge & Data',
    icon: FileText,
    colors: {
      bg: 'bg-yellow-100',
      border: 'border-yellow-400',
      text: 'text-yellow-700',
      hover: 'hover:bg-yellow-200'
    }
  },
  retriever: {
    category: 'Knowledge & Data',
    icon: Search,
    colors: {
      bg: 'bg-teal-100',
      border: 'border-teal-400',
      text: 'text-teal-700',
      hover: 'hover:bg-teal-200'
    }
  },
  vectorStore: {
    category: 'Knowledge & Data',
    icon: Database,
    colors: {
      bg: 'bg-blue-800',
      border: 'border-blue-900',
      text: 'text-blue-100',
      hover: 'hover:bg-blue-700'
    }
  },
  
  // Memory
  conversationBufferMemory: {
    category: 'Memory',
    icon: Layers,
    colors: {
      bg: 'bg-sky-100',
      border: 'border-sky-400',
      text: 'text-sky-700',
      hover: 'hover:bg-sky-200'
    }
  },
  conversationSummaryMemory: {
    category: 'Memory',
    icon: BookOpen,
    colors: {
      bg: 'bg-sky-100',
      border: 'border-sky-400',
      text: 'text-sky-700',
      hover: 'hover:bg-sky-200'
    }
  },
  entityMemory: {
    category: 'Memory',
    icon: Contact,
    colors: {
      bg: 'bg-sky-100',
      border: 'border-sky-400',
      text: 'text-sky-700',
      hover: 'hover:bg-sky-200'
    }
  },
  customMemory: {
    category: 'Memory',
    icon: Archive,
    colors: {
      bg: 'bg-sky-100',
      border: 'border-sky-400',
      text: 'text-sky-700',
      hover: 'hover:bg-sky-200'
    }
  },
  
  // Chains & Flow
  sequentialChain: {
    category: 'Chains & Flow',
    icon: Workflow,
    colors: {
      bg: 'bg-slate-100',
      border: 'border-slate-400',
      text: 'text-slate-700',
      hover: 'hover:bg-slate-200'
    }
  },
  routerChain: {
    category: 'Chains & Flow',
    icon: GitBranch,
    colors: {
      bg: 'bg-slate-100',
      border: 'border-slate-400',
      text: 'text-slate-700',
      hover: 'hover:bg-slate-200'
    }
  },
  mapReduceChain: {
    category: 'Chains & Flow',
    icon: GitMerge,
    colors: {
      bg: 'bg-slate-100',
      border: 'border-slate-400',
      text: 'text-slate-700',
      hover: 'hover:bg-slate-200'
    }
  },
  
  // Agents & Planning
  agent: {
    category: 'Agents & Planning',
    icon: Bot,
    colors: {
      bg: 'bg-red-100',
      border: 'border-red-400',
      text: 'text-red-700',
      hover: 'hover:bg-red-200'
    }
  },
  planner: {
    category: 'Agents & Planning',
    icon: Compass,
    colors: {
      bg: 'bg-red-100',
      border: 'border-red-400',
      text: 'text-red-700',
      hover: 'hover:bg-red-200'
    }
  },
  executor: {
    category: 'Agents & Planning',
    icon: Play,
    colors: {
      bg: 'bg-red-100',
      border: 'border-red-400',
      text: 'text-red-700',
      hover: 'hover:bg-red-200'
    }
  },
  
  // Tools & Integrations
  tool: {
    category: 'Tools & Integrations',
    icon: Wrench,
    colors: {
      bg: 'bg-zinc-100',
      border: 'border-zinc-400',
      text: 'text-zinc-700',
      hover: 'hover:bg-zinc-200'
    }
  },
  calculatorTool: {
    category: 'Tools & Integrations',
    icon: Calculator,
    colors: {
      bg: 'bg-zinc-100',
      border: 'border-zinc-400',
      text: 'text-zinc-700',
      hover: 'hover:bg-zinc-200'
    }
  },
  apiTool: {
    category: 'Tools & Integrations',
    icon: Plug,
    colors: {
      bg: 'bg-zinc-100',
      border: 'border-zinc-400',
      text: 'text-zinc-700',
      hover: 'hover:bg-zinc-200'
    }
  },
  
  // Input/Output
  input: {
    category: 'Input/Output',
    icon: LogIn,
    colors: {
      bg: 'bg-emerald-100',
      border: 'border-emerald-400',
      text: 'text-emerald-700',
      hover: 'hover:bg-emerald-200'
    }
  },
  output: {
    category: 'Input/Output',
    icon: LogOut,
    colors: {
      bg: 'bg-purple-100',
      border: 'border-purple-400',
      text: 'text-purple-700',
      hover: 'hover:bg-purple-200'
    }
  },
  
  // Monitoring & Meta
  callbacks: {
    category: 'Monitoring & Meta',
    icon: Radio,
    colors: {
      bg: 'bg-amber-100',
      border: 'border-amber-400',
      text: 'text-amber-700',
      hover: 'hover:bg-amber-200'
    }
  },
  monitoring: {
    category: 'Monitoring & Meta',
    icon: Activity,
    colors: {
      bg: 'bg-amber-100',
      border: 'border-amber-400',
      text: 'text-amber-700',
      hover: 'hover:bg-amber-200'
    }
  },
  logging: {
    category: 'Monitoring & Meta',
    icon: Eye,
    colors: {
      bg: 'bg-amber-100',
      border: 'border-amber-400',
      text: 'text-amber-700',
      hover: 'hover:bg-amber-200'
    }
  },
  
  // Custom
  custom: {
    category: 'Custom',
    icon: Code,
    colors: {
      bg: 'bg-indigo-100',
      border: 'border-indigo-400',
      text: 'text-indigo-700',
      hover: 'hover:bg-indigo-200'
    }
  }
};

// Professional Node Component
interface ProfessionalNodeProps {
  data: {
    label: string;
    type: string;
    isActive?: boolean;
    isRunning?: boolean;
  };
}

export const ProfessionalNode: React.FC<ProfessionalNodeProps> = ({ data }) => {
  // Get configuration for this node type, fallback to custom if not found
  const config = nodeTypeConfig[data.type as keyof typeof nodeTypeConfig] || nodeTypeConfig.custom;
  const IconComponent = config.icon;
  
  // Dynamic classes based on state
  const baseClasses = `
    relative flex items-center p-3 rounded-lg border-2 shadow-sm 
    min-w-48 transition-all duration-200 hover:scale-105
    ${config.colors.bg} ${config.colors.border} ${config.colors.text} ${config.colors.hover}
  `;
  
  const activeClasses = data.isActive ? 'ring-2 ring-blue-400 ring-opacity-75' : '';
  const runningClasses = data.isRunning ? 'animate-pulse' : '';
  
  return (
    <div className={`${baseClasses} ${activeClasses} ${runningClasses}`}>
      {/* Input Handle */}
      <Handle 
        type="target" 
        position={Position.Left}
        className="w-3 h-3 bg-gray-400 border-2 border-white"
      />
      
      {/* Node Content */}
      <div className="flex items-center space-x-3">
        {/* Icon */}
        <div className={`flex-shrink-0 p-2 rounded-md ${config.colors.bg} border ${config.colors.border}`}>
          <IconComponent size={20} className={config.colors.text} />
        </div>
        
        {/* Text Content */}
        <div className="flex-1 min-w-0">
          {/* Main Label */}
          <div className={`font-semibold text-sm ${config.colors.text} truncate`}>
            {data.label}
          </div>
          {/* Category */}
          <div className="text-xs text-gray-500 mt-0.5">
            {config.category}
          </div>
        </div>
      </div>
      
      {/* Output Handle */}
      <Handle 
        type="source" 
        position={Position.Right}
        className="w-3 h-3 bg-gray-400 border-2 border-white"
      />
      
      {/* Running Indicator */}
      {data.isRunning && (
        <div className="absolute -top-1 -right-1">
          <div className="w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
          <div className="absolute top-0 right-0 w-3 h-3 bg-green-500 rounded-full"></div>
        </div>
      )}
    </div>
  );
};
