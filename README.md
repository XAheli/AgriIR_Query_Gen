# Agriculture Inconsistency Detection Dataset# Agriculture Inconsistency Detection Dataset# Agriculture Inconsistency Detection - Setup & Usage Guide



[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)## 📋 Project Overview

## 📋 Project Overview

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive pipeline for creating an **Indian Agriculture Inconsistency Detection Dataset**. This project scrapes diverse sources, extracts agriculture-related statements using NLP, and generates intelligent statement pairs for manual annotation.

This project creates a dataset for detecting inconsistencies in statements about Indian agriculture. It:

**Goal**: Create 300+ high-quality annotated statement pairs to train inconsistency detection models.

## 📋 Project Overview1. **Scrapes** diverse sources (Google, articles, Reddit, social media)

### What This Does

2. **Extracts** agriculture-related statements using NLP

1. 🔍 **Multi-Source Scraping**: Google search (via SerpAPI), web articles, Reddit discussions

2. 🧠 **NLP Processing**: SpaCy-based statement extraction with opinion detectionA comprehensive pipeline for creating an **Indian Agriculture Inconsistency Detection Dataset**. This project scrapes diverse sources, extracts agriculture-related statements using NLP, and generates intelligent statement pairs for manual annotation.3. **Generates** smart statement pairs based on semantic similarity

3. 🔗 **Intelligent Pairing**: Sentence Transformers for semantic similarity with stratified sampling

4. 📊 **Export for Annotation**: CSV format with metadata for manual labeling4. **Exports** pairs for manual annotation



### Task Definition**Goal**: Create 300+ high-quality annotated statement pairs to train inconsistency detection models.



Classify relationships between agriculture statement pairs:**Goal**: Create 200+ annotated statement pairs to train an inconsistency detection model.



- **Unrelated**: Statements discuss different topics### What This Does

- **Consistent**: Both statements can be true, support similar conclusions

- **Inconsistent**: Statements contradict each other## 🎯 Task Definition

  - *Surface contradiction*: Direct logical contradiction

  - *Factual inconsistency*: Conflicting facts/statistics1. 🔍 **Multi-Source Scraping**: Google search results (SerpAPI), web articles, Reddit discussions

  - *Value inconsistency*: Conflicting values/policy positions

2. 🧠 **NLP Processing**: SpaCy-based statement extraction with opinion detectionClassify relationship between statement pairs as:

---

3. 🔗 **Intelligent Pairing**: Sentence Transformers for semantic similarity, stratified sampling for diversity- **Unrelated**: Different topics

## 🚀 Quick Start

4. 📊 **Export for Annotation**: CSV format with metadata for manual labeling- **Consistent**: Compatible statements

### Prerequisites

- **Inconsistent**: Contradictory statements

- Python 3.11+

- Virtual environment (recommended)### Task Definition  - *Surface contradiction*: Direct logical contradiction

- Git LFS installed (for data files)

  - *Factual inconsistency*: Conflicting facts/numbers

### 1. Clone Repository

Classify relationships between agriculture statement pairs:  - *Value inconsistency*: Conflicting values/policies

```bash

git clone git@github.com:XAheli/AgriIR_Query_Gen.git

cd AgriIR_Query_Gen

```- **Unrelated**: Statements discuss different topics## 🚀 Quick Start



### 2. Install Dependencies- **Consistent**: Both statements can be true, support similar conclusions



```bash- **Inconsistent**: Statements contradict each other### 1. Install Dependencies

# Create and activate virtual environment

python -m venv .venv  - *Surface contradiction*: Direct logical contradiction

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

  - *Factual inconsistency*: Conflicting facts/statistics```bash

# Install packages

pip install -r requirements.txt  - *Value inconsistency*: Conflicting values/policy positions# Create virtual environment (recommended)



# Download SpaCy modelpython -m venv venv

python -m spacy download en_core_web_sm

```---source venv/bin/activate  # On Windows: venv\Scripts\activate



### 3. Configure API Keys (Optional but Recommended)



Create `secrets.toml` with your API keys:## 🚀 Quick Start# Install requirements



```tomlpip install -r requirements.txt

