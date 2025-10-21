# Agriculture Inconsistency Detection Dataset# Agriculture Inconsistency Detection - Setup & Usage Guide



[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)## 📋 Project Overview

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project creates a dataset for detecting inconsistencies in statements about Indian agriculture. It:

## 📋 Project Overview1. **Scrapes** diverse sources (Google, articles, Reddit, social media)

2. **Extracts** agriculture-related statements using NLP

A comprehensive pipeline for creating an **Indian Agriculture Inconsistency Detection Dataset**. This project scrapes diverse sources, extracts agriculture-related statements using NLP, and generates intelligent statement pairs for manual annotation.3. **Generates** smart statement pairs based on semantic similarity

4. **Exports** pairs for manual annotation

**Goal**: Create 300+ high-quality annotated statement pairs to train inconsistency detection models.

**Goal**: Create 200+ annotated statement pairs to train an inconsistency detection model.

### What This Does

## 🎯 Task Definition

1. 🔍 **Multi-Source Scraping**: Google search results (SerpAPI), web articles, Reddit discussions

2. 🧠 **NLP Processing**: SpaCy-based statement extraction with opinion detectionClassify relationship between statement pairs as:

3. 🔗 **Intelligent Pairing**: Sentence Transformers for semantic similarity, stratified sampling for diversity- **Unrelated**: Different topics

4. 📊 **Export for Annotation**: CSV format with metadata for manual labeling- **Consistent**: Compatible statements

- **Inconsistent**: Contradictory statements

### Task Definition  - *Surface contradiction*: Direct logical contradiction

  - *Factual inconsistency*: Conflicting facts/numbers

Classify relationships between agriculture statement pairs:  - *Value inconsistency*: Conflicting values/policies



- **Unrelated**: Statements discuss different topics## 🚀 Quick Start

- **Consistent**: Both statements can be true, support similar conclusions

- **Inconsistent**: Statements contradict each other### 1. Install Dependencies

  - *Surface contradiction*: Direct logical contradiction

  - *Factual inconsistency*: Conflicting facts/statistics```bash

  - *Value inconsistency*: Conflicting values/policy positions# Create virtual environment (recommended)

python -m venv venv

---source venv/bin/activate  # On Windows: venv\Scripts\activate



## 🚀 Quick Start# Install requirements

pip install -r requirements.txt

### Prerequisites

# Download SpaCy model

- Python 3.11+python -m spacy download en_core_web_sm

- Virtual environment (recommended)```

- Git LFS installed (for data files)

### 2. Configure (Optional)

### 1. Clone Repository

Edit `config.py` to:

```bash- Add more agriculture queries

git clone git@github.com:XAheli/AgriIR_Query_Gen.git- Configure target domains

cd AgriIR_Query_Gen- Set API keys (optional, for better results)

```

```python

### 2. Install Dependencies# For better Google scraping (100 free searches/month)

SERP_API_KEY = "your_serpapi_key"  # Get from serpapi.com

```bash

# Create and activate virtual environment# For Reddit scraping (optional)

python -m venv .venvREDDIT_CLIENT_ID = "your_client_id"

source .venv/bin/activate  # On Windows: .venv\Scripts\activateREDDIT_CLIENT_SECRET = "your_client_secret"

# Get from: https://www.reddit.com/prefs/apps

# Install packages```

pip install -r requirements.txt

### 3. Run the Pipeline

# Download SpaCy model

python -m spacy download en_core_web_sm```bash

```# Use enhanced pipeline (recommended)

python main_enhanced.py

### 3. Configure API Keys (Optional but Recommended)

# Or use basic pipeline

Create `secrets.toml` from the example:python main.py

```

```bash

cp secrets.toml.example secrets.toml## 📦 What Gets Generated

```

After running the pipeline, you'll have:

Edit `secrets.toml` and add your API keys:

```

```tomldata/

[api]├── raw/

serp_api_key = "your_serpapi_key_here"  # Get from serpapi.com (100 free/month)│   ├── search_results.csv      # Google search results

│   ├── documents.json          # Scraped article content

[reddit]│   └── reddit_content.json     # Reddit posts/comments (if enabled)

client_id = "your_reddit_client_id"├── processed/

client_secret = "your_reddit_client_secret"│   └── statements.json         # Extracted statements

user_agent = "python:agriculture_scraper:v1.0 (by /u/YourUsername)"├── final/

```│   └── pairs_for_annotation_[timestamp].csv  # Ready for annotation

└── agriculture_statements.db   # SQLite database

