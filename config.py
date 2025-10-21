"""
Configuration file for Agriculture Inconsistency Detection Project
"""

# Agriculture-related search queries for Indian context
AGRICULTURE_QUERIES = [
    # Farm Laws & Policy Controversies
    "farm laws 2020 India benefits drawbacks debate",
    "farm bills India farmers protest controversy",
    "MSP guarantee India debate government farmers",
    "APMC mandi system reform India opposition support",
    "farm laws repeal India government decision reasons",
    "agricultural reforms India success failure debate",
    
    # MSP & Pricing Controversies
    "MSP minimum support price India increase decrease debate",
    "MSP legal guarantee India feasibility concerns",
    "crop pricing India government vs farmers demand",
    "MSP announcement India wheat rice pulses changes",
    "procurement system India farmers complaints benefits",
    
    # Subsidies & Support Schemes
    "agricultural subsidies India increase cut debate",
    "PM-KISAN scheme India success failure criticism",
    "farm loan waiver India impact economy farmers",
    "fertilizer subsidy India government policy changes",
    "crop insurance India PMFBY claims rejection controversy",
    
    # Farmer challenges
    "Indian farmer problems crop failure",
    "agricultural debt crisis India farmers",
    "irrigation problems Indian agriculture",
    "fertilizer shortage India farmers",
    "pesticide usage issues Indian farming",


    # Economic Debates
    "farmer income doubling India achieved failed target",
    "agricultural exports India ban promotion policy flip",
    "food grain procurement India quantity prices controversy",
    "agriculture GDP contribution India growth decline debate",
    "contract farming India farmers exploitation benefits",
    
    # Environmental & Sustainability Debates
    "stubble burning India ban enforcement farmers plight",
    "organic farming India promotion challenges profitability",
    "pesticide use India harmful necessary debate",
    "water crisis agriculture India groundwater depletion solutions",
    "climate change agriculture India adaptation mitigation debate",
    
    # Technology & Modernization
    "farm mechanization India employment displacement benefits",
    "GM crops India ban approval safety controversy",
    "drone technology farming India permission restrictions",
    "digital agriculture India success accessibility concerns",
    
    # Farmer Welfare Debates
    "farmer suicide India rates causes government failure",
    "agricultural debt crisis India loan waiver solution",
    "farmer protests India valid unjustified debate",
    "agriculture distress India real exaggerated controversy",
    
    # Land & Resources
    "land acquisition India farmers compensation controversy",
    "agricultural land conversion India urbanization debate",
    "water allocation agriculture industry India conflict",
    "irrigation projects India benefits displacement issues",
]

# Target websites for agriculture content
TARGET_DOMAINS = [
    "www.pib.gov.in",  # Press Information Bureau
    "www.agricoopnic.com",  # Ministry of Agriculture
    "www.agriwelfare.gov.in",  # Ministry of Agriculture
    "www.fssai.gov.in",  # Food Safety and Standards Authority of India
    "www.niti.gov.in",  # NITI Aayog
    "www.msme.gov.in",  # Ministry of Micro, Small & Medium Enterprises
    "www.midh.gov.in",  # Ministry of Food Processing Industries
    "www.nhb.gov.in",  # National Horticulture Board
    "www.apeda.gov.in",  # Agricultural and Processed Food Products Export Development Authority
    "www.afsti.org",  # Association of Food Scientists and Technologists India
    "www.cftri.com",  # Central Food Technological Research Institute
    "www.mofpi.nic.in",  # Ministry of Food Processing Industries
    "www.nabard.org",  # National Bank for Agriculture and Rural Development
    "www.thewire.in",
    "www.drishtiias.com",
    "krishijagran.com",
    "www.thehindu.com",
    "www.indianexpress.com",
    "www.downtoearth.org.in",
    "www.economictimes.com",
    "www.business-standard.com",
]

# Database configuration
DATABASE_PATH = "data/agriculture_statements.db"

# Processing parameters
MAX_STATEMENT_LENGTH = 500  # Maximum characters per statement
MIN_STATEMENT_LENGTH = 20   # Minimum characters per statement
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity for pairing (0-1)
MAX_PAIRS_PER_SOURCE = 100  # Maximum pairs from single source

# Sentence Transformer model
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L12-v2"

# SpaCy model (run: python -m spacy download en_core_web_sm)
SPACY_MODEL = "en_core_web_sm"

# Scraping parameters
MAX_PAGES_PER_QUERY = 1  # First page only
SCRAPE_DELAY = 2  # Seconds between requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Output paths
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
FINAL_DATA_PATH = "data/final/"

# API Keys - Load from secrets.toml
# Create secrets.toml file with your API keys (see secrets.toml.example)
import tomli
from pathlib import Path

def load_secrets():
    """Load API keys from secrets.toml"""
    secrets_path = Path(__file__).parent / "secrets.toml"
    if secrets_path.exists():
        with open(secrets_path, "rb") as f:
            return tomli.load(f)
    else:
        print("⚠️  WARNING: secrets.toml not found. API features will be disabled.")
        return {"api": {}, "reddit": {}}

_secrets = load_secrets()

# API Keys
SERP_API_KEY = _secrets.get("api", {}).get("serp_api_key", "")
REDDIT_CLIENT_ID = _secrets.get("reddit", {}).get("client_id", "")
REDDIT_CLIENT_SECRET = _secrets.get("reddit", {}).get("client_secret", "")
REDDIT_USER_AGENT = _secrets.get("reddit", {}).get("user_agent", "python:agriculture_scraper:v1.0")
