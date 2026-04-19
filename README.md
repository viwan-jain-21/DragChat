<div align="center">

# 🎯 DragChat

### Intelligent PDF Question Answering with RAG

[![DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue?style=flat&logo=read-the-docs)](https://deepwiki.com/viwan-jain-21/DragChat)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.x-black?style=flat&logo=next.js)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)

**DragChat** is a powerful RAG (Retrieval-Augmented Generation) application that lets you chat with your PDF documents. Upload any PDF and ask questions — get accurate answers backed by direct citations from your document.

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Reference](#-api-reference) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

### 🧠 **Smart Document Understanding**
- **Intelligent Chunking**: Automatically splits PDFs into semantic chunks using sentence-level segmentation
- **Vector Embeddings**: Leverages `nomic-embed-text` for high-quality document embeddings
- **Contextual Retrieval**: Uses cosine similarity to find the most relevant passages for your questions

### 💬 **Conversational AI**
- **Powered by Llama 3.1**: State-of-the-art language model running locally via Ollama
- **Citation-Aware Responses**: Every answer includes page numbers from the source document
- **Context-Grounded**: Responses are strictly based on document content — no hallucinations

### 🎨 **Modern Tech Stack**
- **FastAPI Backend**: High-performance async Python API with automatic OpenAPI docs
- **Next.js Frontend**: Fast, responsive React-based UI with real-time updates
- **Local-First AI**: Runs entirely on your machine — your documents never leave your system

### 🔒 **Privacy & Control**
- **100% Local**: All processing happens on your machine
- **No Cloud Dependencies**: Works offline once models are downloaded
- **Your Data, Your Control**: Documents are processed in-memory and not stored

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Ollama** ([Install Guide](https://ollama.ai/))

### Installation

#### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/viwan-jain-21/DragChat.git
cd DragChat
```

#### 2️⃣ **Set Up Ollama Models**

Pull the required models:

```bash
# Download embedding model (~274MB)
ollama pull nomic-embed-text:latest

# Download LLM model (~4.7GB)
ollama pull llama3.1:latest
```

#### 3️⃣ **Backend Setup**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

#### 4️⃣ **Frontend Setup**

```bash
cd pdf-rag-frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐
│   Next.js UI    │  ← User uploads PDF & asks questions
└────────┬────────┘
         │
         ↓ HTTP
┌─────────────────┐
│  FastAPI Server │  ← Handles uploads & queries
└────────┬────────┘
         │
    ┌────┴─────┬──────────────┐
    ↓          ↓              ↓
┌────────┐ ┌──────┐  ┌──────────────┐
│ PyMuPDF│ │Spacy │  │    Ollama    │
│ (PDF)  │ │(NLP) │  │   (Models)   │
└────────┘ └──────┘  └──────────────┘
```

### Pipeline Flow

1. **Document Processing** (`/upload` endpoint)
   ```
   PDF Upload → Text Extraction → Sentence Chunking → Embedding → Vector Storage
   ```

2. **Question Answering** (`/chat` endpoint)
   ```
   User Query → Query Embedding → Similarity Search → Context Building → LLM Generation → Cited Response
   ```

### Tech Stack Details

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Next.js 14, React, Tailwind CSS | Modern, responsive UI |
| **Backend** | FastAPI, Python 3.10+ | High-performance async API |
| **PDF Processing** | PyMuPDF (fitz) | Extract text from PDFs |
| **NLP** | spaCy | Sentence segmentation |
| **Embeddings** | Ollama + nomic-embed-text | Convert text to vectors |
| **LLM** | Ollama + Llama 3.1 | Generate contextual answers |
| **Vector Operations** | PyTorch | Cosine similarity computation |

---

## 📡 API Reference

### Upload PDF

**Endpoint:** `POST /upload`

Upload a PDF document for processing.

**Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "message": "Successfully processed document.pdf into 87 chunks."
}
```

---

### Ask Question

**Endpoint:** `POST /chat`

Ask a question about the uploaded document.

**Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main findings?"}'
```

**Request Body:**
```json
{
  "query": "What is the conclusion of the research?"
}
```

**Response:**
```json
{
  "answer": "According to page 24, the research concludes that...",
  "citations": [24, 25, 26]
}
```

---

## 🛠️ Configuration

### Customizing Models

Edit the model names in `main.py`:

```python
EMBEDDING_MODEL_NAME = "nomic-embed-text:latest"
LLM_MODEL_NAME = "llama3.1:latest"
```

Other compatible Ollama models:
- **Embeddings:** `all-minilm`, `mxbai-embed-large`
- **LLMs:** `llama3.2`, `mistral`, `phi3`, `gemma2`

### Adjusting Chunk Size

In `main.py`, modify the chunking parameters:

```python
chunk_size = 10  # Number of sentences per chunk
```

### Top-K Results

Change the number of relevant chunks retrieved:

```python
top_k = min(5, len(pages_and_chunks))  # Retrieve top 5 chunks
```

---

## 📁 Project Structure

```
DragChat/
├── main.py                 # FastAPI backend server
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── pdf-rag-frontend/      # Next.js frontend application
    ├── src/
    │   ├── app/           # Next.js pages
    │   └── components/    # React components
    ├── public/            # Static assets
    ├── package.json       # Node.js dependencies
    └── next.config.js     # Next.js configuration
```

---

## 🔧 Development

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run with custom host/port
uvicorn main:app --host 0.0.0.0 --port 8080

# View API documentation
open http://localhost:8000/docs
```

### Frontend Development

```bash
cd pdf-rag-frontend

# Development mode
npm run dev

# Production build
npm run build
npm start

# Linting
npm run lint
```

---

## 🐛 Troubleshooting

### Ollama Connection Error

**Problem:** `Failed to connect to Ollama`

**Solution:**
```bash
# Start Ollama service
ollama serve

# Verify models are installed
ollama list
```

### Empty Response

**Problem:** `Please upload a PDF document first`

**Solution:** Ensure you've uploaded a PDF via `/upload` before using `/chat`

### Low-Quality Answers

**Problem:** Answers don't match document content

**Solutions:**
- Increase `top_k` value for more context
- Ensure PDF has extractable text (not scanned images)
- Try a different embedding model
- Adjust chunk size for better semantic boundaries

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/TypeScript
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

---

## 📋 Roadmap

- [ ] **Multi-Document Support** - Chat with multiple PDFs simultaneously
- [ ] **Conversation History** - Maintain context across multiple queries
- [ ] **Advanced Filters** - Filter by page range, keywords, sections
- [ ] **Export Functionality** - Save Q&A sessions as markdown/PDF
- [ ] **Docker Compose** - One-command deployment
- [ ] **Authentication** - User accounts and document management
- [ ] **Cloud Deployment** - Deploy to Vercel/Railway with hosted Ollama

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Ollama](https://ollama.ai/)** - Local LLM runtime
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Next.js](https://nextjs.org/)** - React framework
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** - PDF processing
- **[spaCy](https://spacy.io/)** - Industrial-strength NLP

---

## 📞 Support

- **Documentation:** [DeepWiki](https://deepwiki.com/viwan-jain-21/DragChat)
- **Issues:** [GitHub Issues](https://github.com/viwan-jain-21/DragChat/issues)
- **Discussions:** [GitHub Discussions](https://github.com/viwan-jain-21/DragChat/discussions)

---

<div align="center">

Made with ❤️ by [Viwan Jain](https://github.com/viwan-jain-21)

⭐ Star this repo if you find it helpful!

</div>