**Without API keys**: The pipeline will still work using web scraping fallbacks (slower, less reliable).```



### 4. Run the Pipeline## 📝 Manual Annotation



#### Option A: Local Machine (Steps 1-5 only)1. **Open** the CSV file in `data/final/`

2. **Review** each pair and fill columns:

```bash   - `relationship_label`: Unrelated/Consistent/Inconsistent

source .venv/bin/activate   - `inconsistency_subtype`: Surface/Factual/Value (if Inconsistent)

python main_enhanced.py   - `notes`: Any observations

```

3. **Prioritize** pairs where `same_source = True` (self-inconsistency)

⚠️ **Note**: Steps 6-8 (embedding computation) require GPU resources. Your local machine may hang/crash at Step 6.4. **Target** 200+ annotated pairs for quality dataset



#### Option B: Complete Pipeline with Google Colab (Recommended)### Annotation Guidelines



**Steps 1-5 (Local - Data Collection):**#### Unrelated

```bash- Statements discuss completely different topics

source .venv/bin/activate- No logical connection

python main_enhanced.py- Example: "MSP increased" vs "Cotton prices fell"

# Wait for "Step 5 completed" message, then stop (Ctrl+C) if it hangs at Step 6

```#### Consistent

- Both can be true simultaneously

**Steps 6-8 (Colab - Pair Generation):**- Support similar conclusions

1. Upload `colab_pair_generation.ipynb` to Google Colab- Example: "Farmers need support" vs "Agricultural subsidies help farmers"

2. Upload `data/processed/statements.json` (generated from Steps 1-5)

3. Enable GPU: Runtime → Change runtime type → GPU (T4)#### Inconsistent Types

4. Run all cells

5. Download generated CSV file**Surface Contradiction**

- Direct logical contradiction

**Expected Time**:- Both cannot be true

- Local Steps 1-5: 30-60 minutes (depends on network speed)- Example: "MSP increased by 10%" vs "MSP decreased this year"

- Colab Steps 6-8: 5-10 minutes with GPU

**Factual Inconsistency**

---- Conflicting facts, numbers, or data

- Example: "1000 farmers" vs "5000 farmers" (same event)

## 📂 Project Structure

**Value Inconsistency**

```- Conflicting values, opinions, or policy positions

agriculture_inconsistency_detection/- Example: "Farm laws benefit farmers" vs "Farm laws harm farmers"

├── main_enhanced.py              # Main pipeline orchestrator

├── config.py                     # Configuration (queries, parameters)## 🔧 Customization

├── secrets.toml                  # API keys (DO NOT COMMIT)

├── secrets.toml.example          # Template for secrets### Add More Queries

├── requirements.txt              # Python dependencies

├── colab_pair_generation.ipynb   # Google Colab notebook for Steps 6-8Edit `config.py`:

│

├── scraping/                     # Data collection modules```python

│   ├── enhanced_serp_scraper.py  # Google search with SerpAPIAGRICULTURE_QUERIES = [

│   ├── enhanced_content_scraper.py # Multi-strategy content extraction    "your custom query 1",

│   └── reddit_scraper.py         # Reddit posts & comments    "your custom query 2",

│    # Add more...

├── processing/                   # NLP processing modules]

│   ├── enhanced_statement_extractor.py  # SpaCy + opinion detection```

│   └── enhanced_pair_generator.py       # Semantic similarity pairing

│### Adjust Similarity Threshold

├── storage/                      # Database management

│   └── database.py               # SQLite operationsLower threshold = more pairs (but less similar):

│

├── annotation/                   # Export utilities```python

│   └── export_for_annotation.py # CSV/JSON exportersSIMILARITY_THRESHOLD = 0.2  # Default: 0.3

│```

└── data/                         # Generated data (tracked with Git LFS)

    ├── raw/                      # Scraped content### Change Target Pair Count

    │   ├── search_results.csv

    │   ├── documents.jsonIn `main_enhanced.py`:

    │   └── reddit_content.json

    ├── processed/                # Extracted statements```python

    │   └── statements.jsonTARGET_PAIRS = 1000  # Default: 500

    └── final/                    # Annotated pairs```

        └── pairs_for_annotation_*.csv

```## 🛠️ Troubleshooting



---### Issue: Google Blocking Requests



## 🔧 Configuration**Solution 1**: Use SerpAPI (recommended)

- Sign up at https://serpapi.com (100 free searches/month)

### Key Parameters in `config.py`- Add API key to `config.py`



```python**Solution 2**: Increase delays

# Number of queries to use (43 controversy-focused queries available)```python

