import React from 'react';

export default function Dashboard({ state, onAction }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Analyzing': return 'bg-amber-500 text-amber-950 animate-pulse';
      case 'Reviewing': return 'bg-purple-500 text-white animate-pulse';
      case 'Approved': return 'bg-indigo-500 text-white';
      case 'Deployed': return 'bg-emerald-500 text-emerald-950 font-bold';
      case 'Rejected': return 'bg-rose-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  return (
    <div class="space-y-6">
      {/* Metrics Banner */}
      <div class="bg-gray-900 border border-gray-800 rounded-lg p-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <div class="text-xs text-gray-500 uppercase tracking-wider">Active Thread</div>
          <div class="text-sm font-mono font-medium text-gray-200 truncate mt-1">{state.thread_id}</div>
        </div>
        <div>
          <div class="text-xs text-gray-500 uppercase tracking-wider">Repository Target</div>
          <div class="text-sm font-medium text-gray-200 mt-1">{state.repo_name}</div>
        </div>
        <div>
          <div class="text-xs text-gray-500 uppercase tracking-wider">Commit SHA</div>
          <div class="text-sm font-mono text-gray-400 mt-1">{state.commit_sha.substring(0, 7)}</div>
        </div>
        <div>
          <div class="text-xs text-gray-500 uppercase tracking-wider">System Pipeline Status</div>
          <span class={`inline-block text-xs px-2.5 py-0.5 rounded-md font-mono mt-1 ${getStatusColor(state.status)}`}>
            {state.status}
          </span>
        </div>
      </div>

      {/* Node Evaluations Outputs */}
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">🔍 Log Analysis Node</h3>
          {state.log_analysis?.status ? (
            <div class="space-y-2">
              <div class="text-sm">Status: <span class={state.log_analysis.status === 'PASS' ? 'text-emerald-400' : 'text-rose-400'}>{state.log_analysis.status}</span></div>
              <div class="text-xs text-gray-400">Warnings Detected: {state.log_analysis.warning_count}</div>
            </div>
          ) : <p class="text-xs text-gray-600 italic">Awaiting calculation...</p>}
        </div>

        <div class="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">⚖️ Compliance Audit Node</h3>
          {state.compliance_report?.compliant !== undefined ? (
            <div class="space-y-2">
              <div class="text-sm">Pass Threshold: <span class={state.compliance_report.compliant ? 'text-emerald-400' : 'text-rose-400'}>{state.compliance_report.compliant ? 'VALID' : 'INVALID'}</span></div>
              <div class="text-xs text-gray-400">Critical Vulnerabilities: {state.compliance_report.cve_critical_count}</div>
            </div>
          ) : <p class="text-xs text-gray-600 italic">Awaiting calculation...</p>}
        </div>

        <div class="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">🛡️ Risk Mitigation Evaluation</h3>
          {state.risk_assessment?.risk_score !== undefined ? (
            <div class="space-y-2">
              <div class="text-sm">Risk Metric: <span class={state.risk_assessment.risk_score > 60 ? 'text-rose-400' : 'text-emerald-400'}>{state.risk_assessment.risk_score}%</span></div>
              <div class="text-xs text-gray-400">Classification: {state.risk_assessment.risk_classification}</div>
            </div>
          ) : <p class="text-xs text-gray-600 italic">Awaiting calculation...</p>}
        </div>
      </div>

      {/* Critical Human-in-the-Loop Interruption Interaction Card */}
      {state.status === 'Reviewing' && (
        <div class="bg-purple-950/40 border border-purple-500/40 rounded-lg p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h2 class="text-base font-bold text-purple-300 flex items-center gap-2">
              ⚠️ LangGraph Checkpoint Invariant Execution Halt
            </h2>
            <p class="text-xs text-purple-400/80 mt-1 max-w-xl">
              The multi-agent graph completed core node analysis and executed its conditional interruption condition. State is currently locked in persistent memory. Manual action signatures required.
            </p>
          </div>
          <div class="flex gap-3 w-full md:w-auto">
            <button 
              onClick={() => onAction('reject')} 
              class="flex-1 md:flex-none px-4 py-2 bg-rose-700 hover:bg-rose-600 text-white text-xs font-semibold rounded tracking-wide transition-all"
            >
              Reject & Terminate
            </button>
            <button 
              onClick={() => onAction('approve')} 
              class="flex-1 md:flex-none px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded tracking-wide shadow-lg shadow-indigo-950 transition-all"
            >
              Approve & Deploy Canary
            </button>
          </div>
        </div>
      )}
    </div>
  );
}