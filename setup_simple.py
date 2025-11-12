#!/usr/bin/env python3
"""
Simple Environment Setup for CHORUS Tutorial
Uses exact package versions from working 'pt' environment
"""

import subprocess
import sys

ENV_NAME = "chorus-tutorial"

# Exact versions from working 'pt' environment
PACKAGES = {
    # Core packages (via pip to avoid conflicts)
    "pip": [
        "pandas==2.2.1",
        "numpy==1.26.4",
        "scipy==1.11.2",
        "tqdm==4.67.1",

        # Scientific computing
        "faiss-cpu==1.10.0",
        "sentence-transformers==3.4.1",

        # Gurobi
        "gurobipy==11.0.0",

        # LLM and RAG
        "openai==1.72.0",
        "python-dotenv==1.0.1",
        "langchain==0.3.20",
        "langchain-community==0.3.19",
        "langchain-core==0.3.43",
        "langchain-huggingface==0.1.2",

        # PDF processing
        "pymupdf==1.24.2",

        # Validation
        "pydantic==2.10.6",

        # Jupyter
        "jupyter",
        "jupyterlab",
        "ipykernel",
    ]
}

def run(cmd):
    """Run command and return success status."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("=" * 70)
    print("CHORUS Tutorial - Simple Environment Setup")
    print("=" * 70)
    print(f"\nCreating environment: {ENV_NAME}")
    print("This will take 5-10 minutes...\n")

    # Step 1: Create conda environment with Python 3.9
    print("[1/4] Creating conda environment...")
    if not run(f"conda create -n {ENV_NAME} python=3.9 -y"):
        print("Failed to create environment")
        return 1

    # Step 2: Get conda prefix
    result = subprocess.run(
        f"conda env list | grep {ENV_NAME}",
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Failed to find environment")
        return 1

    # Extract environment path
    env_path = None
    for line in result.stdout.split('\n'):
        if ENV_NAME in line:
            parts = line.split()
            env_path = parts[-1]
            break

    if not env_path:
        print("Could not determine environment path")
        return 1

    # Step 3: Install packages via pip
    pip_cmd = f"{env_path}/bin/pip"

    print(f"\n[2/4] Installing packages...")
    for package in PACKAGES["pip"]:
        print(f"  Installing {package}...")
        if not run(f'{pip_cmd} install "{package}"'):
            print(f"Warning: Failed to install {package}")

    # Step 4: Register Jupyter kernel
    print(f"\n[3/4] Registering Jupyter kernel...")
    python_cmd = f"{env_path}/bin/python"
    if not run(f'{python_cmd} -m ipykernel install --user --name {ENV_NAME} --display-name "CHORUS Tutorial"'):
        print("Warning: Failed to register kernel")

    # Step 5: Verify
    print(f"\n[4/4] Verifying installation...")
    test_imports = [
        "pandas",
        "numpy",
        "faiss",
        "sentence_transformers",
        "gurobipy",
        "langchain",
    ]

    for package in test_imports:
        result = subprocess.run(
            f'{python_cmd} -c "import {package}"',
            shell=True,
            capture_output=True
        )
        status = "✓" if result.returncode == 0 else "✗"
        print(f"  {status} {package}")

    # Done
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print(f"\nActivate with: conda activate {ENV_NAME}")
    print(f"Start Jupyter: jupyter lab")
    print(f'\nIn Jupyter, select kernel: "CHORUS Tutorial"')
    print("\nDon't forget to:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your OpenRouter API key")
    print("  3. Activate Gurobi license: grbgetkey YOUR-KEY")

    return 0

if __name__ == "__main__":
    sys.exit(main())