[api]

serp_api_key = "your_serpapi_key_here"  # Get from serpapi.com (100 free/month)### Prerequisites



[reddit]# Download SpaCy model

client_id = "your_reddit_client_id"

client_secret = "your_reddit_client_secret"- Python 3.11+python -m spacy download en_core_web_sm

user_agent = "python:agriculture_scraper:v1.0 (by /u/YourUsername)"

```- Virtual environment (recommended)```



**Without API keys**: Pipeline will use web scraping fallbacks (slower, less reliable).- Git LFS installed (for data files)



### 4. Run the Pipeline### 2. Configure (Optional)



```bash### 1. Clone Repository

source .venv/bin/activate

python main_enhanced.pyEdit `config.py` to:

```

```bash- Add more agriculture queries

⚠️ **Note**: The pipeline may hang at Step 6 (embedding computation) due to GPU/memory limitations. See "GPU Issue Workaround" below if this happens.

git clone git@github.com:XAheli/AgriIR_Query_Gen.git- Configure target domains

---

cd AgriIR_Query_Gen- Set API keys (optional, for better results)

## 📂 Project Structure

```

```

agriculture_inconsistency_detection/```python

├── main_enhanced.py              # Main pipeline orchestrator

├── config.py                     # Configuration (queries, parameters, loads secrets)### 2. Install Dependencies# For better Google scraping (100 free searches/month)

├── secrets.toml                  # API keys (DO NOT COMMIT - not in repo)

├── requirements.txt              # Python dependenciesSERP_API_KEY = "your_serpapi_key"  # Get from serpapi.com

│

├── scraping/                     # Data collection modules```bash

│   ├── enhanced_serp_scraper.py  # Google search with SerpAPI

│   ├── enhanced_content_scraper.py # Multi-strategy content extraction# Create and activate virtual environment# For Reddit scraping (optional)

│   └── reddit_scraper.py         # Reddit posts & comments

│python -m venv .venvREDDIT_CLIENT_ID = "your_client_id"

├── processing/                   # NLP processing modules

│   ├── enhanced_statement_extractor.py  # SpaCy + opinion detectionsource .venv/bin/activate  # On Windows: .venv\Scripts\activateREDDIT_CLIENT_SECRET = "your_client_secret"

│   └── enhanced_pair_generator.py       # Semantic similarity pairing

│# Get from: https://www.reddit.com/prefs/apps

├── storage/                      # Database management

│   └── database.py               # SQLite operations# Install packages```

│

├── annotation/                   # Export utilitiespip install -r requirements.txt

│   └── export_for_annotation.py # CSV/JSON exporters

│### 3. Run the Pipeline

└── data/                         # Generated data (tracked with Git LFS)

    ├── raw/                      # Scraped content# Download SpaCy model

    │   ├── search_results.csv

    │   ├── documents.jsonpython -m spacy download en_core_web_sm```bash

    │   └── reddit_content.json

    ├── processed/                # Extracted statements```# Use enhanced pipeline (recommended)

    │   └── statements.json

    ├── final/                    # Annotated pairspython main_enhanced.py

    │   └── pairs_for_annotation_*.csv

    └── agriculture_statements.db # SQLite database### 3. Configure API Keys (Optional but Recommended)

```

# Or use basic pipeline

---

Create `secrets.toml` from the example:python main.py

## 📊 Pipeline Steps

```

The pipeline has **8 steps** divided into two parts:

```bash

### Part 1: Data Collection (Steps 1-5)

cp secrets.toml.example secrets.toml## 📦 What Gets Generated

**Runs on: Local machine**

```

1. **SERP Scraping**: Query Google for agriculture-related content using 43 controversy-focused queries

2. **Content Extraction**: Scrape full text from URLs using multi-strategy extractionAfter running the pipeline, you'll have:

3. **Reddit Scraping**: Collect posts and comments from 10 agriculture-related subreddits

4. **Statement Extraction**: Use SpaCy to extract sentences, detect opinions, filter for relevanceEdit `secrets.toml` and add your API keys:

