#!/usr/bin/env python3

import requests
import json

def test_chat_functionality():
    """Test the FastAPI chat functionality"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing TATA Nexon Assistant Chat Functionality\n")
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        health_data = response.json()
        print(f"   ✅ Status: {health_data['status']}")
        print(f"   🤖 Assistant Available: {health_data['assistant_available']}")
        print(f"   📝 Message: {health_data.get('message', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Test 2: Non-streaming chat
    print("\n2️⃣ Testing Non-Streaming Chat...")
    try:
        chat_data = {
            "message": "What are the key safety features in TATA Nexon?",
            "stream": False
        }
        response = requests.post(f"{base_url}/chat", json=chat_data)
        chat_response = response.json()
        
        if chat_response.get('success'):
            print(f"   ✅ Success: True")
            print(f"   📝 Response: {chat_response['response'][:200]}...")
        else:
            print(f"   ❌ Failed: {chat_response.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Non-streaming chat failed: {e}")
    
    # Test 3: Streaming chat
    print("\n3️⃣ Testing Streaming Chat...")
    try:
        chat_data = {
            "message": "Tell me about TATA Nexon engine specifications",
            "stream": True
        }
        response = requests.post(f"{base_url}/chat/stream", json=chat_data, stream=True)
        
        if response.status_code == 200:
            print(f"   ✅ Streaming started successfully")
            print(f"   📡 Response chunks:")
            
            chunk_count = 0
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        try:
                            data = json.loads(line_text[6:])
                            content = data.get('content', '')
                            if content == '[DONE]':
                                print(f"\n   🏁 Stream completed ({chunk_count} chunks)")
                                break
                            elif content:
                                print(content, end='', flush=True)
                                chunk_count += 1
                                if chunk_count > 50:  # Limit output for testing
                                    print("... (truncated)")
                                    break
                        except json.JSONDecodeError:
                            pass
        else:
            print(f"   ❌ Streaming failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Streaming chat failed: {e}")
    
    # Test 4: Chat with history
    print("\n\n4️⃣ Testing Chat with History...")
    try:
        history_data = {
            "messages": [
                "Hello, I have a TATA Nexon",
                "What maintenance should I do at 20,000 km?"
            ],
            "stream": False
        }
        response = requests.post(f"{base_url}/chat/history", json=history_data)
        history_response = response.json()
        
        if history_response.get('success'):
            print(f"   ✅ Success: True")
            print(f"   📝 Response: {history_response['response'][:200]}...")
        else:
            print(f"   ❌ Failed: {history_response.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Chat with history failed: {e}")
    
    print("\n🎉 Testing Complete!")

if __name__ == "__main__":
    test_chat_functionality()