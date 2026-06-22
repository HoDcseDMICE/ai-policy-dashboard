#!/usr/bin/env bash
# deploy_render.sh
# Build Docker image, push to Docker Hub, and trigger a Render deploy.
# Requires environment variables: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, RENDER_SERVICE_ID, RENDER_API_KEY

set -euo pipefail

if [ -z "${DOCKERHUB_USERNAME:-}" ] || [ -z "${DOCKERHUB_TOKEN:-}" ] || [ -z "${RENDER_SERVICE_ID:-}" ] || [ -z "${RENDER_API_KEY:-}" ]; then
  echo "Missing required env vars. Set DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, RENDER_SERVICE_ID, RENDER_API_KEY"
  exit 1
fi

IMAGE_NAME="$DOCKERHUB_USERNAME/ai-policy-dashboard:latest"

echo "Building Docker image $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" .

echo "Logging in to Docker Hub..."
echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin

echo "Pushing image..."
docker push "$IMAGE_NAME"

echo "Triggering Render deploy for service $RENDER_SERVICE_ID..."
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"clearCache": true}')

if [ "$response" -ge 200 ] && [ "$response" -lt 300 ]; then
  echo "Render deploy triggered (HTTP $response)."
else
  echo "Render deploy request returned HTTP $response. Check API key and service ID."
  exit 1
fi

echo "Done."
