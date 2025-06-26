#!/bin/bash

# Exit on any error
set -e

# Function to check command existence
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

echo "🔍 Checking prerequisites..."

# Install kubectl if not installed
if ! command_exists kubectl; then
  echo "🔧 Installing kubectl..."
  curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x kubectl
  sudo mv kubectl /usr/local/bin/
else
  echo "✅ kubectl is already installed."
fi

# Install minikube if not installed
if ! command_exists minikube; then
  echo "🔧 Installing Minikube..."
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  rm minikube-linux-amd64
else
  echo "✅ Minikube is already installed."
fi

echo "🚀 Starting Minikube cluster..."
minikube start

echo "🔎 Verifying Kubernetes cluster info..."
kubectl cluster-info

echo "📦 Retrieving available pods in default namespace..."
kubectl get pods --namespace=default

echo "✅ Kubernetes cluster is up and running!"
