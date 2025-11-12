# CHORUS: Hierarchical RAG for Mathematical Optimization Code Generation

A Jupyter notebook tutorial implementing the CHORUS framework, a Retrieval-Augmented Generation (RAG) system that generates executable Gurobi optimization code from natural language problem descriptions.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gurobi](https://img.shields.io/badge/Gurobi-11.0-green.svg)](https://www.gurobi.com/)

## Overview

CHORUS is a RAG-based system that bridges natural language and optimization code through:
- **Hierarchical document processing** that preserves semantic structure
- **Dual-stage retrieval** (vector search + cross-encoder reranking) for precise context
- **Expert prompting** with structured output for reliable code generation
- **Safe execution** with timeout protection for validation

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- [Conda](https://docs.conda.io/en/latest/miniconda.html) or Miniconda
- [Gurobi license](https://www.gurobi.com/downloads/) (free academic license available)
- OpenRouter API key (get from [openrouter.ai/keys](https://openrouter.ai/keys))

### Setup

**1. Run the setup script:**
```bash
./setup.sh
```

The script will:
- Create `chorus-tutorial` conda environment with Python 3.9
- Install all dependencies with exact working versions
- Register Jupyter kernel
- Verify installation (~5-10 minutes)

**2. Activate environment:**
```bash
conda activate chorus-tutorial
```

**3. Configure API keys:**
```bash
# Copy template to your env file
cp .env.example test.env

# Edit test.env and add your keys:
nano test.env
```

Required variables:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
HF_TOKEN=your_huggingface_token_here  # optional
```

**4. Activate Gurobi license:**
```bash
grbgetkey YOUR-LICENSE-KEY
```

Get your academic license at [gurobi.com/academia](https://www.gurobi.com/academia/academic-program-and-licenses/)

**5. Start Jupyter:**
```bash
jupyter lab
```

In Jupyter, select the **"CHORUS Tutorial"** kernel when opening notebooks.

---

## Running the Tutorial

Execute notebooks sequentially (01 through 07):

1. **01_pdf_processing.ipynb** → Hierarchical chunking of Gurobi documentation
2. **02_metadata_generation.ipynb** → Generate summaries and keywords for code examples
3. **03_vector_store_creation.ipynb** → Build FAISS indices for retrieval
4. **04_keyword_generation.ipynb** → Extract keywords from problem descriptions
5. **05_retrieval_and_reranking.ipynb** → Two-stage retrieval with reranking
6. **06_code_generation.ipynb** → Generate Gurobi code using LLM
7. **07_execution_and_evaluation.ipynb** → Execute and evaluate generated code

**Estimated time**: 35-50 minutes (test mode with 2 problems)

---

## CHORUS Pipeline Stages

### Stage 1: PDF Processing and Hierarchical Chunking
**Runtime**: ~2-3 minutes

Extracts table of contents from Gurobi PDF documentation and creates hierarchical chunks that preserve document structure. Unlike fixed-size chunking, this respects semantic boundaries (chapters, sections).

**Output**: `tutorial_chunks_doc.pkl`

### Stage 2: Metadata Generation for Code Examples
**Runtime**: ~15-20 minutes

Generates LLM-based summaries and keywords for code snippets to bridge the vocabulary gap between natural language queries and code syntax. For example, "minimize cost" is linked to `model.setObjective(..., GRB.MINIMIZE)`.

**Output**: `tutorial_chunks_code.pkl`

### Stage 3: Vector Store Creation
**Runtime**: ~3-5 minutes

Creates FAISS indices for fast similarity search over documentation and code examples. Uses `all-MiniLM-L6-v2` embeddings (384 dimensions).

**Output**: `tutorial_vectorstore_save/`, `tutorial_code_save/`

### Stage 4: Keyword Generation from Problems
**Runtime**: ~2-3 minutes

Extracts 5-7 keywords from each problem description using LLM. Keywords balance domain context (e.g., "fishery transportation") with technical hints (e.g., "binary variables", "budget constraint").

**Output**: `tutorial_keywords.pkl`

### Stage 5: Retrieval and Cross-Encoder Reranking
**Runtime**: ~1-2 minutes

Performs two-stage retrieval:
1. **Vector search**: Fast retrieval of top-10 candidates using dual-encoder
2. **Reranking**: Precise scoring with cross-encoder to select top-2 docs + top-2 code examples

**Output**: `tutorial_retrievals.pkl`

### Stage 6: Code Generation with Expert Prompting
**Runtime**: ~10-15 minutes

Generates executable Gurobi code using LLM with:
- Retrieved context injection (2 docs + 2 code examples)
- Structured output (Pydantic schema)
- Reasoning field for self-validation

**Output**: `tutorial_generated_code.pkl`

### Stage 7: Execution and Evaluation
**Runtime**: ~2-5 minutes

Executes generated code safely with:
- Isolated namespace (no scope pollution)
- 120-second timeout protection
- Accuracy calculation vs. ground truth

**Output**: `tutorial_results.csv`, `tutorial_summary.txt`

---

## Configuration

Edit `config.py` to customize the pipeline:

```python
# Test mode (faster, fewer problems)
TEST_MODE = True         # Set False for full pipeline
NUM_PROBLEMS = 2         # 2 for testing, 5-10 for demo, 289 for full

# Model selection
OPENROUTER_MODEL = "google/gemini-2.0-flash-exp:free"  # Free tier
# Alternatives: "anthropic/claude-3.5-sonnet", "openai/gpt-4"

# Retrieval parameters
RETRIEVAL_TOP_K = 10     # Initial candidates from vector search
RERANK_TOP_N_DOC = 2     # Final docs after reranking
RERANK_TOP_N_CODE = 2    # Final code examples after reranking

# Execution
EXECUTION_TIMEOUT = 120  # Seconds per problem
```

---

## Dataset

The tutorial uses **[NL4Opt](https://proceedings.mlr.press/v220/ramamonjison23a.html)**, a benchmark dataset of 289 linear/integer programming problems:
- Natural language problem descriptions
- Ground truth Gurobi code solutions
- Expected objective values for evaluation

**Categories**: Resource allocation, production planning, financial optimization, network flow

**Format** (`test_data.csv`):
```csv
problem_id,question,expected_objective
0,"A fishery wants to transport...",3000.0
1,"An office supply company...",5050.0
```

---

## Files Generated During Execution

**Do not commit these files** (already in `.gitignore`):
- `tutorial_chunks_doc.pkl`, `tutorial_chunks_code.pkl` - Processed documents
- `tutorial_keywords.pkl` - Extracted keywords
- `tutorial_retrievals.pkl` - Retrieved context
- `tutorial_generated_code.pkl` - Generated Gurobi code
- `tutorial_vectorstore_save/`, `tutorial_code_save/` - FAISS indices
- `tutorial_results.csv` - Full results with execution outputs
- `tutorial_summary.txt` - Accuracy metrics

---

## Citation

If you use CHORUS in your research, please cite:

```bibtex
@inproceedings{c-2025-lion,
      title={CHORUS: Zero-shot Hierarchical Retrieval and Orchestration for Generating Linear Programming Code},
      author={Tasnim Ahmed and Salimur Choudhury},
      year={2025},
      eprint={2505.01485},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.01485},
      booktitle={The 19th Learning and Intelligent OptimizatioN Conference (LION19)}
}
```

---

## Acknowledgments

- **Gurobi Optimization**: Documentation and Python API
- **OpenRouter**: Unified LLM API access
- **HuggingFace**: Embedding models and transformers
- **LangChain**: RAG framework utilities
- **FAISS**: Similarity search
- **NL4Opt**: [Benchmark dataset](https://proceedings.mlr.press/v220/ramamonjison23a.html)

---

## Contact

- **Author**: Tasnim Ahmed
- **Email**: tasnim.ahmed@queensu.ca
- **GitHub**: [@tasnim7ahmed](https://github.com/tasnim7ahmed)
- **Institution**: Queen's University
- **Paper**: [arXiv:2505.01485](https://arxiv.org/abs/2505.01485)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

**Third-party licenses**:
- Gurobi: Commercial license (free for academic use)
- OpenRouter: Per-token pricing (free tier available)
- HuggingFace Models: Apache 2.0 / MIT
