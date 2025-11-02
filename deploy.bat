@echo off
echo 🚀 Deploying TATA Nexon Assistant to Vercel...

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI is not installed. Installing...
    npm install -g vercel
)

REM Login to Vercel (if not already logged in)
echo 📋 Checking Vercel authentication...
vercel whoami || vercel login

REM Set environment variables
echo 🔑 Setting environment variables...
set /p PINECONE_API_KEY="Enter your Pinecone API key: "

echo %PINECONE_API_KEY% | vercel env add PINECONE_API_KEY production

REM Deploy to production
echo 🌐 Deploying to production...
vercel --prod

echo ✅ Deployment complete!
echo 📱 Your TATA Nexon Assistant is now live!