5. **Database Storage**: Save statements to SQLite database

```

**Expected Output**:

- ~3,400+ documents scraped```tomldata/

- ~22,000+ statements extracted

- ~4,400+ opinion statements (19.9%)[api]├── raw/

- Runtime: 30-60 minutes

serp_api_key = "your_serpapi_key_here"  # Get from serpapi.com (100 free/month)│   ├── search_results.csv      # Google search results

### Part 2: Pair Generation (Steps 6-8)

│   ├── documents.json          # Scraped article content

**GPU-intensive - May crash on local machines**

[reddit]│   └── reddit_content.json     # Reddit posts/comments (if enabled)

6. **Embedding Computation**: Generate semantic embeddings using Sentence Transformers

7. **Intelligent Pairing**: client_id = "your_reddit_client_id"├── processed/

   - Compute cosine similarity matrix

   - Quality scoring (bonus for same-source, opinions)client_secret = "your_reddit_client_secret"│   └── statements.json         # Extracted statements

   - Stratified sampling (50% same-source opinions, 25% same-source mixed, etc.)

   - Diversity filtering (max 100 pairs per URL combo)user_agent = "python:agriculture_scraper:v1.0 (by /u/YourUsername)"├── final/

8. **Export**: Generate CSV with annotation columns

```│   └── pairs_for_annotation_[timestamp].csv  # Ready for annotation

**Expected Output**:

- 1,000+ diverse statement pairs ready for annotation└── agriculture_statements.db   # SQLite database



---**Without API keys**: The pipeline will still work using web scraping fallbacks (slower, less reliable).```



## 🔧 GPU Issue Workaround



If your computer hangs/crashes at Step 6 (embedding computation), you have two options:### 4. Run the Pipeline## 📝 Manual Annotation



### Option A: Wait for Step 5 to Complete, Then Stop



```bash#### Option A: Local Machine (Steps 1-5 only)1. **Open** the CSV file in `data/final/`

# Run pipeline

python main_enhanced.py2. **Review** each pair and fill columns:



# Wait for console message: "Step 5 completed: 22,198 statements saved to database"```bash   - `relationship_label`: Unrelated/Consistent/Inconsistent

# Then press Ctrl+C to stop before Step 6

```source .venv/bin/activate   - `inconsistency_subtype`: Surface/Factual/Value (if Inconsistent)



Your data is saved in:python main_enhanced.py   - `notes`: Any observations

- `data/processed/statements.json` (22,198 statements)

- `data/agriculture_statements.db` (SQLite database)```



You can manually create pairs later or skip Steps 6-8 if you only need the statements.3. **Prioritize** pairs where `same_source = True` (self-inconsistency)



### Option B: Use Google Colab (Not Provided)⚠️ **Note**: Steps 6-8 (embedding computation) require GPU resources. Your local machine may hang/crash at Step 6.4. **Target** 200+ annotated pairs for quality dataset



If you need the pair generation functionality, you would need to:

1. Create a Jupyter notebook for Steps 6-8

2. Upload `statements.json` to Google Colab#### Option B: Complete Pipeline with Google Colab (Recommended)### Annotation Guidelines

3. Run embedding computation with GPU (T4 or better)

4. Download generated pairs CSV



---**Steps 1-5 (Local - Data Collection):**#### Unrelated



## 🔧 Configuration```bash- Statements discuss completely different topics



### Key Parameters in `config.py`source .venv/bin/activate- No logical connection



```pythonpython main_enhanced.py- Example: "MSP increased" vs "Cotton prices fell"

# Queries - 43 controversy-focused queries on Indian agriculture

AGRICULTURE_QUERIES = [...]  # Farm laws, MSP, subsidies, reforms, etc.# Wait for "Step 5 completed" message, then stop (Ctrl+C) if it hangs at Step 6



# Similarity threshold for pairing (0-1)```#### Consistent

SIMILARITY_THRESHOLD = 0.3  # Lower = more pairs but less similar

- Both can be true simultaneously

# Maximum pairs from single URL combination

