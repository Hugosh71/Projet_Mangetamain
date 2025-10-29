#!/bin/bash

# Build and push Docker image to ECR
# Make sure AWS CLI is configured first: aws configure

set -e

# Configuration
ECR_REGISTRY="815843283208.dkr.ecr.eu-west-3.amazonaws.com"
ECR_REPOSITORY="mangetamain"
AWS_REGION="eu-west-3"
IMAGE_NAME="mangetamain"
TAG="latest"

echo "Building and pushing Docker image to ECR"
echo "Registry: $ECR_REGISTRY"
echo "Repository: $ECR_REPOSITORY"
echo "Tag: $TAG"
echo ""

# Login to ECR
echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
# Build the Docker image
echo "Building Docker image..."
docker build --platform linux/amd64 -t $IMAGE_NAME:$TAG .

# Tag the image for ECR
ECR_IMAGE="$ECR_REGISTRY/$ECR_REPOSITORY:$TAG"
echo "Tagging image as $ECR_IMAGE..."
docker tag $IMAGE_NAME:$TAG $ECR_IMAGE

# Push the image to ECR
echo "Pushing image to ECR..."
docker push $ECR_IMAGE

echo ""
echo "Successfully built and pushed image to ECR!"
echo "Image URI: $ECR_IMAGE"
