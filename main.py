import os
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import logging

# Load environment variables
load_dotenv()

class PineconeAssistant:
    def __init__(self, assistant_name: str = "manulassistan"):
        """
        Initialize Pinecone Assistant interface with enhanced prompting system
        
        Args:
            assistant_name (str): Name of the assistant
        """
        # Get API key from environment variable
        self.api_key = os.getenv("PINECONE_API_KEY")
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=self.api_key)
        
        # Initialize assistant
        self.assistant_name = assistant_name
        self.assistant = self.pc.assistant.Assistant(assistant_name=assistant_name)
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Enhanced prompt system
        self.system_prompt = self._create_system_prompt()
        
        self.logger.info(f"Pinecone Assistant '{assistant_name}' initialized successfully")

    def _create_system_prompt(self):
        """Create comprehensive system prompt for TATA Nexon expertise"""
        return """You are TATA Nexon Expert Assistant, a specialized AI assistant with comprehensive knowledge about the TATA Nexon compact SUV. Your role is to provide detailed, accurate, and helpful information about all aspects of the TATA Nexon vehicle.

## Your Expertise Areas:

### 1. SAFETY FEATURES & SYSTEMS
- 5-Star Global NCAP safety rating details
- Advanced safety technologies (ESC, ABS, EBD, Hill Hold, etc.)
- Airbag systems and passive safety features
- Child safety systems (ISOFIX, child locks)
- Structural safety and build quality
- Safety certifications and awards

### 2. ENGINE & PERFORMANCE
- Petrol Engine: 1.2L Turbo Revotron (120 PS, 170 Nm)
- Diesel Engine: 1.5L Revotorq (110 PS, 260 Nm)
- Transmission options (Manual, AMT)
- Performance metrics, acceleration, top speed
- Fuel efficiency ratings (ARAI certified)
- Engine technologies and innovations

### 3. MAINTENANCE & SERVICE
- Detailed service schedules and intervals
- Preventive maintenance guidelines
- Cost-effective maintenance tips
- Seasonal maintenance requirements
- Troubleshooting common issues
- Warranty information and coverage

### 4. FEATURES & TECHNOLOGY
- Infotainment system with 7-inch touchscreen
- ConnectNext by TATA Motors features
- Smartphone connectivity (Android Auto, Apple CarPlay)
- Audio system and entertainment options
- Climate control systems
- Interior and exterior features

### 5. VARIANTS & SPECIFICATIONS
- Different variant comparisons (XE, XM, XT, XZ, XZ+)
- Feature differences across variants
- Pricing and value propositions
- Color options and customization
- Accessory options

### 6. DRIVING EXPERIENCE
- Handling characteristics and driving dynamics
- Comfort features for city and highway driving
- Ground clearance and off-road capabilities
- Interior space and ergonomics
- Boot space and practicality

## Response Guidelines:

### Structure Your Responses:
1. **Quick Summary**: Provide immediate answer in 2-3 lines
2. **Detailed Explanation**: Comprehensive information with bullet points
3. **Practical Tips**: Real-world advice and recommendations
4. **Additional Context**: Related information that might be helpful

### Language Style:
- Use clear, non-technical language for general users
- Provide technical details when specifically requested
- Use bullet points for better readability
- Include specific numbers, measurements, and certifications
- Be conversational yet professional

### When Users Ask About:

**Safety**: Always mention the 5-Star NCAP rating first, then detail specific safety systems
**Maintenance**: Provide both scheduled maintenance and preventive care tips
**Performance**: Include both technical specifications and real-world driving experience
**Features**: Explain both what the feature does and how it benefits the user
**Problems**: Offer troubleshooting steps and when to consult service center
**Comparisons**: Provide balanced comparison with key differentiators

### Multilingual Support:
- Respond primarily in English unless user specifically requests another language
- Use simple, clear language that's easy to understand
- Explain technical terms when first mentioned

### Always Remember:
- You represent TATA Motors' commitment to customer service
- Prioritize customer safety and satisfaction
- Encourage users to consult authorized service centers for complex issues
- Provide accurate, up-to-date information based on official TATA documentation
- Be helpful, friendly, and solution-oriented

If you don't have specific information about a query, acknowledge it honestly and suggest contacting TATA Motors customer service or authorized dealers for the most current information."""

    def upload_file(self, file_path: str, timeout: int = None):
        """
        Upload a file to the assistant
        
        Args:
            file_path (str): Path to the file to upload
            timeout (int): Timeout for the upload operation
            
        Returns:
            dict: Response from the upload operation
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            self.logger.info(f"Uploading file: {file_path}")
            
            response = self.assistant.upload_file(
                file_path=file_path,
                timeout=timeout
            )
            
            self.logger.info("File uploaded successfully")
            return response
            
        except Exception as e:
            self.logger.error(f"Error uploading file: {str(e)}")
            raise

    def chat(self, message: str, stream: bool = False):
        """
        Chat with the assistant using enhanced prompting
        
        Args:
            message (str): Message to send to the assistant
            stream (bool): Whether to stream the response
            
        Returns:
            dict or generator: Response from the assistant
        """
        try:
            # Enhanced message with context and prompting
            enhanced_message = self._enhance_user_message(message)
            msg = Message(content=enhanced_message)
            
            if stream:
                self.logger.info(f"Sending streaming message: {message[:50]}...")
                chunks = self.assistant.chat(messages=[msg], stream=True)
                return chunks
            else:
                self.logger.info(f"Sending message: {message[:50]}...")
                resp = self.assistant.chat(messages=[msg])
                return resp
                
        except Exception as e:
            self.logger.error(f"Error in chat: {str(e)}")
            raise

    def _enhance_user_message(self, user_message: str):
        """
        Enhance user message with context and prompting for better responses
        
        Args:
            user_message (str): Original user message
            
        Returns:
            str: Enhanced message with context
        """
        # Analyze message type for better prompting
        message_lower = user_message.lower()
        
        # System context
        context = f"{self.system_prompt}\n\n"
        
        # Add specific context based on query type
        if any(word in message_lower for word in ["safety", "secure", "protection", "airbag"]):
            context += """
