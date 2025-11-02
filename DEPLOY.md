# Quick Vercel Deployment Guide

## Option 1: One-Click Deploy (Easiest)

1. **Fork this repository** to your GitHub account
2. **Go to [Vercel](https://vercel.com/)**
3. **Click "New Project"**
4. **Import your forked repository**
5. **Add Environment Variable:**
   - Name: `PINECONE_API_KEY`
   - Value: `pcsk_mvCty_UAVDKVyUf53dtL7gZ3dgyLyXGjsMjpFHEuosuEg2BNnuwxcautPP9vZeFVjdnt8`
6. **Click "Deploy"**

## Option 2: Command Line (Advanced)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

4. **Set Environment Variable:**
   ```bash
   vercel env add PINECONE_API_KEY
   # Enter: pcsk_mvCty_UAVDKVyUf53dtL7gZ3dgyLyXGjsMjpFHEuosuEg2BNnuwxcautPP9vZeFVjdnt8
   ```

## Option 3: Windows Batch Script

Simply run:
```cmd
deploy.bat
```

## What happens after deployment:

✅ **Full-screen ChatGPT-like interface**  
✅ **Real-time streaming responses**  
✅ **Mobile-optimized design**  
✅ **Expert TATA Nexon knowledge**  
✅ **Smooth scrolling for long answers**  

Your assistant will be available at: `https://your-project-name.vercel.app`

## Troubleshooting

- **Build fails**: Check that all files are committed to git
- **API errors**: Verify the Pinecone API key is set correctly
- **UI issues**: Clear browser cache and refresh

## Post-Deployment

1. Test the chat interface
2. Try the quick questions
3. Verify streaming responses work
4. Test on mobile devices

Your TATA Nexon AI Assistant is ready to help users with comprehensive vehicle information!