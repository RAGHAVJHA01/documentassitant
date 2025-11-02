#!/usr/bin/env python3

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from pinecone import Pinecone
    from pinecone_plugins.assistant.models.chat import Message
    
    api_key = os.getenv("PINECONE_API_KEY")
    print(f"Testing streaming with API Key: {api_key[:10]}...")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    assistant = pc.assistant.Assistant(assistant_name="manulassistan")
    
    # Test streaming
    print("\n=== Testing Streaming Response ===")
    msg = Message(content="What are the safety features in TATA Nexon?")
    chunks = assistant.chat(messages=[msg], stream=True)
    
    print("Raw chunk data:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {type(chunk)} -> {repr(chunk)}")
        if i > 10:  # Limit output
            print("... (truncated)")
            break
    
    print("\n=== Testing Non-Streaming Response ===")
    resp = assistant.chat(messages=[msg])
    print(f"Response type: {type(resp)}")
    print(f"Response keys: {resp.keys() if isinstance(resp, dict) else 'Not a dict'}")
    if isinstance(resp, dict) and "message" in resp:
        print(f"Message content: {resp['message']['content'][:200]}...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()