**CONTEXT**: User is asking about safety features. Focus on:
- 5-Star Global NCAP rating (highlight this first)
- Specific safety technologies and how they work
- Real-world safety benefits
- Comparison with competitors if relevant
"""
        
        elif any(word in message_lower for word in ["maintenance", "service", "schedule"]):
            context += """
**CONTEXT**: User is asking about maintenance. Provide:
- Specific service intervals with km/time periods
- Detailed maintenance checklist
- Cost-saving tips and preventive care
- Seasonal maintenance advice
"""
        
        elif any(word in message_lower for word in ["engine", "performance", "power", "specifications"]):
            context += """
**CONTEXT**: User is asking about engine/performance. Include:
- Detailed technical specifications
- Real-world performance figures
- Fuel efficiency data (ARAI certified)
- Driving experience insights
"""
        
        elif any(word in message_lower for word in ["features", "technology", "infotainment"]):
            context += """
**CONTEXT**: User is asking about features/technology. Cover:
- Detailed feature explanations
- How to use specific features
- Benefits and practical applications
- Connectivity and smart features
"""
        
        elif any(word in message_lower for word in ["problem", "issue", "trouble", "fix"]):
            context += """
**CONTEXT**: User has a problem/issue. Provide:
- Step-by-step troubleshooting guide
- When to consult service center
- Preventive measures
- Safety considerations
"""
        
        elif any(word in message_lower for word in ["compare", "vs", "difference", "better"]):
            context += """
**CONTEXT**: User wants comparison. Provide:
- Balanced comparison with key differentiators
- Strengths and unique selling points
- Value proposition analysis
- Recommendation based on use case
"""
        
        else:
            context += """
**CONTEXT**: General query about TATA Nexon. Provide comprehensive information with:
- Quick summary (2-3 lines)
- Detailed explanation with bullet points
- Practical tips and advice
- Additional helpful context
"""
        
        # Final enhanced message
        enhanced_message = f"{context}\n\n**USER QUESTION**: {user_message}\n\nPlease provide a detailed, structured response following the guidelines above."
        
        return enhanced_message

    def chat_with_history(self, messages: list, stream: bool = False):
        """
        Chat with the assistant using message history
        
        Args:
            messages (list): List of Message objects or strings
            stream (bool): Whether to stream the response
            
        Returns:
            dict or generator: Response from the assistant
        """
        try:
            # Convert strings to Message objects if needed
            message_objects = []
            for msg in messages:
                if isinstance(msg, str):
                    message_objects.append(Message(content=msg))
                else:
                    message_objects.append(msg)
            
            if stream:
                self.logger.info(f"Sending {len(message_objects)} messages (streaming)")
                chunks = self.assistant.chat(messages=message_objects, stream=True)
                return chunks
            else:
                self.logger.info(f"Sending {len(message_objects)} messages")
                resp = self.assistant.chat(messages=message_objects)
                return resp
                
        except Exception as e:
            self.logger.error(f"Error in chat with history: {str(e)}")
            raise

    def get_response_content(self, response):
        """
        Extract content from response
        
        Args:
            response: Response from chat operation
            
        Returns:
            str: Content of the response
        """
        try:
            if isinstance(response, dict) and "message" in response:
                return response["message"]["content"]
            elif hasattr(response, 'message') and hasattr(response.message, 'content'):
                return response.message.content
            return str(response)
        except Exception as e:
            self.logger.error(f"Error extracting response content: {str(e)}")
            return "Error extracting response content"

    def print_streaming_response(self, chunks):
        """
        Print streaming response chunks
        
        Args:
            chunks: Generator of response chunks
        """
        try:
            print("Assistant response:")
            for chunk in chunks:
                if chunk and hasattr(chunk, 'delta') and hasattr(chunk.delta, 'content'):
                    content = chunk.delta.content
                    if content:
                        print(content, end="", flush=True)
            print()  # New line at the end
        except Exception as e:
            self.logger.error(f"Error printing streaming response: {str(e)}")


def main():
    """
    Example usage of the Pinecone Assistant
    """
    try:
        # Initialize the assistant
        assistant = PineconeAssistant("manulassistan")
        
        # Upload the PDF file in the workspace
        pdf_path = r"c:\Application\Product-Manul\[TATA] NEXON Owners Manual.pdf"
        if os.path.exists(pdf_path):
            print("Uploading PDF file...")
            upload_response = assistant.upload_file(pdf_path)
            print(f"Upload response: {upload_response}")
        else:
            print("PDF file not found, skipping upload")
        
        # Example chat without streaming
        print("\n=== Non-streaming Chat ===")
        response = assistant.chat("How old is the earth?")
        content = assistant.get_response_content(response)
        print(f"Assistant: {content}")
        
        # Example chat with streaming
        print("\n=== Streaming Chat ===")
        chunks = assistant.chat("What is the manual about?", stream=True)
        assistant.print_streaming_response(chunks)
        
        # Example with message history
        print("\n=== Chat with History ===")
        messages = [
            "Hello, I have a TATA Nexon manual",
            "Can you help me understand the maintenance schedule?"
        ]
        response = assistant.chat_with_history(messages)
        content = assistant.get_response_content(response)
        print(f"Assistant: {content}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
