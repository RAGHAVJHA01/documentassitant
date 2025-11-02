#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from main import PineconeAssistant

# Load environment variables
load_dotenv()

def test_enhanced_prompting():
    """Test the enhanced prompting system with different query types"""
    
    print("🚗 Testing TATA Nexon Enhanced Assistant with Detailed Prompting\n")
    
    try:
        # Initialize assistant
        assistant = PineconeAssistant("manulassistan")
        print("✅ Assistant initialized successfully\n")
        
        # Test different types of queries
        test_queries = [
            {
                "type": "Safety Query", 
                "question": "What safety features does TATA Nexon have?",
                "description": "Testing safety-focused prompting"
            },
            {
                "type": "Maintenance Query",
                "question": "What is the maintenance schedule?", 
                "description": "Testing maintenance-focused prompting"
            },
            {
                "type": "Engine/Performance Query",
                "question": "Tell me about engine specifications and performance",
                "description": "Testing engine-focused prompting"
            },
            {
                "type": "Feature/Technology Query", 
                "question": "How does the infotainment system work?",
                "description": "Testing feature-focused prompting"
            },
            {
                "type": "Troubleshooting Query",
                "question": "My car is making strange noises, help me troubleshoot",
                "description": "Testing problem-solving prompting"
            },
            {
                "type": "Comparison Query",
                "question": "Compare petrol vs diesel variants",
                "description": "Testing comparison-focused prompting"
            }
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"{i}️⃣ {query['type']}: {query['description']}")
            print(f"Question: \"{query['question']}\"")
            print("Response preview:")
            
            try:
                # Test non-streaming response
                response = assistant.chat(query['question'], stream=False)
                content = assistant.get_response_content(response)
                
                # Show first 300 characters of response
                preview = content[:300] + "..." if len(content) > 300 else content
                print(f"📝 {preview}\n")
                
                # Show enhanced message (for debugging)
                enhanced_message = assistant._enhance_user_message(query['question'])
                enhanced_preview = enhanced_message[:200] + "..." if len(enhanced_message) > 200 else enhanced_message
                print(f"🔍 Enhanced Prompt Preview: {enhanced_preview}\n")
                
            except Exception as e:
                print(f"❌ Error: {e}\n")
            
            print("-" * 80 + "\n")
        
        # Test streaming with one detailed query
        print("🎬 Testing Streaming Response:")
        streaming_query = "Give me detailed information about TATA Nexon's 5-Star safety rating and all safety features"
        print(f"Question: \"{streaming_query}\"")
        print("Streaming Response:")
        
        try:
            chunks = assistant.chat(streaming_query, stream=True)
            assistant.print_streaming_response(chunks)
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            
    except Exception as e:
        print(f"❌ Initialization error: {e}")

if __name__ == "__main__":
    test_enhanced_prompting()