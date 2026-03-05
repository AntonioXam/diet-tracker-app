#!/bin/bash

# Deploy script for Diet Tracker FIT
# This script helps deploy to Vercel with proper environment variables

set -e

echo "🚀 Diet Tracker FIT - Deploy Script"
echo "===================================="
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if logged in
echo "📝 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel..."
    vercel login
fi

echo ""
echo "📁 Project directory: $(pwd)"
echo ""

# Set environment variables
echo "🔧 Setting environment variables..."
echo ""

# SUPABASE_URL
echo "Setting SUPABASE_URL..."
vercel env add SUPABASE_URL https://kaomgwojvnncidyezdzj.supabase.co

# SUPABASE_ANON_KEY
echo "Setting SUPABASE_ANON_KEY..."
vercel env add SUPABASE_ANON_KEY eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthb21nd29qdm5uY2lkeWV6ZHpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI3MDcxNzYsImV4cCI6MjA4ODI4MzE3Nn0.Ds2ICxfiahuqt2n83dwoX9tMYGf7Xz8Jjvx6lFJc4zs

echo ""
echo "✅ Environment variables configured!"
echo ""

# Deploy
echo "🚀 Deploying to Vercel..."
echo ""

# Ask for deployment type
echo "Select deployment type:"
echo "1) Preview deployment"
echo "2) Production deployment"
read -p "Choose (1 or 2): " choice

if [ "$choice" = "2" ]; then
    echo "🌟 Deploying to PRODUCTION..."
    vercel --prod
else
    echo "🔍 Creating preview deployment..."
    vercel
fi

echo ""
echo "✅ Deploy complete!"
echo ""
echo "⚠️  REMEMBER:"
echo "   1. Update Google Analytics ID in frontend/index.html"
echo "   2. Update Sentry DSN in frontend/index.html"
echo "   3. Generate and upload favicon files"
echo "   4. Submit sitemap.xml to Google Search Console"
echo ""
echo "📊 Monitor your deployment at: https://vercel.com/dashboard"
echo ""
