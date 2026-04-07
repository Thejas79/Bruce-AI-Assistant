# 🦇 Bruce AI - The Local AI Assistant

> **"It's not who I am underneath, but what I do that defines me."**

**Bruce AI** is a fully local, zero-API-cost, ChatGPT-style AI assistant running directly on your machine. Featuring a Batman-inspired dark UI, voice input/output, document parsing, and persistent multi-chat sessions, it acts as your personal "Batcomputer".

---

## 🚀 Features

- **Multi-Chat System**: Create, switch, and delete multiple chats via a sleek sidebar navigation.
- **Persistent Memory**: Chat histories are stored locally (`chat_history.json`), maintaining conversation context across sessions and reboots. Keeps the last 6 messages for context.
- **File Handling**: Upload PDFs or text files. The system reads and converts PDFs (via PyMuPDF) to feed custom context directly into the AI.
- **Voice Capabilities**: 
  - 🎤 Speech-to-text (voice input via mic button).
  - 🔊 Text-to-speech (AI voice response with play/stop toggles per message).
- **Custom AI Persona**: Uses a `knowledge.txt` memory system injected into every prompt to control Bruce's behavior, tone, and system capabilities.
- **Batman Theme UI**: Clean, dark aesthetics, smooth chat bubbles, suggestion prompts, Enter-to-send support, and a "Bruce is thinking..." loading animation powered by "Wayne AI Systems".

---

## 🧱 Tech Stack

- **Frontend:** Vanilla HTML, CSS, JavaScript (No heavy frameworks!)
- **Backend:** Python & FastAPI
- **Local AI Engine:** Ollama running the `llama3:8b` model
- **PDF Processing:** PyMuPDF
- **Voice Interaction:** Web Speech API

---

## 🧠 How It Works Under The Hood

The architecture follows a straightforward, privacy-first flow: `Frontend ↔ FastAPI ↔ Ollama ↔ Response ↔ Frontend`

1. **User Request**: The user types a message, uploads a file, or uses voice input.
2. **Context Assembly**: The FastAPI backend receives the request and:
   - Fetches the current chat history for context.
   - Injects the `knowledge.txt` (static brain instructions).
   - Appends the newly uploaded file content and user prompt.
3. **Ollama Processing**: The complete system prompt is sent locally to the `llama3` model running via Ollama.
4. **Response**: The generated AI response is returned to the frontend, displayed beautifully in the UI, and optionally spoken aloud.

---

## ⚙️ Installation & Setup

### 1. Install & Run Ollama (The AI Engine)
Since Bruce AI runs entirely locally, you need Ollama to host the AI model without internet dependency.
1. Download Ollama from [ollama.com](https://ollama.com/) and install it.
2. Open your terminal/command prompt and pull the Llama 3 model:
   ```bash
   ollama run llama3:8b
   ```
   *(Note: The project uses `llama3:8b` for optimal logic and maintaining the Bruce persona.)*
3. Make sure the Ollama desktop app/service is running in the background.

### 2. Set Up the Backend (FastAPI)
1. Navigate to your project directory.
2. Create a virtual environment (optional but highly recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows PowerShell use: .\venv\Scripts\activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install fastapi uvicorn pymupdf pydantic
   ```
4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   The FastAPI backend should now be running securely (usually on `http://localhost:8000`).

### 3. Start the Frontend
Since it's built with Vanilla HTML/JS, you simply need to open the `index.html` file in your preferred web browser, or use a tool like VS Code Live Server to serve it. 

*(Make sure the fetch URLs in your JavaScript match the FastAPI server URL, which defaults to `http://127.0.0.1:8000`)*

---

## 📡 API Endpoints Overview

The FastAPI backend exposes the following core endpoints for the frontend to communicate with:
- `POST /chat` → Main AI interaction, sends prompts/file content to Ollama and retrieves the generated response.
- `GET /chats` → Retrieves the list of all saved chat channels.
- `GET /history` → Gets the message line history for the currently active chat channel.
- `POST /new` → Creates and initializes a fresh new chat session.
- `POST /switch` → Switches the active chatting context gracefully.
- `POST /stop` → Interrupts and terminates the current generation process.

---

## 🚧 Current Limitations & Next Steps

This project has actively moved past beginner level into a strong product-level AI architecture.

- **Streaming currently disabled**: Real-time response streaming (like ChatGPT) is temporarily disabled for stability due to JSON stream chunk parsing issues, falling back to full-response returns.
- **Future Roadmap**: 
  - Re-enable streaming (properly parsing Web-Streams).
  - Add AI logical tools (Search, system tools).
  - Advanced voice clones (Jarvis/Batman style Text-To-Speech).

---
*Wayne AI Systems*
