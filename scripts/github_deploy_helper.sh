#!/usr/bin/env bash
# github_deploy_helper.sh
# Helper to push the current repo to GitHub, create a repo if needed, and set secrets for DockerHub and Render using the GitHub CLI (`gh`).
# Requires: git, gh (GitHub CLI) installed and authenticated.

set -euo pipefail

REPO_NAME=${1:-ai-policy-dashboard}
GH_ORG_OR_USER=${2:-}
DOCKERHUB_USER=${3:-}
RENDER_SERVICE_ID=${4:-}

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install from https://cli.github.com/ and authenticate with 'gh auth login'"
  exit 2
fi

# Create remote repo (under user if not provided)
if [ -n "$GH_ORG_OR_USER" ]; then
  gh repo create "$GH_ORG_OR_USER/$REPO_NAME" --public --confirm || true
  REMOTE="https://github.com/$GH_ORG_OR_USER/$REPO_NAME.git"
else
  gh repo create "$REPO_NAME" --public --confirm || true
  USERNAME=$(gh api user --jq '.login')
  REMOTE="https://github.com/$USERNAME/$REPO_NAME.git"
fi

# Push current branch
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE"
git push -u origin HEAD:main --force

# Set GitHub secrets (prompt for values if not provided)
if [ -n "$DOCKERHUB_USER" ]; then
  read -s -p "Docker Hub password/token: " DOCKERHUB_TOKEN
  echo
  gh secret set DOCKERHUB_USERNAME --body "$DOCKERHUB_USER"
  gh secret set DOCKERHUB_TOKEN --body "$DOCKERHUB_TOKEN"
fi

if [ -n "$RENDER_SERVICE_ID" ]; then
  read -s -p "Render API key: " RENDER_API_KEY
  echo
  gh secret set RENDER_SERVICE_ID --body "$RENDER_SERVICE_ID"
  gh secret set RENDER_API_KEY --body "$RENDER_API_KEY"
fi

echo "Repository pushed and secrets (if provided) set. Configure GitHub Actions if needed."