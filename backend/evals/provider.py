import os
import sys
import json
import asyncio

# Dynamically adjust the system path to allow imports from the parent backend folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import app_graph

def call_api(prompt, options, context):
    """
    Synchronous provider bridge wrapper for Promptfoo.
    'prompt' represents the variable payload string injected from the test case vars matrix.
    """
    async def run_pipeline():
        config = {"configurable": {"thread_id": "eval-stress-thread"}}
        
        # Hydrate target state fields mirroring a real API ingestion hook
        initial_state = {
            "thread_id": "eval-stress-thread",
            "repo_name": "eval-governance-repo",
            "commit_sha": "e0ca43198083812839423b81123a1a1f010378ea",
            "build_logs": prompt,
            "system_logs": []
        }
        
        final_state = {}
        # Stream the graph step execution synchronously for the eval execution trace
        async for event in app_graph.astream(initial_state, config, stream_mode="values"):
            final_state = event
            
        return final_state

    # Orchestrate the asynchronous event loop safely within a synchronous runner execution call
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    result = loop.run_until_complete(run_pipeline())
    
    # Return stringified JSON schemas for Promptfoo's JavaScript assertion evaluation module to parse
    return {
        "output": json.dumps({
            "status": result.get("status"),
            "log_analysis": result.get("log_analysis", {}),
            "compliance_report": result.get("compliance_report", {}),
            "risk_assessment": result.get("risk_assessment", {})
        })
    }