AGRICULTURE_QUERIES = [...]  # 43 queries covering farm laws, MSP, subsidies, etc.SCRAPE_DELAY = 5  # Increase from 2

```

# Similarity threshold for pairing (0-1)

SIMILARITY_THRESHOLD = 0.3**Solution 3**: Use Selenium (slower but more reliable)

- Already in requirements

# Maximum pairs from single URL combination- Modify scraper to use Selenium

MAX_PAIRS_PER_SOURCE = 100

### Issue: No Statements Extracted

# Sentence Transformer model

SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L12-v2"**Cause**: Scraping failed or content quality poor

```

**Solutions**:

### Customization- Check `data/raw/documents.json` to verify content

- Lower `MIN_STATEMENT_LENGTH` in config

Edit `config.py` to:- Add more/better queries

- Add/modify agriculture queries (focus on controversies for better inconsistencies)- Target specific trusted domains

- Change target domains (government sites, news outlets, etc.)

- Adjust similarity thresholds### Issue: No Pairs Generated

- Configure scraping parameters

**Cause**: Statements too dissimilar

---

**Solutions**:

## 📊 Pipeline Steps- Lower `SIMILARITY_THRESHOLD` in config (try 0.2)

- Collect more statements (use more queries/URLs)

### Steps 1-5: Data Collection (Local Machine)- Focus queries on specific controversial topics



1. **SERP Scraping**: Query Google for agriculture-related content### Issue: Too Many Pairs

2. **Content Extraction**: Scrape full text from URLs using multi-strategy extraction

3. **Reddit Scraping**: Collect posts and comments from agriculture subreddits**Solution**: Filter more aggressively

4. **Statement Extraction**: Extract sentences with SpaCy, detect opinions, filter for relevance```python

5. **Database Storage**: Save statements to SQLite databaseMAX_PAIRS_PER_SOURCE = 50  # Default: 100

```

**Output**: 

- ~3,400+ documents## 📊 Pipeline Parameters

- ~22,000+ statements

- ~4,400+ opinion statements (19.9%)Edit these in `main_enhanced.py`:



### Steps 6-8: Pair Generation (Google Colab GPU)```python

NUM_QUERIES = 10              # Number of queries to use

6. **Embedding Computation**: Generate semantic embeddings using Sentence Transformers (GPU-accelerated)MAX_URLS_PER_QUERY = 10      # URLs to scrape per query

7. **Intelligent Pairing**: TARGET_PAIRS = 500            # Target pair count

   - Compute cosine similarity matrixUSE_REDDIT = False            # Enable Reddit scraping

   - Quality scoring (bonus for same-source, opinions)```

   - Stratified sampling (50% same-source opinions, 25% same-source mixed, etc.)

   - Diversity filtering (max 100 pairs per URL combo)## 🎓 Tips for Better Results

8. **Export**: Generate CSV with annotation columns

### 1. Target Controversial Topics

**Output**: Focus queries on topics with multiple viewpoints:

- 1,000+ diverse statement pairs- Farm laws debate

- Ready for manual annotation- MSP policy changes

- Subsidy programs

---- Agricultural reforms



## 📝 Annotation Guide### 2. Mix Source Types

Combine:

### CSV Format- Government announcements (official stance)

- News articles (factual reporting)

The exported CSV contains:- Opinion pieces (subjective views)

- Social media (public opinions)

| Column | Description |

|--------|-------------|### 3. Same-Source Pairs

| `id` | Unique pair identifier |Prioritize pairs from same source/author:

| `statement_a` | First statement |- Better for detecting self-inconsistency

| `statement_b` | Second statement |- Shows evolution of positions

| `similarity_score` | Semantic similarity (0-1) |- More interesting contradictions

| `quality_score` | Quality score with bonuses |

| `same_source` | Both from same URL? |### 4. Opinion Statements

| `both_have_opinions` | Both contain opinions? |Look for statements with:

| `source_a` / `source_b` | Source URLs |- Modal verbs: should, must, need to

| `domain_a` / `domain_b` | Domain names |- Stance markers: support, oppose, believe

| `relationship_label` | **[TO ANNOTATE]** Unrelated/Consistent/Inconsistent |- Value judgments: better, worse, unfair

| `inconsistency_subtype` | **[TO ANNOTATE]** Surface/Factual/Value (if Inconsistent) |

| `notes` | Optional observations |## 🔍 Data Quality Checks



### Annotation InstructionsBefore annotation, verify:



1. **Prioritize**: Start with pairs where `same_source=True` and `both_have_opinions=True`1. **Statement Quality**

2. **Label**: Fill `relationship_label` column:   - ✅ Complete sentences

   - `Unrelated`: Completely different topics   - ✅ Agriculture-related

   - `Consistent`: Can both be true   - ✅ Readable and clear

   - `Inconsistent`: Contradictory   - ❌ No promotional text

3. **Subtype**: If `Inconsistent`, fill `inconsistency_subtype`:   - ❌ No navigation text

   - `Surface`: Direct logical contradiction

   - `Factual`: Conflicting facts/numbers2. **Pair Quality**

   - `Value`: Conflicting opinions/values   - ✅ Semantically similar (overlap in topic)

4. **Notes**: Add any observations to help with model training   - ✅ Both are substantial statements

   - ✅ Worth comparing for consistency

**Target**: Annotate 300+ pairs for robust dataset.   - ❌ Not identical/near-duplicate

   - ❌ Not completely unrelated

---

## 📈 Expected Output

## 🔒 Security & Privacy

For a typical run with 10 queries:

### API Keys- **URLs found**: 50-100

- **Documents scraped**: 30-70 (60-70% success rate)

- **Never commit** `secrets.toml` to GitHub- **Statements extracted**: 500-2000

- Use `secrets.toml.example` as template- **Candidate pairs**: 1000-5000

- API keys are loaded at runtime from `secrets.toml`- **Final pairs**: 500 (after filtering)

- `.gitignore` configured to exclude secrets- **For annotation**: Select best 200-300



### Data Privacy## 🔗 Useful Resources



- All scraped content is public data### APIs & Tools

- Reddit scraping follows API terms of service- SerpAPI: https://serpapi.com (Google scraping)

- Respects `robots.txt` and rate limits- Reddit API: https://www.reddit.com/prefs/apps

- SpaCy: https://spacy.io/usage/models

---

### Open Source Scrapers

## 📦 Git LFS Setup- newspaper3k: Article extraction

- trafilatura: Web content extraction

Large data files (.csv, .json, .db) are tracked with Git LFS:- PRAW: Reddit API wrapper

- snscrape: Twitter scraping

```bash

