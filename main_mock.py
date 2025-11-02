import os
from dotenv import load_dotenv
import logging
import json

# Load environment variables
load_dotenv()

class PineconeAssistant:
    def __init__(self, assistant_name: str = "manulassistan"):
        """
        Initialize TATA Nexon Assistant with mock responses for deployment testing
        
        Args:
            assistant_name (str): Name of the assistant
        """
        self.assistant_name = assistant_name
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Mock TATA Nexon Assistant '{assistant_name}' initialized")
        
        # Mock responses for testing
        self.mock_responses = [
            "Hello! I'm your TATA Nexon expert assistant. I'm here to help you with everything about your SUV - from safety features to maintenance schedules, engine specifications, and troubleshooting. What would you like to know?",
            
            "The TATA Nexon has earned a 5-Star NCAP rating with comprehensive safety features including 6 airbags, ABS with EBD, Electronic Stability Control (ESC), Rear Parking Sensors, and much more. Would you like detailed information about any specific safety feature?",
            
            "TATA Nexon offers both petrol and diesel engine options. The 1.2L Revotron petrol engine delivers 120 PS power and 170 Nm torque, while the 1.5L Revotorq diesel engine provides 110 PS power and 260 Nm torque. Both engines come with manual and AMT transmission options.",
            
            "The recommended maintenance schedule for TATA Nexon includes service every 10,000 km or 12 months. Regular maintenance includes engine oil change, filter replacements, brake inspection, and comprehensive vehicle check-up. Following the schedule ensures optimal performance and warranty coverage."
        ]
    
    def get_assistant_info(self):
        """Get mock assistant information"""
        return {
            "name": self.assistant_name,
            "status": "active",
            "description": "Mock TATA Nexon Expert Assistant for deployment testing"
        }
    
    def send_message(self, message: str, stream: bool = False):
        """
        Send a message to the mock assistant
        
        Args:
            message (str): The user's message
            stream (bool): Whether to stream the response
            
        Returns:
            Generator or dict: Streaming response or direct response
        """
        try:
            # Enhanced message processing
            enhanced_message = self._enhance_user_message(message)
            
            if stream:
                self.logger.info(f"Sending streaming message: {message[:50]}...")
                return self._mock_stream_response(enhanced_message)
            else:
                self.logger.info(f"Sending message: {message[:50]}...")
                response = self._get_mock_response(enhanced_message)
                return {"content": response}
                
        except Exception as e:
            self.logger.error(f"Error in send_message: {e}")
            return {"error": str(e)}
    
    def _mock_stream_response(self, message: str):
        """Generate mock streaming response"""
        response_text = self._get_mock_response(message)
        
        # Simulate streaming by yielding chunks
        words = response_text.split()
        for i, word in enumerate(words):
            if i == 0:
                chunk_content = word
            else:
                chunk_content = " " + word
            
            # Mock the Pinecone streaming format
            mock_chunk = type('MockChunk', (), {
                'delta': type('MockDelta', (), {'content': chunk_content})()
            })()
            
            yield mock_chunk
        
        # End streaming
        yield type('MockChunk', (), {
            'delta': type('MockDelta', (), {'content': '[DONE]'})()
        })()
    
    def _get_mock_response(self, message: str) -> str:
        """Get appropriate mock response based on message content"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['safety', 'airbag', 'ncap', 'protection']):
            return self.mock_responses[1]
        elif any(word in message_lower for word in ['engine', 'petrol', 'diesel', 'performance', 'power']):
            return self.mock_responses[2]
        elif any(word in message_lower for word in ['maintenance', 'service', 'schedule', 'oil']):
            return self.mock_responses[3]
        elif any(word in message_lower for word in ['hello', 'hi', 'help', 'start']):
            return self.mock_responses[0]
        else:
            return f"Thank you for your question about '{message[:50]}...'. As your TATA Nexon expert, I'd be happy to help! This is a mock response for deployment testing. The full AI assistant will provide comprehensive, detailed answers about all aspects of your TATA Nexon SUV including specifications, features, maintenance, troubleshooting, and more."
    
    def _enhance_user_message(self, user_message: str) -> str:
        """Enhance user message with context (mock version)"""
        return f"TATA Nexon Query: {user_message}"
    
    def send_message_with_history(self, messages, stream: bool = False):
        """
        Send messages with conversation history (mock version)
        
        Args:
            messages: List of message strings or objects
            stream (bool): Whether to stream the response
            
        Returns:
            Generator or dict: Streaming response or direct response
        """
        try:
            # Use the last message for response
            last_message = messages[-1] if messages else "Hello"
            if isinstance(last_message, dict):
                last_message = last_message.get('content', 'Hello')
            
            return self.send_message(last_message, stream)
            
        except Exception as e:
            self.logger.error(f"Error in send_message_with_history: {e}")
            return {"error": str(e)}

# For backward compatibility
def create_assistant(assistant_name: str = "manulassistan"):
    """Create and return a PineconeAssistant instance"""
    return PineconeAssistant(assistant_name)