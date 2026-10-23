from fastapi import FastAPI
from pydantic import BaseModel
import requests

app=FastAPI()
chat_history=[{
                "role":"system",
                "content":(
                        "You are a polite  customer service chatbot."
                "Help the customers with their orders, returns and payments and complaints." 
                "Keep your answers clear and simple and friendly."
                "Ask for more details to the customers if you are doubtful the on the customers question."
                "Remember details from earlier messages in this converstaion"
                )
}]


class ChatRequest(BaseModel):
    message:str

@app.get("/")
def home():
    return{"Message":"Customer AI chatbot is ruuning"}

@app.post("/chat")
def chat(request:ChatRequest):
    history=chat_history
    history.append({
        "role":"user",
        "content":request.message
    })

    response=requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model":"gemma4:e2b",
            "messages":history,
            "stream":False
            },
            timeout=120
    )
    response.raise_for_status()
    reply=response.json()["message"]["content"]
    
    history.append({
        "role":"assistant",
        "content":reply})

    return{
        "user_message":request.message,
        "reply":reply
    }