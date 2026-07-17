import os
import sys
from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langgraph.graph import StateGraph, END

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from airlock import TelecomAirlockGuard

airlock_guard = TelecomAirlockGuard()

class TelecomMetadataSchema(BaseModel):
    fraud_risk_index: float = Field(description="Decimal score from 0.0 to 1.0 evaluating fraud risk.")
    is_fraudulent: bool = Field(description="True if transcript represents active malicious phishing or scam behavior.")
    telecom_category: str = Field(description="Classification: e.g., SECURE, PHISHING, SPAM, TECHNICAL_SPOOF.")

class RoutingResolutionSchema(BaseModel):
    designated_route_path: str = Field(description="Action path: e.g., PERMIT_CONNECT, HARD_TERMINATE, ENFORCE_VOICEMAIL_TRAP.")
    latency_penalty_prediction_ms: int = Field(description="Connection latency penalty prediction in ms.")
    justification_rationale: str = Field(description="Technical reason for routing decision execution.")

class AetherNetState(TypedDict):
    raw_call_transcript: str
    routing_source_phone: str
    airlock_clearance: Dict[str, Any]
    raw_audio_packet_hex: str 
    extracted_telecom_metrics: Dict[str, Any]
    subscriber_profile: Dict[str, Any]
    routing_resolution_plan: Dict[str, Any]
    routing_status: str
    execution_node_trace: List[str]
    total_token_cost_usd: float
    token_usage_breakdown: Dict[str, Any]

def native_telecom_airlock_node(state: AetherNetState) -> AetherNetState:
    state["execution_node_trace"] = (state.get("execution_node_trace") or []) + ["TELECOM_AIRLOCK_GUARD"]
    verification = airlock_guard.verify_transaction(state["raw_call_transcript"], state["routing_source_phone"])
    state["airlock_clearance"] = verification
    
    if verification["is_compromised"]:
        state["routing_status"] = "HARD_BLOCKED_BY_AIRLOCK"
        state["execution_node_trace"].append("AIRLOCK_BLOCK_SHIELD_ACTIVATED")
        state["routing_resolution_plan"] = {
            "designated_route_path": "HARD_TERMINATE",
            "latency_penalty_prediction_ms": 0,
            "justification_rationale": f"Halted immediately by edge network airlock: {verification['reason']}"
        }
    return state

def airlock_routing_decision(state: AetherNetState) -> str:
    if state.get("airlock_clearance", {}).get("is_compromised", False):
        return "bypass_to_pruner"
    return "continue_to_extractor"

def cloud_metadata_extraction_node(state: AetherNetState) -> AetherNetState:
    state["execution_node_trace"] = state["execution_node_trace"] + ["CLOUD_OPENAI_EXTRACTOR"]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    structured_extractor = llm.with_structured_output(TelecomMetadataSchema)
    
    system_instruction = (
        "You are an expert telecom security parser. "
        "CRITICAL PRIORITY: If the caller transcript requests secure banking, credentials, limit details, or pin verifications, "
        "you MUST classify this attempt as fraudulent (is_fraudulent: True, fraud_risk_index: 0.95) "
        "regardless of how trusted the subscriber directory tier indicates."
    )
    prompt = f"Analyze call metrics.\nSource: {state['routing_source_phone']}\nTranscript:\n{state['raw_call_transcript']}"
    
    try:
        with get_openai_callback() as cb:
            metrics = structured_extractor.invoke([SystemMessage(content=system_instruction), HumanMessage(content=prompt)])
            state["extracted_telecom_metrics"] = metrics.model_dump() if hasattr(metrics, "model_dump") else metrics
            state["raw_audio_packet_hex"] = "RAW_GSM_64KBPS_STREAM_DUMP_0xFF8D1C"
            
            state["token_usage_breakdown"] = {"frontier_prompt_tokens": cb.prompt_tokens, "frontier_completion_tokens": cb.completion_tokens}
            state["total_token_cost_usd"] = (cb.prompt_tokens * 0.00000015) + (cb.completion_tokens * 0.00000060)
    except Exception:
        state["extracted_telecom_metrics"] = {"fraud_risk_index": 0.5, "is_fraudulent": False, "telecom_category": "SYSTEM_FALLBACK"}
    return state

