from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

class ReleaseState(BaseModel):
    # Core Pipeline Metadata
    thread_id: str = Field(..., description="Unique deployment identifier")
    repo_name: str
    commit_sha: str
    
    # Analysis Metrics Collected by Agents
    build_logs: str
    log_analysis: Dict[str, Any] = Field(default_factory=dict)
    compliance_report: Dict[str, Any] = Field(default_factory=dict)
    risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    
    # Governance State
    status: Literal["Analyzing", "Reviewing", "Approved", "Rejected", "Deployed"] = "Analyzing"
    system_logs: List[str] = Field(default_factory=list)
    messages: List[Dict[str, str]] = Field(default_factory=list)
    
    # NEW: Telemetry performance tracking map per node execution trace
    telemetry: Dict[str, Dict[str, Any]] = Field(default_factory=dict)