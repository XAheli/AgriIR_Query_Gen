# Agriculture Inconsistency Detection Pipeline

A comprehensive data pipeline for creating an **Indian Agriculture Inconsistency Detection Dataset** by scraping diverse sources, extracting agriculture-related statements using NLP, and generating intelligent statement pairs for manual annotation.

---

## 📋 Project Overview

This project creates a dataset for detecting inconsistencies in statements about Indian agriculture.

**What This Pipeline Does**:

1. 🔍 **Multi-Source Scraping**: Google search results (via SerpAPI), web articles, Reddit discussions
2. 🧠 **NLP Processing**: SpaCy-based statement extraction with opinion detection
3. 🔗 **Intelligent Pairing**: Sentence Transformers for semantic similarity with stratified sampling
4. 📊 **Export for Annotation**: CSV format with metadata for manual labeling

**Goal**: Create 300+ high-quality annotated statement pairs to train inconsistency detection models.


## 🎯 Task Definition

Classify relationships between agriculture statement pairs:

- **Unrelated**: Statements discuss different topics
- **Consistent**: Both statements can be true, support similar conclusions
- **Inconsistent**: Statements contradict each other
  - *Surface contradiction*: Direct logical contradiction
  - *Factual inconsistency*: Conflicting facts/statistics
  - *Value inconsistency*: Conflicting values/policy positions

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Virtual environment (recommended)
- Git LFS installed (for data files)

### 1. Clone Repository

```
git clone git@github.com:XAheli/AgriIR_Query_Gen.git
cd AgriIR_Query_Gen
git lfs pull  # Download data files
```

### 2. Install Dependencies

```
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Download SpaCy model
python -m spacy download en_core_web_sm
```

### 3. Configure API Keys (Optional but Recommended)

Create `secrets.toml` in the project root:

```
[api]
serp_api_key = "your_serpapi_key_here"  # Get from serpapi.com (100 free/month)

[reddit]
client_id = "your_reddit_client_id"
client_secret = "your_reddit_client_secret"
user_agent = "python:agriculture_scraper:v1.0 (by /u/YourUsername)"
```

**Note**: Get Reddit credentials from https://www.reddit.com/prefs/apps

**Without API keys**: Pipeline will use web scraping fallbacks (slower, less reliable).

### 4. Run the Pipeline

```
source .venv/bin/activate
python main_enhanced.py
```

⚠️ **Important**: The pipeline may hang at Step 6 (embedding computation) due to GPU/memory limitations on local machines. See "GPU Issue Workaround" section below.


## 📊 Pipeline Steps

The pipeline has **8 steps** divided into two parts:

### Part 1: Data Collection (Steps 1-5)

**Runs on**: Local machine  
**Runtime**: 30-60 minutes

1. **SERP Scraping**: Query Google for agriculture-related content using 43 controversy-focused queries
2. **Content Extraction**: Scrape full text from URLs using multi-strategy extraction
3. **Reddit Scraping**: Collect posts and comments from 10 agriculture-related subreddits
4. **Statement Extraction**: Use SpaCy to extract sentences, detect opinions, filter for relevance
5. **Database Storage**: Save statements to SQLite database

**Expected Output**:
- ~3,400+ documents scraped
- ~22,000+ statements extracted
- ~4,400+ opinion statements (19.9%)

### Part 2: Pair Generation (Steps 6-8)

**GPU-intensive** - May crash on local machines without sufficient GPU/memory

6. **Embedding Computation**: Generate semantic embeddings using Sentence Transformers
7. **Intelligent Pairing**: 
   - Compute cosine similarity matrix
   - Quality scoring (bonus for same-source, opinions)
   - Stratified sampling (50% same-source opinions, 25% same-source mixed, etc.)
   - Diversity filtering (max 100 pairs per URL combo)
8. **Export**: Generate CSV with annotation columns

**Expected Output**:
- 1,000+ diverse statement pairs ready for annotation


## 🔧 GPU Issue Workaround

If your computer hangs/crashes at Step 6 (embedding computation), you have two options:

### Option A: Stop After Step 5 (Recommended for Low-End Machines)

```
# Run pipeline
python main_enhanced.py

# Wait for console message: "Step 5 completed: 22,198 statements saved to database"
# Then press Ctrl+C to stop before Step 6
```