MAX_PAIRS_PER_SOURCE = 100  # For diversity**Steps 6-8 (Colab - Pair Generation):**- Support similar conclusions



# Sentence Transformer model1. Upload `colab_pair_generation.ipynb` to Google Colab- Example: "Farmers need support" vs "Agricultural subsidies help farmers"

SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L12-v2"

2. Upload `data/processed/statements.json` (generated from Steps 1-5)

# Target domains - 20+ sites including government, news, agriculture portals

TARGET_DOMAINS = [...]3. Enable GPU: Runtime → Change runtime type → GPU (T4)#### Inconsistent Types

```

4. Run all cells

### Customization

5. Download generated CSV file**Surface Contradiction**

Edit `config.py` to:

- Add/modify agriculture queries (focus on controversies for better inconsistencies)- Direct logical contradiction

- Change target domains for different source types

- Adjust similarity threshold (lower = more pairs)**Expected Time**:- Both cannot be true

- Configure scraping parameters (delays, user agent)

- Local Steps 1-5: 30-60 minutes (depends on network speed)- Example: "MSP increased by 10%" vs "MSP decreased this year"

Edit `main_enhanced.py` to:

- Change number of queries used (default: all 43)- Colab Steps 6-8: 5-10 minutes with GPU

- Adjust max URLs per query (default: 50)

- Set target pair count (default: 1000)**Factual Inconsistency**

- Enable/disable Reddit scraping (default: enabled)

---- Conflicting facts, numbers, or data

---

- Example: "1000 farmers" vs "5000 farmers" (same event)

## 📝 Annotation Guide

## 📂 Project Structure

### CSV Format

**Value Inconsistency**

The exported CSV (`data/final/pairs_for_annotation_*.csv`) contains:

```- Conflicting values, opinions, or policy positions

| Column | Description |

|--------|-------------|agriculture_inconsistency_detection/- Example: "Farm laws benefit farmers" vs "Farm laws harm farmers"

| `id` | Unique pair identifier |

| `statement_a` | First statement text |├── main_enhanced.py              # Main pipeline orchestrator

| `statement_b` | Second statement text |

| `similarity_score` | Semantic similarity (0-1) |├── config.py                     # Configuration (queries, parameters)## 🔧 Customization

| `quality_score` | Quality score with bonuses |

| `same_source` | Both from same URL? |├── secrets.toml                  # API keys (DO NOT COMMIT)

| `both_have_opinions` | Both contain opinions? |

| `source_a` / `source_b` | Source URLs |├── secrets.toml.example          # Template for secrets### Add More Queries

| `domain_a` / `domain_b` | Domain names |

| `author_a` / `author_b` | Authors (if available) |├── requirements.txt              # Python dependencies

| `relationship_label` | **[TO FILL]** Unrelated/Consistent/Inconsistent |

| `inconsistency_subtype` | **[TO FILL]** Surface/Factual/Value (if Inconsistent) |├── colab_pair_generation.ipynb   # Google Colab notebook for Steps 6-8Edit `config.py`:

| `notes` | Optional observations |

│

### Annotation Instructions

├── scraping/                     # Data collection modules```python

1. **Prioritize**: Start with pairs where `same_source=True` and `both_have_opinions=True`

2. **Label `relationship_label`**:│   ├── enhanced_serp_scraper.py  # Google search with SerpAPIAGRICULTURE_QUERIES = [

   - `Unrelated`: Completely different topics

   - `Consistent`: Can both be true│   ├── enhanced_content_scraper.py # Multi-strategy content extraction    "your custom query 1",

   - `Inconsistent`: Contradictory

3. **If Inconsistent, label `inconsistency_subtype`**:│   └── reddit_scraper.py         # Reddit posts & comments    "your custom query 2",

   - `Surface`: Direct logical contradiction

   - `Factual`: Conflicting facts/numbers│    # Add more...

   - `Value`: Conflicting opinions/values

4. **Add notes**: Any observations to help with model training├── processing/                   # NLP processing modules]



**Target**: Annotate 300+ pairs for robust dataset.│   ├── enhanced_statement_extractor.py  # SpaCy + opinion detection```



