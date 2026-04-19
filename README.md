The frontend will be available at http://localhost:3000 and the backend API/WebSocket server at http://localhost:8000.

Manual Local Setup
1. Database Initialization

Bash
docker run --name dragchat-db -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=dragchat -p 5432:5432 -d postgres:15
2. Backend (FastAPI)

Bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
3. Frontend (Next.js)

Bash
cd frontend
npm install
npm run dev
🔌 WebSocket API
DragChat communicates via a structured JSON payload over WebSockets. Connect your client to ws://localhost:8000/ws/{client_id}.

Sending a Message
JSON
{
  "event": "message_send",
  "data": {
    "sender_id": "user_123",
    "content": "Hello, DragChat!",
    "timestamp": "2026-04-20T03:33:00Z"
  }
}
Receiving an AI Response
JSON
{
  "event": "agent_reply",
  "data": {
    "agent_name": "SupportBot",
    "content": "Hi there! How can I assist you today?",
    "latency_ms": 120
  }
}
🧑‍💻 Contributing
We welcome pull requests! Whether it's optimizing C++ logic for the AI parsing engine, enhancing the Tailwind components, or adding new database migrations, your contributions are appreciated.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

🛡️ License
Distributed under the MIT License. See LICENSE for more information.

Visit the Deepwiki Page for extended documentation and community plugins.
"""

with open('README-v2.md', 'w', encoding='utf-8') as f:
f.write(readme_v2_content)

print("Generated README-v2.md")

```python?code_reference&code_event_index=6
readme_content = """# DragChat 💬✨

[![DeepWiki Badge](https://deepwiki.com/badge-maker?url=https%3A%2F%2Fdeepwiki.com%2Fviwan-jain-21%2FDragChat)](https://deepwiki.com/viwan-jain-21/DragChat)
![Next.js](https://img.shields.io/badge/Next.js-14.x-black?logo=next.js)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?logo=tailwind-css)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

**DragChat** is a high-performance, real-time chat interface builder designed for seamless integration with local LLMs, Agentic AI systems, and modern web applications. Featuring a visually intuitive drag-and-drop builder, it bridges the gap between complex conversational logic and frontend execution.

---

## 🚀 Key Features

* **Real-Time Bidirectional Communication:** Built on robust WebSockets to handle instantaneous message delivery, typing indicators, and online status without polling overhead.
* **Modern Frontend Architecture:** A responsive, accessible interface constructed with Next.js and styled using Tailwind CSS, ensuring pixel-perfect adaptability across all device sizes.
* **Voice-Ready Integrations:** Native schema support for asynchronous audio streams, seamlessly linking up with speech-to-text (like faster-whisper) and text-to-speech (Deepgram API) pipelines.
* **Persistent & Scalable Data:** State and conversation history are managed efficiently and stored securely using a PostgreSQL backend.
* **Containerized Workflows:** Fully containerized utilizing Docker and Docker Compose, making local testing and production deployment of both the UI and backend proxy straightforward and reproducible.
* **Extensible AI Hooks:** Built-in webhooks specifically tailored for routing messages through local Large Language Models (e.g., Ollama) or complex Agentic logic controllers.

---

## 🛠️ Tech Stack Overview

### Frontend (Client Studio & Renderer)
* **Framework:** React / Next.js
* **Styling:** Tailwind CSS
* **State Management:** Zustand / React Context

### Backend (Logic & Real-Time Proxy)
* **API & WebSockets:** FastAPI (Python)
* **Database:** PostgreSQL
* **Infrastructure:** Docker, Docker Compose

---

## 💻 Getting Started

Follow these instructions to get a local development environment up and running.

### Prerequisites
* Docker & Docker Compose
* Node.js (v18+)
* Python 3.10+

### Installation

1. **Clone the repository:**
Spin up the backend services:
This will start the FastAPI backend and initialize the PostgreSQL database.

Bash
docker-compose up -d --build
Install frontend dependencies:

Bash
cd client
npm install
Start the Next.js development server:

Bash
npm run dev
Access the application:
Navigate to http://localhost:3000 in your browser. The FastAPI Swagger documentation is available at http://localhost:8000/docs.

🔌 WebSocket API Reference
DragChat relies on a structured JSON payload over WebSockets for real-time events.

Connection Endpoint
ws://localhost:8000/ws/chat/{client_id}

Message Payload Example
JSON
{
  "type": "chat_message",
  "payload": {
    "id": "msg_987654321",
    "sender": "user_123",
    "content": "Initialize the network diagnostic sequence.",
    "timestamp": "2026-04-20T03:33:00Z",
    "metadata": {
      "requires_llm": true,
      "voice_enabled": false
    }
  }
}
🧑‍💻 Contributing
We welcome pull requests! Whether it's optimizing algorithmic logic in the backend, refining the Tailwind styling, or expanding the LLM integration hooks, your contributions are valued.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

🛡️ License
Distributed under the MIT License. See LICENSE for more information.

Engineered with precision by viwan-jain-21
