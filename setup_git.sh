#!/bin/bash

# Setup script for initializing Git repository and connecting to remote

set -e

echo "🚀 Reddit Scraper Actor - Git Setup"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git repository not initialized. Run 'git init' first."
    exit 1
fi

# Get repository name
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your repository name (default: reddit-scraper-actor): " REPO_NAME
REPO_NAME=${REPO_NAME:-reddit-scraper-actor}

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "⚠️  Remote 'origin' already exists."
    read -p "Do you want to update it? (y/n): " UPDATE_REMOTE
    if [ "$UPDATE_REMOTE" = "y" ]; then
        git remote set-url origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
        echo "✅ Updated remote origin"
    fi
else
    git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
    echo "✅ Added remote origin"
fi

# Set default branch to main
git branch -M main 2>/dev/null || echo "Branch already set to main"

echo ""
echo "📋 Next steps:"
echo "1. Create the repository on GitHub: https://github.com/new"
echo "   - Name: ${REPO_NAME}"
echo "   - Don't initialize with README, .gitignore, or license"
echo ""
echo "2. Add and commit your files:"
echo "   git add ."
echo "   git commit -m 'Initial commit: Reddit scraper actor with CI/CD'"
echo ""
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "4. Set up GitHub Secrets (see SECRETS_SETUP.md):"
echo "   - DOCKER_USERNAME"
echo "   - DOCKER_PASSWORD"
echo ""
echo "✅ Git setup complete!"

