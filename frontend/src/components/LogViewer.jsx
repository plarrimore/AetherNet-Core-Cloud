import React, { useEffect, useRef } from 'react';

export default function LogViewer({ systemLogs }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [systemLogs]);

  return (
    <div class="bg-gray-900 border border-gray-800 rounded-lg p-5 h-full flex flex-col min-h-[450px]">
      <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 pb-2 border-b border-gray-800">
        📟 Core Agent Thread Streams
      </h3>
      <div 
        ref={containerRef}
        class="flex-1 font-mono text-[11px] leading-relaxed text-gray-300 overflow-y-auto space-y-2 pr-2 custom-scrollbar"
      >
        {systemLogs?.map((log, idx) => {
          let textClass = 'text-gray-400';
          if (log.includes('[LogAnalyzer]')) textClass = 'text-amber-400';
          if (log.includes('[ComplianceAgent]')) textClass = 'text-blue-400';
          if (log.includes('[RiskAssessor]')) textClass = 'text-purple-400';
          if (log.includes('[DeployEngine]')) textClass = 'text-emerald-400 font-bold';
          if (log.includes('[Governance UI]')) textClass = 'text-cyan-400 italic';
          
          return (
            <div key={idx} class={`${textClass} break-words border-l-2 border-gray-800 pl-2`}>
              {log}
            </div>
          );
        })}
      </div>
    </div>
  );
}