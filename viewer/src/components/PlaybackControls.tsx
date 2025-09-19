import React from 'react';
import { GraphEvent } from '../types/GraphJSON';

interface PlaybackControlsProps {
  events: GraphEvent[];
  currentIndex: number;
  onIndexChange: (index: number) => void;
}

export const PlaybackControls: React.FC<PlaybackControlsProps> = ({ 
  events, 
  currentIndex, 
  onIndexChange 
}) => {
  if (events.length === 0) return null;

  return (
    <div className="bg-white p-3 rounded-lg shadow-lg flex items-center gap-3">
      <button
        onClick={() => onIndexChange(Math.max(0, currentIndex - 1))}
        disabled={currentIndex === 0}
        className="px-3 py-1 bg-blue-500 text-white rounded disabled:bg-gray-300"
      >
        ← Prev
      </button>
      
      <div className="flex items-center gap-2">
        <span className="text-sm">
          Event {currentIndex + 1} of {events.length}
        </span>
        <input
          type="range"
          min={0}
          max={events.length - 1}
          value={currentIndex}
          onChange={(e) => onIndexChange(parseInt(e.target.value))}
          className="w-32"
        />
      </div>
      
      <button
        onClick={() => onIndexChange(Math.min(events.length - 1, currentIndex + 1))}
        disabled={currentIndex === events.length - 1}
        className="px-3 py-1 bg-blue-500 text-white rounded disabled:bg-gray-300"
      >
        Next →
      </button>
      
      <div className="text-xs text-gray-600">
        {events[currentIndex]?.kind} at {events[currentIndex]?.ts_ms}ms
      </div>
    </div>
  );
};
