#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from pinecone import Pinecone
    from pinecone_plugins.assistant.models.chat import Message
    
    api_key = os.getenv("PINECONE_API_KEY")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    assistant = pc.assistant.Assistant(assistant_name="manulassistan")
    
    # Test non-streaming first
    print("=== Non-Streaming Test ===")
    msg = Message(content="What are the safety features in TATA Nexon?")
    resp = assistant.chat(messages=[msg])
    print(f"Response type: {type(resp)}")
    print(f"Has message attr: {hasattr(resp, 'message')}")
    if hasattr(resp, 'message'):
        print(f"Message type: {type(resp.message)}")
        print(f"Has content attr: {hasattr(resp.message, 'content')}")
        if hasattr(resp.message, 'content'):
            print(f"Content: {resp.message.content[:200]}...")
    
    print("\n=== Streaming Test ===")
    chunks = assistant.chat(messages=[msg], stream=True)
    
    full_response = ""
    chunk_count = 0
    for chunk in chunks:
        if chunk and hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content'):
            content = chunk.delta.content
            if content:
                full_response += content
                chunk_count += 1
    
    print(f"Processed {chunk_count} chunks")
    print(f"Full response: {full_response[:200]}...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()