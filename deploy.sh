#!/bin/bash

echo "🚀 Deploying TATA Nexon Assistant to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed. Installing..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "📋 Checking Vercel authentication..."
vercel whoami || vercel login

# Set environment variables
echo "🔑 Setting environment variables..."
echo "Enter your Pinecone API key:"
read -s PINECONE_API_KEY

vercel env add PINECONE_API_KEY production <<< "$PINECONE_API_KEY"

# Deploy to production
echo "🌐 Deploying to production..."
vercel --prod

echo "✅ Deployment complete!"
echo "📱 Your TATA Nexon Assistant is now live!"