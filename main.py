import os
import fitz  # PyMuPDF
import re
import spacy
import torch
import torch.nn.functional as F
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import OllamaEmbeddings, OllamaLLM

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Spacy for sentence chunking (like in the notebook)
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

# Explicitly specifying the Ollama models
EMBEDDING_MODEL_NAME = "nomic-embed-text:latest"
LLM_MODEL_NAME = "llama3.1:latest"

embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
llm = OllamaLLM(model=LLM_MODEL_NAME)

# In-memory "Vector DB" using notebook's approach
pages_and_chunks = []
embeddings_tensor = None

def text_formatter(text: str) -> str:
    """Performs minor formatting on extracted text."""
    return text.replace("\n", " ").strip()


class ChatRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global pages_and_chunks, embeddings_tensor
    
    # 1. Check file size
    content = await file.read()
    print(f"--- DEBUG: Uploaded file size: {len(content)} bytes ---")
    
    temp_pdf_path = f"temp_{file.filename}"
    with open(temp_pdf_path, "wb") as f:
        f.write(content)
        
    doc = fitz.open(temp_pdf_path)
    pages_and_texts = []
    
    # Read PDF text
    for page_number, page in enumerate(doc):
        text = text_formatter(page.get_text())
        if not text:
            continue
        pages_and_texts.append({
            "page_number": page_number + 1,
            "text": text
        })
        
    # 2. Check how many pages had extractable text
    print(f"--- DEBUG: Extracted text from {len(pages_and_texts)} pages ---")
        
    for item in pages_and_texts:
        doc_spacy = nlp(item["text"])
        sentences = [sent.text.strip() for sent in doc_spacy.sents if sent.text.strip()]
        
        chunk_size = 10
        chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]
        item["sentence_chunks"] = chunks
        
    pages_and_chunks = []
    for item in pages_and_texts:
        for chunk in item["sentence_chunks"]:
            joined_chunk = " ".join(chunk).strip()
            joined_chunk = re.sub(r'\s+', ' ', joined_chunk)
            joined_chunk = re.sub(r'\.([A-Z])', r'. \1', joined_chunk)
            
            # Skip chunks with very few words
            if len(joined_chunk.split()) < 10:
                continue
                
            pages_and_chunks.append({
                "page_number": item["page_number"],
                "sentence_chunk": joined_chunk
            })
            
    # 3. Check how many chunks survived the filtering
    print(f"--- DEBUG: Created {len(pages_and_chunks)} final chunks ---")
            
    if len(pages_and_chunks) > 0:
        texts = [item["sentence_chunk"] for item in pages_and_chunks]
        embeddings_list = embedding_model.embed_documents(texts)
        embeddings_tensor = torch.tensor(embeddings_list, dtype=torch.float32)
    else:
        print("--- DEBUG: Skipping embedding because chunks list is empty ---")
    
    doc.close() 
    os.remove(temp_pdf_path)
    return {"message": f"Successfully processed {file.filename} into {len(pages_and_chunks)} chunks."}

@app.post("/chat")
async def chat(request: ChatRequest):
    global pages_and_chunks, embeddings_tensor
    if embeddings_tensor is None:
        return {"answer": "Please upload a PDF document first.", "citations": []}
        
    # Embed the incoming query
    query_emb = embedding_model.embed_query(request.query)
    query_tensor = torch.tensor(query_emb, dtype=torch.float32).unsqueeze(0)
    
    # Normalize for cosine similarity
    query_norm = F.normalize(query_tensor, p=2, dim=1)
    embeddings_norm = F.normalize(embeddings_tensor, p=2, dim=1)
    
    # Calculate similarity scores
    cosine_scores = torch.matmul(query_norm, embeddings_norm.T)[0]
    top_k = min(5, len(pages_and_chunks))
    top_results = torch.topk(cosine_scores, k=top_k)
    
    # Prepare context and retrieve relevant chunks
    context_items = [pages_and_chunks[i] for i in top_results.indices]
    context = "\n\n".join([f"- {item['sentence_chunk']} (Page {item['page_number']})" for item in context_items])
    
    prompt = f"""You are a helpful expert. 

Use ONLY the context below to answer the question. Be explanatory and precise. 
If you use information from the context, always cite the exact page number(s) in your answer (e.g., "according to page 4...").

Context:
{context}

Question:
{request.query}

Answer:"""

    # Query Ollama
    answer = llm.invoke(prompt)
    
    # Extract unique citation pages for the frontend metadata
    citations = list(set([item["page_number"] for item in context_items]))
    
    return {"answer": answer, "citations": citations}