Your data is saved in:
- `data/processed/statements.json` (22,198 statements)
- `data/agriculture_statements.db` (SQLite database)

You can manually create pairs later or use external GPU resources for Steps 6-8.

### Option B: Use GPU Cluster (Provided Script)

A standalone GPU script (`generate_pairs_gpu.py`) is provided for university GPU clusters:

```
# On GPU cluster
pip install -r requirements_gpu.txt
python generate_pairs_gpu.py
```

See `README_GPU_CLUSTER.md` for detailed instructions.


## 🔧 Configuration

### Key Parameters in `config.py`

```
# Queries - 43 controversy-focused queries on Indian agriculture
AGRICULTURE_QUERIES = [...]  # Farm laws, MSP, subsidies, reforms, etc.

# Similarity threshold for pairing (0-1)
SIMILARITY_THRESHOLD = 0.3  # Lower = more pairs but less similar

# Maximum pairs from single URL combination
MAX_PAIRS_PER_SOURCE = 100  # For diversity

# Sentence Transformer model
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

# Target domains - 20+ sites including government, news, agriculture portals
TARGET_DOMAINS = [...]
```

### Customization

**Edit `config.py` to**:
- Add/modify agriculture queries (focus on controversies)
- Change target domains for different source types
- Adjust similarity threshold (lower = more pairs)
- Configure scraping parameters (delays, user agent)

**Edit `main_enhanced.py` to**:
- Change number of queries used (default: all 43)
- Adjust max URLs per query (default: 50)
- Set target pair count (default: 1000)
- Enable/disable Reddit scraping (default: enabled)


## 📝 Annotation Guide

### CSV Format

The exported CSV (`data/final/pairs_for_annotation_*.csv`) contains:

| Column | Description |
|--------|-------------|
| `id` | Unique pair identifier |
| `statement_a` | First statement text |
| `statement_b` | Second statement text |
| `similarity_score` | Semantic similarity (0-1) |
| `quality_score` | Quality score with bonuses |
| `same_source` | Both from same URL? |
| `both_have_opinions` | Both contain opinions? |
| `source_a` / `source_b` | Source URLs |
| `domain_a` / `domain_b` | Domain names |
| `author_a` / `author_b` | Authors (if available) |
| `relationship_label` | **[TO FILL]** Unrelated/Consistent/Inconsistent |
| `inconsistency_subtype` | **[TO FILL]** Surface/Factual/Value (if Inconsistent) |
| `notes` | Optional observations |

### Annotation Instructions

1. **Prioritize**: Start with pairs where `same_source=True` and `both_have_opinions=True`
2. **Label `relationship_label`**:
   - `Unrelated`: Completely different topics
   - `Consistent`: Can both be true
   - `Inconsistent`: Contradictory
3. **If Inconsistent, label `inconsistency_subtype`**:
   - `Surface`: Direct logical contradiction
   - `Factual`: Conflicting facts/numbers
   - `Value`: Conflicting opinions/values
4. **Add notes**: Any observations to help with model training

**Target**: Annotate 300+ pairs for robust dataset.

### Annotation Examples

**Inconsistent - Surface:**
- A: "Farm laws were repealed in 2021"
- B: "Farm laws are still in effect"

**Inconsistent - Factual:**
- A: "MSP increased by 10%"
- B: "MSP decreased by 5%" (same year/crop)

**Inconsistent - Value:**
- A: "Farm laws benefit small farmers"
- B: "Farm laws harm small farmers"

**Consistent:**
- A: "Farmers need better MSP"
- B: "Agricultural support prices should increase"

---

## 🔒 Security & Privacy

### API Keys

- **secrets.toml is NOT in the repository** (protected by .gitignore)
- `config.py` loads secrets at runtime using `tomli` library
- Never commit `secrets.toml` to version control
- Get your own API keys:
  - SerpAPI: https://serpapi.com (250 free searches/month)
  - Reddit: https://www.reddit.com/prefs/apps

### Data Privacy

- All scraped content is from public sources
- Reddit scraping follows API terms of service
- Respects `robots.txt` and rate limits
- No personal data collection


## 📦 Git LFS

Large data files (.csv, .json, .db) are tracked with Git LFS:

```
# Already configured in .gitattributes
# Files are automatically managed by Git LFS

# To download data files after cloning
git lfs pull
```

