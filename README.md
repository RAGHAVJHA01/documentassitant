# TATA Nexon AI Assistant

A sophisticated ChatGPT-like AI assistant specialized for TATA Nexon SUV owners, built with FastAPI and Pinecone Assistant API.

## Features

- 🚗 **Complete TATA Nexon Expertise**: Safety, maintenance, performance, and troubleshooting
- 🎨 **ChatGPT-like Interface**: Full-screen, responsive design with smooth scrolling
- ⚡ **Real-time Streaming**: Live response streaming for better user experience
- 🎯 **Smart Quick Questions**: Pre-defined expert questions with one-click access
- 📱 **Mobile Optimized**: Perfect experience on all device sizes
- 🎭 **Beautiful UI**: Gradient effects, animations, and modern styling
- 🔒 **Secure**: Environment-based API key management

## Technologies Used

- **Backend**: FastAPI, Pinecone Assistant API
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **AI**: Pinecone's Assistant with RAG capabilities
- **Deployment**: Vercel (Serverless)

## Local Development

### Prerequisites

- Python 3.8+
- Pinecone API key

### Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
PINECONE_API_KEY=your_pinecone_api_key_here
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8000`

### Project Structure

```
├── app.py              # FastAPI application
├── main.py             # Pinecone Assistant class
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── app.js      # Frontend JavaScript
├── templates/
│   └── index.html      # Main HTML template
└── uploads/            # Uploaded files directory
```

## API Endpoints

### Health Check
- `GET /health` - Check application health and assistant availability

### File Management
- `POST /upload` - Upload a file to the assistant
- `GET /files` - List uploaded files
- `DELETE /files/{filename}` - Delete a specific file

### Chat
- `POST /chat` - Send a message (non-streaming)
- `POST /chat/stream` - Send a message with streaming response
- `POST /chat/history` - Send multiple messages with history

### UI
- `GET /` - Main web interface

## Deployment to Vercel

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables
```bash
vercel env add PINECONE_API_KEY
```
Enter your Pinecone API key: `pcsk_mvCty_UAVDKVyUf53dtL7gZ3dgyLyXGjsMjpFHEuosuEg2BNnuwxcautPP9vZeFVjdnt8`

### 4. Deploy
```bash
vercel --prod
```

### Quick Deployment (Windows)
```bash
deploy.bat
```

### Quick Deployment (Linux/Mac)
```bash
chmod +x deploy.sh
./deploy.sh
```

### Alternative Deployment Methods

#### Using Vercel Web Interface
1. Fork this repository
2. Connect your GitHub account to Vercel
3. Import the project
4. Set the `PINECONE_API_KEY` environment variable
5. Deploy

#### Using GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## Usage

### 1. Upload Documents
- Click "Choose File" and select your TATA Nexon manual (PDF format recommended)
- Click "Upload" to process the document

### 2. Chat with Assistant
- Type questions about your vehicle in the chat input
- Use quick question buttons for common queries
- Toggle streaming mode for real-time responses

### 3. Sample Questions
- "What are the safety features in TATA Nexon?"
- "Tell me about the maintenance schedule"
- "What are the engine specifications?"
- "How do I troubleshoot common issues?"

## Configuration

### Environment Variables
- `PINECONE_API_KEY`: Your Pinecone API key (required)

### Customization
- Modify `templates/index.html` for UI changes
- Update `static/css/style.css` for styling
- Extend `app.py` for additional API endpoints
- Customize `main.py` for assistant behavior

## Security Notes

- Keep your Pinecone API key secure
- Use environment variables for sensitive data
- Consider implementing authentication for production use
- Validate file uploads and implement file size limits

## Troubleshooting

### Common Issues

1. **Assistant not available**: Check if Pinecone API key is set correctly
2. **File upload fails**: Ensure file format is supported and size is reasonable
3. **Chat not working**: Verify network connectivity and API status

### Logs
Check browser console and server logs for error messages.

## License

This project is for educational and demonstration purposes.

## Support

For issues and questions, please check the documentation or create an issue in the repository.