def subscriber_history_node(state: AetherNetState) -> AetherNetState:
    state["execution_node_trace"] = state["execution_node_trace"] + ["SUBSCRIBER_REGISTRY_LOOKUP"]
    if state["routing_source_phone"] == "+15550199":
        state["subscriber_profile"] = {"phone_number": "+15550199", "subscriber_tier": "VIP_ENTERPRISE", "is_trusted": True}
    else:
        state["subscriber_profile"] = {"phone_number": state["routing_source_phone"], "subscriber_tier": "GUEST_ROUTING", "is_trusted": True}
    return state

def cloud_telecom_orchestrator_node(state: AetherNetState) -> AetherNetState:
    state["execution_node_trace"] = state["execution_node_trace"] + ["CLOUD_OPENAI_ORCHESTRATOR"]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    structured_orchestrator = llm.with_structured_output(RoutingResolutionSchema)
    
    system_instruction = (
        "Select the safest telecom route path. "
        "SPOOFING RULE: If metrics indicate 'is_fraudulent' is True or 'fraud_risk_index' > 0.7, "
        "assume the caller ID is spoofed. You are STRICTLY FORBIDDEN from choosing 'PERMIT_CONNECT'. "
        "Enforce 'HARD_TERMINATE' or 'ENFORCE_VOICEMAIL_TRAP' to protect the network infrastructure."
    )
    eval_context = f"Profile: {state['subscriber_profile']}\nMetrics: {state['extracted_telecom_metrics']}\nTranscript: {state['raw_call_transcript']}"
    
    try:
        with get_openai_callback() as cb:
            plan = structured_orchestrator.invoke([SystemMessage(content=system_instruction), HumanMessage(content=eval_context)])
            state["routing_resolution_plan"] = plan.model_dump() if hasattr(plan, "model_dump") else plan
            
            breakdown = state.get("token_usage_breakdown") or {}
            breakdown["frontier_prompt_tokens"] = breakdown.get("frontier_prompt_tokens", 0) + cb.prompt_tokens
            breakdown["frontier_completion_tokens"] = breakdown.get("frontier_completion_tokens", 0) + cb.completion_tokens
            state["token_usage_breakdown"] = breakdown
            state["total_token_cost_usd"] = state.get("total_token_cost_usd", 0.0) + ((cb.prompt_tokens * 0.00000015) + (cb.completion_tokens * 0.00000060))
    except Exception:
        state["routing_resolution_plan"] = {"designated_route_path": "REDIRECT_TO_IVR", "latency_penalty_prediction_ms": 100}
        
    state["routing_status"] = "ROUTE_RESOLVED"
    return state

def state_pruner_node(state: AetherNetState) -> AetherNetState:
    state["execution_node_trace"] = state["execution_node_trace"] + ["STATE_PRUNER_NODE"]
    state["raw_call_transcript"] = "[PRUNED_FOR_STORAGE_OPTIMIZATION]"
    state["raw_audio_packet_hex"] = "[PRUNED_FOR_STORAGE_OPTIMIZATION]"
    return state

workflow = StateGraph(AetherNetState)
workflow.add_node("airlock", native_telecom_airlock_node)
workflow.add_node("extractor", cloud_metadata_extraction_node)
workflow.add_node("history", subscriber_history_node)
workflow.add_node("orchestrator", cloud_telecom_orchestrator_node)
workflow.add_node("pruner", state_pruner_node)

workflow.set_entry_point("airlock")
workflow.add_conditional_edges("airlock", airlock_routing_decision, {"bypass_to_pruner": "pruner", "continue_to_extractor": "extractor"})
workflow.add_edge("extractor", "history")
workflow.add_edge("history", "orchestrator")
workflow.add_edge("orchestrator", "pruner")
workflow.add_edge("pruner", END)