# Install Git LFS### Agriculture Sources

git lfs install- PIB: https://pib.gov.in

- Ministry of Agriculture: https://agricoop.nic.in

# Track data files (already configured in .gitattributes)- Down to Earth: https://downtoearth.org.in

git lfs track "*.csv"- The Hindu (Agriculture section)

git lfs track "*.json"- Indian Express (Rural section)

git lfs track "*.db"



# Add and commit
git add .gitattributes
git add data/
git commit -m "Add data files with LFS"
git push
```

---

## 🐛 Troubleshooting

### Import Error: tomli

```bash
pip install tomli==2.0.1
```

### SpaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### GPU Out of Memory (Local Machine)

Use Google Colab for Steps 6-8:
1. Stop local pipeline after Step 5
2. Upload `statements.json` to Colab
3. Run `colab_pair_generation.ipynb`

### SerpAPI Quota Exceeded

- Free tier: 100 searches/month
- Upgrade or wait for quota reset
- Pipeline falls back to web scraping (slower)

### Reddit API Errors

- Check credentials in `secrets.toml`
- Verify Reddit app permissions
- Ensure user agent is correctly formatted

---

## 📈 Performance & Scalability

### Current Stats (Real Run)

- **Queries**: 43 controversy-focused queries
- **URLs Scraped**: 3,438 documents
- **Statements Extracted**: 22,198 (4,413 with opinions)
- **Pairs Generated**: 1,000+ diverse pairs
- **Time**: ~90 minutes total (60 min local + 10 min Colab + 20 min annotation)

### Scaling Up

To increase dataset size:
1. Add more queries to `config.py`
2. Increase `MAX_URLS_PER_QUERY` in `main_enhanced.py`
3. Adjust `TARGET_PAIRS` for more pair generation
4. Use more powerful GPU for faster embeddings

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **SerpAPI** for Google search API
- **Reddit API** (PRAW) for social media data
- **SpaCy** for NLP processing
- **Sentence Transformers** for semantic embeddings
- **Hugging Face** for transformer models

---

## 📧 Contact

For questions or issues:
- Open a GitHub issue
- Email: [Your email]
- GitHub: [@XAheli](https://github.com/XAheli)

---

## 🗺️ Roadmap

- [ ] Add support for Twitter/X scraping
- [ ] Implement automatic annotation suggestions
- [ ] Add data augmentation techniques
- [ ] Create fine-tuned inconsistency detection model
- [ ] Deploy as web service API
- [ ] Add multilingual support (Hindi, other Indian languages)

---

**Star ⭐ this repo if you find it useful!**