### Annotation Examples│   └── enhanced_pair_generator.py       # Semantic similarity pairing



**Inconsistent - Surface:**│### Adjust Similarity Threshold

- A: "Farm laws were repealed in 2021"

- B: "Farm laws are still in effect"├── storage/                      # Database management



**Inconsistent - Factual:**│   └── database.py               # SQLite operationsLower threshold = more pairs (but less similar):

- A: "MSP increased by 10%"

- B: "MSP decreased by 5%" (same year/crop)│



**Inconsistent - Value:**├── annotation/                   # Export utilities```python

- A: "Farm laws benefit small farmers"

- B: "Farm laws harm small farmers"│   └── export_for_annotation.py # CSV/JSON exportersSIMILARITY_THRESHOLD = 0.2  # Default: 0.3



**Consistent:**│```

- A: "Farmers need better MSP"

- B: "Agricultural support prices should increase"└── data/                         # Generated data (tracked with Git LFS)



---    ├── raw/                      # Scraped content### Change Target Pair Count



## 🔒 Security & Privacy    │   ├── search_results.csv



### API Keys    │   ├── documents.jsonIn `main_enhanced.py`:



- **secrets.toml is NOT in the repository** (protected by .gitignore)    │   └── reddit_content.json

- `config.py` safely loads secrets at runtime using `tomli`

- Never commit `secrets.toml` to version control    ├── processed/                # Extracted statements```python

- Get your own API keys:

  - SerpAPI: https://serpapi.com (100 free searches/month)    │   └── statements.jsonTARGET_PAIRS = 1000  # Default: 500

  - Reddit: https://www.reddit.com/prefs/apps

    └── final/                    # Annotated pairs```

### Data Privacy

        └── pairs_for_annotation_*.csv

- All scraped content is from public sources

- Reddit scraping follows API terms of service```## 🛠️ Troubleshooting

- Respects `robots.txt` and rate limits

- No personal data collection



------### Issue: Google Blocking Requests



## 📦 Git LFS



Large data files (.csv, .json, .db) are tracked with Git LFS:## 🔧 Configuration**Solution 1**: Use SerpAPI (recommended)



```bash- Sign up at https://serpapi.com (100 free searches/month)

# Already configured in .gitattributes

# Files are automatically managed by Git LFS### Key Parameters in `config.py`- Add API key to `config.py`



# To download data files after cloning

git lfs pull

``````python**Solution 2**: Increase delays



---# Number of queries to use (43 controversy-focused queries available)```python



## 🐛 TroubleshootingAGRICULTURE_QUERIES = [...]  # 43 queries covering farm laws, MSP, subsidies, etc.SCRAPE_DELAY = 5  # Increase from 2



### Import Error: tomli```



```bash# Similarity threshold for pairing (0-1)

pip install tomli==2.0.1

```SIMILARITY_THRESHOLD = 0.3**Solution 3**: Use Selenium (slower but more reliable)



### SpaCy Model Not Found- Already in requirements



```bash# Maximum pairs from single URL combination- Modify scraper to use Selenium

python -m spacy download en_core_web_sm

```MAX_PAIRS_PER_SOURCE = 100



### Warning: secrets.toml not found### Issue: No Statements Extracted



This is normal if you haven't created `secrets.toml` yet. The pipeline will work without it using web scraping fallbacks, but:# Sentence Transformer model

- Google scraping will be slower and less reliable

- Reddit scraping will be disabledSENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L12-v2"**Cause**: Scraping failed or content quality poor



