#!/bin/bash
# CHORUS Tutorial - Simple Setup Script
# Uses exact package versions from working environment

set -e  # Exit on error

ENV_NAME="chorus-tutorial"

echo "=========================================="
echo "CHORUS Tutorial - Simple Setup"
echo "=========================================="
echo ""

# Check if conda exists
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found"
    echo "Please install Miniconda from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "[1/5] Creating conda environment..."
conda create -n $ENV_NAME python=3.9 -y

echo ""
echo "[2/5] Installing packages (this may take 5-10 minutes)..."

# Get conda environment path
CONDA_PREFIX=$(conda run -n $ENV_NAME python -c "import sys; print(sys.prefix)")

echo "Environment path: $CONDA_PREFIX"

# Install packages using conda's pip
echo ""
echo "Installing core packages..."
conda run -n $ENV_NAME pip install -q pandas==2.2.1 numpy==1.26.4 scipy==1.11.2

echo "Installing FAISS and transformers..."
conda run -n $ENV_NAME pip install -q faiss-cpu==1.10.0 sentence-transformers==3.4.1

echo "Installing Gurobi..."
conda run -n $ENV_NAME pip install -q gurobipy==11.0.0

echo "Installing LangChain..."
conda run -n $ENV_NAME pip install -q langchain==0.3.20 langchain-community==0.3.19 langchain-core==0.3.43 langchain-huggingface==0.1.2

echo "Installing utilities..."
conda run -n $ENV_NAME pip install -q openai==1.72.0 python-dotenv==1.0.1 pymupdf==1.24.2 pydantic==2.10.6 tqdm==4.67.1

echo "Installing Jupyter..."
conda run -n $ENV_NAME pip install -q jupyter jupyterlab ipykernel ipywidgets

echo ""
echo "[3/5] Registering Jupyter kernel..."
conda run -n $ENV_NAME python -m ipykernel install --user --name $ENV_NAME --display-name "CHORUS Tutorial"

echo ""
echo "[4/5] Verifying installation..."
conda run -n $ENV_NAME python -c "import pandas; print('✓ pandas')"
conda run -n $ENV_NAME python -c "import numpy; print('✓ numpy')"
conda run -n $ENV_NAME python -c "import faiss; print('✓ faiss')"
conda run -n $ENV_NAME python -c "import sentence_transformers; print('✓ sentence-transformers')"
conda run -n $ENV_NAME python -c "import gurobipy; print('✓ gurobipy')"
conda run -n $ENV_NAME python -c "import langchain; print('✓ langchain')"
conda run -n $ENV_NAME python -c "import jupyter; print('✓ jupyter')"

echo ""
echo "[5/5] Setup complete!"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Activate environment:"
echo "   conda activate $ENV_NAME"
echo ""
echo "2. Configure API keys:"
echo "   cp .env.example .env"
echo "   nano .env  # Add your OpenRouter API key"
echo ""
echo "3. Activate Gurobi license:"
echo "   grbgetkey YOUR-LICENSE-KEY"
echo ""
echo "4. Start Jupyter:"
echo "   jupyter lab"
echo ""
echo "5. In Jupyter, select kernel: 'CHORUS Tutorial'"
echo ""
echo "=========================================="
