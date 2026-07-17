import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI(title="AetherNet-Core Cloud Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CallPayload(BaseModel):
    session_thread_id: str
    routing_source_phone: str
    raw_call_transcript: str

from graph import workflow

memory_checkpointer = MemorySaver()
mesh = workflow.compile(checkpointer=memory_checkpointer)

@app.get("/")
async def cloud_health_check():
    return {
        "status": "healthy",
        "service": "AetherNet-Core Engine Live",
        "mode": "stateless-in-memory-saver"
    }

@app.post("/api/v1/aether/ingest")
async def ingest_call_stream(payload: CallPayload):
    config = {"configurable": {"thread_id": payload.session_thread_id}}
    initial_inputs = {
        "raw_call_transcript": payload.raw_call_transcript, 
        "routing_source_phone": payload.routing_source_phone,
        "airlock_clearance": {}, 
        "raw_audio_packet_hex": "", 
        "extracted_telecom_metrics": {},
        "subscriber_profile": {}, 
        "routing_resolution_plan": {}, 
        "routing_status": "PENDING",
        "execution_node_trace": [], 
        "total_token_cost_usd": 0.0, 
        "token_usage_breakdown": {}
    }
    try:
        return await mesh.ainvoke(initial_inputs, config=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/aether/snapshot/{thread_id}")
async def get_session_snapshot(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        snap = await mesh.aget_state(config)
        return snap.values if snap else {}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Clean programmatic port binding: Looks up Railway/Docker dynamic assignments, falls back to 8000 locally
    assigned_port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=assigned_port, reload=True)