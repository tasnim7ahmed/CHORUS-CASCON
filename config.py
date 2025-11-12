"""
CHORUS Tutorial Configuration
=============================

This file contains all configurable parameters for the CHORUS pipeline.
Modify these values to customize the tutorial demonstration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), 'test.env'))

# Set HuggingFace token for model downloads
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN
    os.environ["HUGGING_FACE_HUB_TOKEN"] = HF_TOKEN

# ============================================================================
# PATHS AND DIRECTORIES
# ============================================================================

# Base directory (parent of tutorial folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input paths
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PDF_THEORETICAL = os.path.join(DOCS_DIR, "docs-gurobi-com-optimizer-en-12.0.pdf")
PDF_CODE_EXAMPLES = os.path.join(DOCS_DIR, "docs-gurobi-com-examples-en-11.0.pdf")
TEST_DATA_PATH = os.path.join(BASE_DIR, "test_data.csv")

# Output paths (all inside tutorial folder)
TUTORIAL_DIR = BASE_DIR
DOC_CHUNKS_PATH = os.path.join(TUTORIAL_DIR, "tutorial_chunks_doc.pkl")
CODE_CHUNKS_PATH = os.path.join(TUTORIAL_DIR, "tutorial_chunks_code.pkl")
VECTORSTORE_DOC_PATH = os.path.join(TUTORIAL_DIR, "tutorial_vectorstore_save")
VECTORSTORE_CODE_PATH = os.path.join(TUTORIAL_DIR, "tutorial_code_save")
RESULTS_PATH = os.path.join(TUTORIAL_DIR, "tutorial_results.csv")
SUMMARY_PATH = os.path.join(TUTORIAL_DIR, "tutorial_summary.txt")

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Temperature for code generation (0.0 = deterministic)
LLM_TEMPERATURE = 0.0

# Embedding model for vector stores
# Options: "all-MiniLM-L6-v2", "nvidia/NV-Embed-v2", "Alibaba-NLP/gte-Qwen2-1.5B-instruct"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Cross-encoder model for reranking
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ============================================================================
# CHUNKING PARAMETERS
# ============================================================================

# Maximum words per chunk (for theoretical documentation)
MAX_CHUNK_WORDS = 400

# Whether to split large chunks exceeding MAX_CHUNK_WORDS
SPLIT_LARGE_CHUNKS = True

# ============================================================================
# RETRIEVAL PARAMETERS
# ============================================================================

# Initial retrieval: Top-k documents from vector search
RETRIEVAL_TOP_K = 10

# After reranking: Number of documents to keep
# Manuscript specifies: top-3 conceptual, top-2 code examples
# Implementation uses top-2 for both (can be modified)
RERANK_TOP_N_DOC = 2
RERANK_TOP_N_CODE = 2

# Number of keywords to generate per problem (5-7 recommended)
NUM_KEYWORDS_MIN = 5
NUM_KEYWORDS_MAX = 7

# ============================================================================
# CODE GENERATION PARAMETERS
# ============================================================================

# Structured output schema
# Set to False for ablation study (CHORUS w/o reasoning)
INCLUDE_REASONING_FIELD = True

# Code execution timeout (seconds)
EXECUTION_TIMEOUT = 120

# ============================================================================
# TUTORIAL DEMONSTRATION PARAMETERS
# ============================================================================

# TEST MODE: Use minimal data for quick pipeline testing
# Set to True for initial testing to save API costs
TEST_MODE = True

# Maximum chunks to process in TEST_MODE
# For testing: Process only first 20 doc chunks and 20 code chunks
TEST_MAX_DOC_CHUNKS = 20
TEST_MAX_CODE_CHUNKS = 20

# Number of problems to demonstrate
# Set to 2 for testing, 5-10 for tutorial, 289 for full evaluation
NUM_PROBLEMS = 2 if TEST_MODE else 5

# Number of example chunks to display in Stage 1
NUM_EXAMPLE_CHUNKS = 5

# Number of code examples to show metadata in Stage 2
NUM_EXAMPLE_CODE_METADATA = 3

# Number of similarity search tests in Stage 3
NUM_SIMILARITY_TESTS = 2

# Number of problems to show retrieval details in Stage 5
NUM_RETRIEVAL_EXAMPLES = 2

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================

# Maximum characters to display in truncated outputs
MAX_DISPLAY_CHARS = 500

# Whether to print detailed logs during execution
VERBOSE = True

# Whether to save intermediate outputs (useful for debugging)
SAVE_INTERMEDIATES = True

# ============================================================================
# ADVANCED SETTINGS (usually don't need to change)
# ============================================================================

# FAISS index type
# Options: "Flat" (exact search), "IVF" (approximate, faster for large datasets)
FAISS_INDEX_TYPE = "Flat"

# Allow dangerous deserialization when loading FAISS stores
# Set to True for tutorial (trusted environment)
FAISS_ALLOW_DANGEROUS = True

# Random seed for reproducibility
RANDOM_SEED = 42

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration and check file existence."""
    errors = []

    # Check PDF files exist
    if not os.path.exists(PDF_THEORETICAL):
        errors.append(f"Theoretical PDF not found: {PDF_THEORETICAL}")

    if not os.path.exists(PDF_CODE_EXAMPLES):
        errors.append(f"Code examples PDF not found: {PDF_CODE_EXAMPLES}")

    if not os.path.exists(TEST_DATA_PATH):
        errors.append(f"Test data not found: {TEST_DATA_PATH}")

    # Check tutorial directory exists
    if not os.path.exists(TUTORIAL_DIR):
        os.makedirs(TUTORIAL_DIR)
        print(f"Created tutorial directory: {TUTORIAL_DIR}")

    # Check parameter ranges
    if NUM_PROBLEMS < 1:
        errors.append("NUM_PROBLEMS must be at least 1")

    if MAX_CHUNK_WORDS < 100:
        errors.append("MAX_CHUNK_WORDS too small (minimum 100)")

    if RETRIEVAL_TOP_K < RERANK_TOP_N_DOC:
        errors.append("RETRIEVAL_TOP_K must be >= RERANK_TOP_N_DOC")

    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("Configuration validated successfully")
    return True

