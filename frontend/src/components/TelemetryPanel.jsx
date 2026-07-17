import React from 'react';

export default function TelemetryPanel({ telemetry }) {
  const telemetryEntries = Object.entries(telemetry || {});
  
  const totalCost = telemetryEntries.reduce((acc, [_, data]) => acc + (data.cost_usd || 0), 0);
  const totalTime = telemetryEntries.reduce((acc, [_, data]) => acc + (data.latency_sec || 0), 0);

  return (
    <div class="bg-gray-900 border border-gray-800 rounded-lg p-5 space-y-4">
      <div class="flex justify-between items-center pb-2 border-b border-gray-800">
        <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">
          📊 LLM Real-Time Trace Telemetry
        </h3>
        <span class="text-[10px] font-mono text-cyan-400 bg-cyan-950/50 border border-cyan-800 px-2 py-0.5 rounded">
          Model: gpt-4o-mini
        </span>
      </div>

      {/* Aggregate Overview Metrics */}
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-950 p-3 rounded border border-gray-800/60">
          <div class="text-[10px] text-gray-500 uppercase font-medium">Total Tokens Cost</div>
          <div class="text-lg font-mono font-bold text-cyan-400 mt-1">
            ${totalCost.toFixed(6)}
          </div>
        </div>
        <div class="bg-gray-950 p-3 rounded border border-gray-800/60">
          <div class="text-[10px] text-gray-500 uppercase font-medium">Total Graph Latency</div>
          <div class="text-lg font-mono font-bold text-purple-400 mt-1">
            {totalTime.toFixed(3)}s
          </div>
        </div>
      </div>

      {/* Individual Node Resource Breakdowns */}
      <div class="space-y-2.5 pt-2">
        <div class="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">Node Breakdown</div>
        {telemetryEntries.length === 0 ? (
          <p class="text-xs text-gray-600 italic py-2">Awaiting network ingestion events...</p>
        ) : (
          telemetryEntries.map(([nodeName, metrics]) => (
            <div key={nodeName} class="bg-gray-950 rounded p-3 border border-gray-800/40 text-xs space-y-2">
              <div class="flex justify-between items-center font-medium text-gray-300">
                <span>{nodeName}</span>
                <span class="font-mono text-purple-400 text-[11px]">{metrics.latency_sec}s</span>
              </div>
              <div class="flex justify-between items-center text-[11px] font-mono text-gray-500">
                <div>
                  Tokens: <span class="text-gray-400">{metrics.input_tokens}⚙️</span> / <span class="text-gray-400">{metrics.output_tokens}✍️</span>
                </div>
                <div class="text-cyan-500/90 font-medium">
                  ${metrics.cost_usd?.toFixed(6)}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}