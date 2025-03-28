from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class WebhookData(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, index=True)
    payload = Column(String)
Base.metadata.create_all(bind=engine)
app = FastAPI()
class WebhookRequest(BaseModel):
    event: str
    payload: str
@app.post("/webhook")
def receive_webhook(webhook: WebhookRequest):
    db = SessionLocal()
    new_webhook = WebhookData(event=webhook.event, payload=webhook.payload)
    db.add(new_webhook)
    db.commit()
    db.refresh(new_webhook)
    db.close()
    return {"message": "Webhook received", "id": new_webhook.id}
@app.get("/webhooks")
def get_webhooks():
    db = SessionLocal()
    webhooks = db.query(WebhookData).all()
    db.close()
    return webhooks
#запуск uvicorn fastAPI:app --reload
