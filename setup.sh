#!/bin/bash

# Name of the Conda environment
ENV_NAME="my_project_env"

echo "🚀 Setting up the Conda environment: $ENV_NAME..."

# Step 1: Check if Conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

# Step 2: Create the Conda environment
if conda env list | grep -q "$ENV_NAME"; then
    echo "✅ Conda environment '$ENV_NAME' already exists."
else
    echo "🔧 Creating new Conda environment..."
    conda create -y --name $ENV_NAME python=3.10
fi

# Step 3: Activate the environment
echo "🔄 Activating the environment..."
eval "$(conda shell.bash hook)"  # Ensure Conda is properly loaded
conda activate $ENV_NAME

# Step 4: Install dependencies
echo "📦 Installing dependencies..."
conda install -y numpy pandas matplotlib pyyaml requests scikit-learn
pip install some-package-from-pypi  # Add any pip-only dependencies

echo "🎉 Setup complete! To start using the environment, run:"
echo "   conda activate $ENV_NAME"
