from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import asyncio
from typing import List, Optional
from pydantic import BaseModel
import aiofiles
from main_mock import PineconeAssistant
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Pinecone Assistant API",
    description="AI-powered assistant for document analysis and Q&A",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global assistant instance
assistant = None

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    stream: Optional[bool] = False

class ChatHistory(BaseModel):
    messages: List[str]
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

class UploadResponse(BaseModel):
    filename: str
    success: bool
    message: str
    error: Optional[str] = None

# Initialize assistant on startup
def initialize_assistant():
    global assistant
    try:
        assistant = PineconeAssistant("manulassistan")
        logger.info("Pinecone Assistant initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Pinecone Assistant: {e}")
        assistant = None

@app.on_event("startup")
async def startup_event():
    initialize_assistant()

# Root endpoint - serve the main UI
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check endpoint
@app.get("/health")
async def health_check():
    assistant_status = assistant is not None
    return {
        "status": "healthy" if assistant_status else "degraded",
        "assistant_available": assistant_status,
        "message": "Assistant ready" if assistant_status else "Assistant initialization failed - check API key"
    }

# Upload file endpoint
@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not assistant:
        raise HTTPException(status_code=503, detail="Assistant not available")
    
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join(upload_dir, file.filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Upload to Pinecone
        upload_response = assistant.upload_file(file_path)
        
        return UploadResponse(
            filename=file.filename,
            success=True,
            message="File uploaded and processed successfully"
        )
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return UploadResponse(
            filename=file.filename,
            success=False,
            message="Upload failed",
            error=str(e)
        )

# Chat endpoint (non-streaming)
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    if not assistant:
        raise HTTPException(status_code=503, detail="Assistant not available")
    
    try:
        response = assistant.chat(chat_message.message, stream=False)
        content = assistant.get_response_content(response)
        
        return ChatResponse(
            response=content,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )

# Streaming chat endpoint
@app.post("/chat/stream")
async def chat_stream(chat_message: ChatMessage):
    if not assistant:
        raise HTTPException(status_code=503, detail="Assistant not available")
    
    try:
        async def generate():
            chunks = assistant.chat(chat_message.message, stream=True)
            for chunk in chunks:
                if chunk and hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content'):
                    content = chunk.delta.content
                    if content:
                        yield f"data: {json.dumps({'content': content})}\n\n"
            yield f"data: {json.dumps({'content': '[DONE]'})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
        
    except Exception as e:
        logger.error(f"Error in streaming chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Chat with history endpoint
@app.post("/chat/history", response_model=ChatResponse)
async def chat_with_history(chat_history: ChatHistory):
    if not assistant:
        raise HTTPException(status_code=503, detail="Assistant not available")
    
    try:
        response = assistant.chat_with_history(chat_history.messages, stream=False)
        content = assistant.get_response_content(response)
        
        return ChatResponse(
            response=content,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error in chat with history: {e}")
        return ChatResponse(
            response="",
            success=False,
            error=str(e)
        )

# Get uploaded files list
@app.get("/files")
async def list_files():
    try:
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            return {"files": []}
        
        files = []
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    "name": filename,
                    "size": stat.st_size,
                    "modified": stat.st_mtime
                })
        
        return {"files": files}
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return {"files": [], "error": str(e)}

# Delete file endpoint
@app.delete("/files/{filename}")
async def delete_file(filename: str):
    try:
        file_path = os.path.join("uploads", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"success": True, "message": f"File {filename} deleted"}
        else:
            return {"success": False, "message": "File not found"}
            
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)