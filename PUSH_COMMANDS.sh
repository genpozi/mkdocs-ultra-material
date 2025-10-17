#!/bin/bash
# Commands to push MkDocs Ultra Material to GitHub

echo "=== MkDocs Ultra Material - Push to GitHub ==="
echo ""
echo "Step 1: Create GitHub Repository"
echo "--------------------------------"
echo "Go to: https://github.com/new"
echo ""
echo "Settings:"
echo "  - Repository name: mkdocs-ultra-material"
echo "  - Description: AI-Powered Documentation Generation for MkDocs"
echo "  - Public repository"
echo "  - DO NOT initialize with README, .gitignore, or license"
echo "  - Click 'Create repository'"
echo ""
echo "Press Enter when repository is created..."
read

echo ""
echo "Step 2: Add Remote and Push"
echo "----------------------------"

cd /workspaces/mkdocs-ultra-material

# Add remote
git remote add origin https://github.com/genpozi/mkdocs-ultra-material.git

# Verify remote
echo "Remote configured:"
git remote -v

echo ""
echo "Pushing to GitHub..."

# Push to GitHub
git push -u origin master

echo ""
echo "=== Push Complete! ==="
echo ""
echo "Your repository is now live at:"
echo "https://github.com/genpozi/mkdocs-ultra-material"
echo ""
echo "Next steps:"
echo "1. Configure repository settings (see GITHUB_SETUP.md)"
echo "2. Enable Issues and Discussions"
echo "3. Add topics: mkdocs, documentation, ai, llm, python"
echo "4. Create initial release (v0.2.0)"
echo ""
