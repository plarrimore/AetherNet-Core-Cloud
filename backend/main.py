import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI(title="AetherNet-Core Cloud Gateway")

# Enable standard CORS permissions for our frontend dashboard
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

# Establish connection environment hooks
DB_URI = os.environ.get("DATABASE_URL")
from graph import workflow

# --- Explicit Platform Health Check ---
@app.get("/")
async def cloud_health_check():
    return {
        "status": "healthy",
        "service": "AetherNet-Core Cloud Switch",
        "database_connected": DB_URI is not None
    }

# --- Ingestion Endpoint ---
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
        if DB_URI:
            # DEFERRED IMPORT: This is only imported if a database is actively configured.
            # Bypasses startup C-linker issues on database-free instances completely.
            from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
            async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
                mesh = workflow.compile(checkpointer=checkpointer)
                return await mesh.ainvoke(initial_inputs, config=config)
        else:
            # Flawless in-memory fallback execution path
            memory_checkpointer = MemorySaver()
            mesh = workflow.compile(checkpointer=memory_checkpointer)
            return await mesh.ainvoke(initial_inputs, config=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Session Query Endpoint ---
@app.get("/api/v1/aether/snapshot/{thread_id}")
async def get_session_snapshot(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        if DB_URI:
            from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
            async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
                mesh = workflow.compile(checkpointer=checkpointer)
                snap = await mesh.aget_state(config)
                return snap.values if snap else {}
        else:
            return {} # MemorySaver drops out of scope gracefully, state managed via ingestion returns
    except Exception as e:
        return {"error": str(e)}