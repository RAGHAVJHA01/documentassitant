#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from pinecone import Pinecone
    from pinecone_plugins.assistant.models.chat import Message
    
    api_key = os.getenv("PINECONE_API_KEY")
    print(f"API Key loaded: {api_key[:10]}..." if api_key else "No API key found")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    print("✓ Pinecone client initialized successfully")
    
    # Create assistant
    assistant = pc.assistant.Assistant(assistant_name="manulassistan")
    print("✓ Assistant created successfully")
    
    # Test a simple message
    msg = Message(content="Hello, how are you?")
    resp = assistant.chat(messages=[msg])
    
    print("✓ Chat test successful")
    print(f"Response: {resp['message']['content']}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if the API key is correct")
    print("2. Verify Pinecone account is active")
    print("3. Make sure the assistant name 'manulassistan' exists or can be created")