import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from models import Hook, Order, create_db_and_tables, engine, insert_order_if_not_exists
from utils import fetch_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App startup")
    create_db_and_tables()
    insert_order_if_not_exists()
    yield
    print("App shutdown")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/hooks/")
def read_hooks(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[Hook]:
    hooks = session.exec(select(Hook).offset(offset).limit(limit)).all()
    return list(hooks)


@app.get("/hooks/{hook_id}")
def read_hook(hook_id: int, session: SessionDep) -> Hook:
    hook = session.get(Hook, hook_id)
    if not hook:
        raise HTTPException(status_code=404, detail="Hook not found")
    return hook


@app.post("/hooks/")
def create_hooks(hook: Hook, session: SessionDep) -> Hook:
    session.add(hook)
    session.commit()
    session.refresh(hook)
    return hook


@app.delete("/hooks/{hook_id}")
def delete_hero(hook_id: int, session: SessionDep):
    hook = session.get(Hook, hook_id)
    if not hook:
        raise HTTPException(status_code=404, detail="Hook not found")
    session.delete(hook)
    session.commit()
    return {"ok": True}


@app.get("/fake-event/{event_name}")
async def fake_event(event_name: str, session: SessionDep):
    filtered_hooks = list(
        session.exec(select(Hook).where(Hook.event == event_name)).all()
    )
    if len(filtered_hooks) == 0:
        raise HTTPException(status_code=404, detail="Hooks not found for the event")

    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, hook) for hook in filtered_hooks]
        results = await asyncio.gather(*tasks)

    return {"status": f"Trigger {len(filtered_hooks)} hooks.", "results": results}


@app.get("/orders/{order_id}")
def get_order(order_id: int, session: SessionDep) -> Order:
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
