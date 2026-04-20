from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from agent.graph import build_graph
from schemas import ProspectRequest, ReplyRequest
from services.llm import stream_llm
from db.models import SessionLocal, Prospect, Interaction
from db.init_db import init_db

app = FastAPI()
init_db()

graph = build_graph()

@app.post("/prospect")
async def generate_email(req: ProspectRequest):
    db = SessionLocal()

    prospect = Prospect(name=req.name, company=req.company)
    db.add(prospect)
    db.commit()
    db.refresh(prospect)

    state = {
        "name": req.name,
        "company": req.company,
        "reply": "",
        "history": []
    }

    result = await asyncio.to_thread(graph.invoke, state)

    interaction = Interaction(
        prospect_id=prospect.id,
        email=result.get("email"),
        reply="",
        response="",
    )
    db.add(interaction)
    db.commit()

    return {
        "email": result.get("email"),
        "enrichment": result.get("enrichment")
    }

@app.post("/prospect/stream")
async def stream_email(req: ProspectRequest):
    prompt = f"Write a cold email for {req.name} at {req.company}"

    def generator():
        for chunk in stream_llm(prompt):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")

@app.post("/reply")
async def handle_reply(req: ReplyRequest):
    db = SessionLocal()

    prospect = db.query(Prospect).filter_by(
        name=req.name, company=req.company
    ).first()

    history = db.query(Interaction).filter_by(
        prospect_id=prospect.id
    ).all()

    history_text = [
        f"Email: {h.email} | Reply: {h.reply} | Response: {h.response}"
        for h in history
    ]

    state = {
        "name": req.name,
        "company": req.company,
        "reply": req.reply,
        "history": [],
    }

    result = await asyncio.to_thread(graph.invoke, state)

    interaction = Interaction(
        prospect_id=prospect.id,
        email="",
        reply=req.reply,
        response=result.get("response"),
    )
    db.add(interaction)
    db.commit()


    return {
        "response": result.get("response"),
        "classification": result.get("classification"),
    }

