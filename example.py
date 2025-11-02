"""
Simple example of using the Pinecone Assistant
"""
from main import PineconeAssistant
import os

def simple_chat_example():
    """Simple chat example"""
    try:
        # Initialize assistant
        assistant = PineconeAssistant("manulassistan")
        
        # Simple question
        response = assistant.chat("What are the key safety features in a TATA Nexon?")
        content = assistant.get_response_content(response)
        print(f"Q: What are the key safety features in a TATA Nexon?")
        print(f"A: {content}")
        
    except Exception as e:
        print(f"Error: {e}")

def streaming_example():
    """Streaming response example"""
    try:
        assistant = PineconeAssistant("manulassistan")
        
        print("Q: Explain the maintenance schedule for TATA Nexon")
        print("A: ", end="")
        
        chunks = assistant.chat("Explain the maintenance schedule for TATA Nexon", stream=True)
        assistant.print_streaming_response(chunks)
        
    except Exception as e:
        print(f"Error: {e}")

def file_upload_example():
    """File upload example"""
    try:
        assistant = PineconeAssistant("manulassistan")
        
        pdf_path = r"c:\Application\Product-Manul\[TATA] NEXON Owners Manual.pdf"
        
        if os.path.exists(pdf_path):
            print("Uploading TATA Nexon manual...")
            response = assistant.upload_file(pdf_path)
            print("Upload successful!")
            
            # Ask a question about the uploaded file
            chat_response = assistant.chat("What is covered in this manual?")
            content = assistant.get_response_content(chat_response)
            print(f"Manual content summary: {content}")
        else:
            print("Manual file not found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Pinecone Assistant Examples ===\n")
    
    print("1. Simple Chat Example:")
    simple_chat_example()
    
    print("\n" + "="*50 + "\n")
    
    print("2. Streaming Example:")
    streaming_example()
    
    print("\n" + "="*50 + "\n")
    
    print("3. File Upload Example:")
    file_upload_example()