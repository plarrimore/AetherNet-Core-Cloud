import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

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

DB_URI = os.environ.get("DATABASE_URL")
from graph import workflow

@app.post("/api/v1/aether/ingest")
async def ingest_call_stream(payload: CallPayload):
    config = {"configurable": {"thread_id": payload.session_thread_id}}
    initial_inputs = {
        "raw_call_transcript": payload.raw_call_transcript, "routing_source_phone": payload.routing_source_phone,
        "airlock_clearance": {}, "raw_audio_packet_hex": "", "extracted_telecom_metrics": {},
        "subscriber_profile": {}, "routing_resolution_plan": {}, "routing_status": "PENDING",
        "execution_node_trace": [], "total_token_cost_usd": 0.0, "token_usage_breakdown": {}
    }
    
    # Adaptive Checkpointer Gating: Uses Postgres if available, falls back to Memory if free-hosting
    try:
        if DB_URI:
            async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
                mesh = workflow.compile(checkpointer=checkpointer)
                return await mesh.ainvoke(initial_inputs, config=config)
        else:
            memory_checkpointer = MemorySaver()
            mesh = workflow.compile(checkpointer=memory_checkpointer)
            return await mesh.ainvoke(initial_inputs, config=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/aether/snapshot/{thread_id}")
async def get_session_snapshot(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        if DB_URI:
            async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
                mesh = workflow.compile(checkpointer=checkpointer)
                snap = await mesh.aget_state(config)
                return snap.values if snap else {}
        else:
            return {} # MemorySaver drops out of scope on raw GET; snapshot visual updates driven via ingest returns
    except Exception as e:
        return {"error": str(e)}