Create `secrets.toml` with your API keys to enable full functionality.```



### Pipeline Hangs at Step 6**Solutions**:



**Expected behavior** - embedding computation requires significant GPU/memory. Options:### Customization- Check `data/raw/documents.json` to verify content

1. Let Step 5 complete, then stop (Ctrl+C)

2. Use a machine with better GPU/memory- Lower `MIN_STATEMENT_LENGTH` in config

3. Modify code to process in smaller batches

Edit `config.py` to:- Add more/better queries

### No Statements Extracted

- Add/modify agriculture queries (focus on controversies for better inconsistencies)- Target specific trusted domains

**Causes**:

- Scraping failed (check `data/raw/documents.json`)- Change target domains (government sites, news outlets, etc.)

- Content quality poor

- Filters too strict- Adjust similarity thresholds### Issue: No Pairs Generated



**Solutions**:- Configure scraping parameters

- Verify API keys in `secrets.toml`

- Check internet connection**Cause**: Statements too dissimilar

- Lower `MIN_STATEMENT_LENGTH` in `config.py`

- Add more/better queries---



### SerpAPI Quota Exceeded**Solutions**:



- Free tier: 100 searches/month## 📊 Pipeline Steps- Lower `SIMILARITY_THRESHOLD` in config (try 0.2)

- Wait for quota reset or upgrade plan

- Pipeline automatically falls back to web scraping- Collect more statements (use more queries/URLs)



---### Steps 1-5: Data Collection (Local Machine)- Focus queries on specific controversial topics



## 📈 Performance Stats (Real Run)



- **Queries Used**: 43 controversy-focused queries1. **SERP Scraping**: Query Google for agriculture-related content### Issue: Too Many Pairs

- **URLs Found**: ~3,400+

- **Documents Scraped**: 3,438 (success rate varies by source)2. **Content Extraction**: Scrape full text from URLs using multi-strategy extraction

- **Statements Extracted**: 22,198 total

- **Opinion Statements**: 4,413 (19.9%)3. **Reddit Scraping**: Collect posts and comments from agriculture subreddits**Solution**: Filter more aggressively

- **Average Statements/Document**: 6.5

- **Runtime**: ~60 minutes for Steps 1-54. **Statement Extraction**: Extract sentences with SpaCy, detect opinions, filter for relevance```python



---5. **Database Storage**: Save statements to SQLite databaseMAX_PAIRS_PER_SOURCE = 50  # Default: 100



## 🤝 Contributing```



Contributions welcome! Please:**Output**: 

1. Fork the repository

2. Create a feature branch- ~3,400+ documents## 📊 Pipeline Parameters

3. Make your changes

4. Submit a pull request- ~22,000+ statements



---- ~4,400+ opinion statements (19.9%)Edit these in `main_enhanced.py`:



## 📄 License



MIT License - See LICENSE file for details### Steps 6-8: Pair Generation (Google Colab GPU)```python



---NUM_QUERIES = 10              # Number of queries to use



## 🙏 Acknowledgments6. **Embedding Computation**: Generate semantic embeddings using Sentence Transformers (GPU-accelerated)MAX_URLS_PER_QUERY = 10      # URLs to scrape per query



- **SerpAPI** for Google search API7. **Intelligent Pairing**: TARGET_PAIRS = 500            # Target pair count

- **Reddit API** (PRAW) for social media data

- **SpaCy** for NLP processing   - Compute cosine similarity matrixUSE_REDDIT = False            # Enable Reddit scraping

- **Sentence Transformers** for semantic embeddings

- **Hugging Face** for transformer models   - Quality scoring (bonus for same-source, opinions)```



---   - Stratified sampling (50% same-source opinions, 25% same-source mixed, etc.)



## 📧 Contact   - Diversity filtering (max 100 pairs per URL combo)## 🎓 Tips for Better Results



- GitHub Issues: [Report bugs or request features](https://github.com/XAheli/AgriIR_Query_Gen/issues)8. **Export**: Generate CSV with annotation columns

- GitHub: [@XAheli](https://github.com/XAheli)

### 1. Target Controversial Topics

---

**Output**: Focus queries on topics with multiple viewpoints:

## 🗺️ Future Enhancements

- 1,000+ diverse statement pairs- Farm laws debate

- [ ] Add support for Twitter/X scraping

- [ ] Implement automatic annotation suggestions- Ready for manual annotation- MSP policy changes

- [ ] Create fine-tuned inconsistency detection model

- [ ] Add multilingual support (Hindi, regional languages)- Subsidy programs

- [ ] Deploy as web service API

---- Agricultural reforms

---



**Star ⭐ this repo if you find it useful!**

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
