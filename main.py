from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests, json, os
import fitz  # PyMuPDF

app = FastAPI()

CHAT_FILE = "chat_history.json"

all_chats = {}
current_chat_id = "default"

# Load chats
if os.path.exists(CHAT_FILE):
    try:
        with open(CHAT_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                all_chats = {"default": data}
            else:
                all_chats = data
    except:
        all_chats = {}

if "default" not in all_chats:
    all_chats["default"] = []

MAX_HISTORY = 6

def save_chat():
    with open(CHAT_FILE, "w") as f:
        json.dump(all_chats, f)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"

# ✅ MEMORY (knowledge.txt)
KNOWLEDGE = ""
if os.path.exists("knowledge.txt"):
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        KNOWLEDGE = f.read()

# ROUTES

@app.get("/chats")
def chats():
    return {"chats": list(all_chats.keys())}

@app.get("/history")
def history():
    return {"history": all_chats[current_chat_id]}

@app.post("/switch")
def switch(data: dict):
    global current_chat_id
    chat_id = data.get("chat_id")

    if chat_id not in all_chats:
        all_chats[chat_id] = []

    current_chat_id = chat_id
    return {"message": "switched"}

@app.post("/new")
def new_chat():
    global current_chat_id
    new_id = f"chat_{len(all_chats)+1}"
    all_chats[new_id] = []
    current_chat_id = new_id
    save_chat()
    return {"chat_id": new_id}

# ✅ DELETE CHAT
@app.post("/delete")
def delete_chat(data: dict):
    global current_chat_id
    chat_id = data.get("chat_id")

    if chat_id in all_chats:
        del all_chats[chat_id]

    # fallback to default
    if not all_chats:
        all_chats["default"] = []

    current_chat_id = list(all_chats.keys())[0]
    save_chat()

    return {"message": "deleted", "current": current_chat_id}

# FILE UPLOAD (simple text)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = await file.read()

    text = ""

    if filename.endswith(".pdf"):
        try:
            pdf = fitz.open(stream=content, filetype="pdf")
            for page in pdf:
                text += page.get_text()
        except:
            text = "Could not read PDF properly."
    else:
        try:
            text = content.decode("utf-8")
        except:
            text = str(content)

    return {"content": text[:3000]}

# CHAT

@app.post("/chat")
def chat(data: dict):
    user_prompt = data.get("prompt", "").strip()

    if not user_prompt:
        raise HTTPException(400, "No prompt")

    chat = all_chats[current_chat_id]

    chat.append(f"User: {user_prompt}")
    chat = chat[-MAX_HISTORY:]
    all_chats[current_chat_id] = chat
    save_chat()

    context = "\n".join(chat)

    prompt = f"""
You are Bruce, an AI assistant by Wayne AI Systems.

Knowledge:
{KNOWLEDGE[:1500]}

Conversation:
{context}

User: {user_prompt}
Bruce:
"""

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        data = resp.json()
        answer = data.get("response", "No response")

    except Exception as e:
        answer = f"Error: {str(e)}"

    chat.append(f"Bruce: {answer}")
    chat = chat[-MAX_HISTORY:]
    all_chats[current_chat_id] = chat
    save_chat()

    return {"response": answer}