# ============================================================================
# PRINT CONFIGURATION
# ============================================================================

def print_config():
    """Print current configuration settings."""
    print("=" * 70)
    print("CHORUS TUTORIAL CONFIGURATION")
    print("=" * 70)
    print(f"\nPaths:")
    print(f"  Theoretical PDF: {PDF_THEORETICAL}")
    print(f"  Code Examples PDF: {PDF_CODE_EXAMPLES}")
    print(f"  Test Data: {TEST_DATA_PATH}")
    print(f"  Output Directory: {TUTORIAL_DIR}")

    print(f"\nModels:")
    print(f"  LLM (OpenRouter): {OPENROUTER_MODEL}")
    print(f"  Embedding: {EMBEDDING_MODEL}")
    print(f"  Cross-Encoder: {CROSS_ENCODER_MODEL}")

    print(f"\nParameters:")
    print(f"  Chunk Size: {MAX_CHUNK_WORDS} words")
    print(f"  Retrieval Top-K: {RETRIEVAL_TOP_K}")
    print(f"  Rerank Doc/Code: {RERANK_TOP_N_DOC}/{RERANK_TOP_N_CODE}")
    print(f"  Execution Timeout: {EXECUTION_TIMEOUT}s")

    print(f"\nTutorial Demo:")
    print(f"  Problems to Demonstrate: {NUM_PROBLEMS}")
    print(f"  Include Reasoning Field: {INCLUDE_REASONING_FIELD}")
    print(f"  Verbose Output: {VERBOSE}")

    print("=" * 70)

if __name__ == "__main__":
    # Validate and print configuration when run directly
    print_config()
    validate_config()
