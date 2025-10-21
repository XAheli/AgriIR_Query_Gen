"""
Enhanced main pipeline for Agriculture Inconsistency Detection Dataset Creation
Includes multi-source scraping, better extraction, and intelligent pairing
"""
import os
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Import enhanced modules
from scraping.enhanced_serp_scraper import EnhancedSERPScraper
from scraping.enhanced_content_scraper import EnhancedContentScraper
from scraping.reddit_scraper import RedditScraper
from processing.enhanced_statement_extractor import EnhancedStatementExtractor
from processing.enhanced_pair_generator import EnhancedPairGenerator
from storage.database import StatementDatabase
from annotation.export_for_annotation import AnnotationExporter
import config

def create_directories():
    """Create necessary directories"""
    for path in [config.RAW_DATA_PATH, config.PROCESSED_DATA_PATH, config.FINAL_DATA_PATH]:
        Path(path).mkdir(parents=True, exist_ok=True)
    Path('data').mkdir(exist_ok=True)
    print("✓ Directories created")

def print_header(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def save_json(data, filepath, description="data"):
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved {description} to: {filepath}")

def main():
    print_header("AGRICULTURE INCONSISTENCY DETECTION - ENHANCED PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuration - ENHANCED FOR DIVERSITY
    NUM_QUERIES = len(config.AGRICULTURE_QUERIES)  # Use ALL queries for maximum diversity
    MAX_URLS_PER_QUERY = 20  # More URLs per query
    TARGET_PAIRS = 1000  # Generate 1000 pairs, annotate best 300+
    USE_REDDIT = True  # Enable Reddit for diverse opinion statements
    
    # Create directories
    print_header("STEP 0: Setup")
    create_directories()
    
    # Initialize database
    print("\nInitializing database...")
    db = StatementDatabase()
    print("✓ Database ready")
    
    # STEP 1: SERP Scraping
    print_header("STEP 1: Google Search (SERP)")
    serp_scraper = EnhancedSERPScraper()
    
    # Select queries
    queries = config.AGRICULTURE_QUERIES[:NUM_QUERIES]
    print(f"Using {len(queries)} queries for maximum diversity:")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
    
    # Scrape search results WITHOUT strict domain filtering for better diversity
    search_results = serp_scraper.scrape_all_queries(queries, num_results=MAX_URLS_PER_QUERY, filter_domains=False)
    
    # Apply diversity filter
    search_results = serp_scraper.get_diverse_results(search_results, max_per_domain=20)
    print(f"✓ Collected {len(search_results)} diverse URLs")
    
    # Save search results
    search_df = pd.DataFrame(search_results)
    search_df.to_csv(f"{config.RAW_DATA_PATH}search_results.csv", index=False)
    print(f"✓ Saved to: {config.RAW_DATA_PATH}search_results.csv")
    
    # STEP 2: Content Scraping
    print_header("STEP 2: Content Scraping")
    content_scraper = EnhancedContentScraper()
    
    urls = [r['url'] for r in search_results]
    print(f"Scraping {len(urls)} URLs...")
    documents = content_scraper.scrape_multiple_urls(urls)
    
    # Save raw documents
    save_json(documents, f"{config.RAW_DATA_PATH}documents.json", "documents")
    
    # STEP 3: Reddit Scraping (Optional)
    if USE_REDDIT and config.REDDIT_CLIENT_ID:
        print_header("STEP 3: Reddit Scraping")
        reddit_scraper = RedditScraper()
        reddit_content = reddit_scraper.scrape_agriculture_content(
            queries[:20],  # Use 20 queries for diverse Reddit content
            max_posts_per_query=30
        )
        
        # Add to documents
        documents.extend(reddit_content)
        save_json(reddit_content, f"{config.RAW_DATA_PATH}reddit_content.json", "Reddit content")
    else:
        print_header("STEP 3: Reddit Scraping")
        print("⏭️  Skipped (Reddit API not configured or disabled)")
        print("   To enable: Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in config.py")
    
    # STEP 4: Statement Extraction
    print_header("STEP 4: Statement Extraction")
    statement_extractor = EnhancedStatementExtractor()
    
    statements, extraction_stats = statement_extractor.extract_from_multiple_documents(documents)
    
    if not statements:
        print("❌ No statements extracted. Exiting.")
        return
    
    # Save statements
    save_json(statements, f"{config.PROCESSED_DATA_PATH}statements.json", "statements")
    
    # STEP 5: Save to Database
    print_header("STEP 5: Database Storage")
    print("Saving statements to database...")
    
    statement_ids = []
    for stmt in statements:
        stmt_id = db.insert_statement(
            text=stmt['text'],
            source_url=stmt['source_url'],
            author=stmt.get('author'),
            topic='agriculture'
        )
        statement_ids.append(stmt_id)
    
    print(f"✓ Saved {len(statement_ids)} statements to database")
    
    # STEP 6: Generate Pairs
    print_header("STEP 6: Intelligent Pair Generation")
    pair_generator = EnhancedPairGenerator()
    
    # Compute embeddings
    embeddings = pair_generator.compute_embeddings(statements)
    
    # Generate pairs with stratified sampling
    pairs = pair_generator.generate_pairs(
        statements, 
        embeddings, 
        max_pairs=TARGET_PAIRS,
        use_stratified=True
    )
    
    if not pairs:
        print("❌ No pairs generated. Try lowering similarity threshold.")
        return
    
    # STEP 7: Save Pairs to Database
    print_header("STEP 7: Save Pairs to Database")
    print("Saving pairs to database...")
    
    saved_count = 0
    for pair in pairs:
        # Get or create statement IDs
        stmt_a_id = db.insert_statement(
            text=pair['statement_a']['text'],
            source_url=pair['statement_a']['source_url'],
            author=pair['statement_a'].get('author'),
            topic='agriculture'
        )
        stmt_b_id = db.insert_statement(
            text=pair['statement_b']['text'],
            source_url=pair['statement_b']['source_url'],
            author=pair['statement_b'].get('author'),
            topic='agriculture'
        )
        
        pair_id = db.insert_pair(
            stmt_a_id, 
            stmt_b_id, 
            pair['similarity_score'],
            pair['same_source']
        )
        
        if pair_id:
            saved_count += 1
    
    print(f"✓ Saved {saved_count} pairs to database")
    
    # STEP 8: Export for Annotation
    print_header("STEP 8: Export for Manual Annotation")
    exporter = AnnotationExporter(db)
    csv_path = exporter.export_to_csv()
    
    # STEP 9: Generate Summary Report
    print_header("PIPELINE COMPLETE - SUMMARY REPORT")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n📊 Collection Statistics:")
    print(f"  Queries used: {len(queries)}")
    print(f"  URLs found: {len(search_results)}")
    print(f"  Documents scraped: {len(documents)}")
    print(f"  Success rate: {len(documents)/max(len(search_results),1)*100:.1f}%")
    
    print(f"\n📝 Statement Statistics:")
    print(f"  Total statements: {extraction_stats['total_statements']}")
    print(f"  Opinion statements: {extraction_stats['opinion_statements']} ({extraction_stats['opinion_statements']/max(extraction_stats['total_statements'],1)*100:.1f}%)")
    print(f"  Avg per document: {extraction_stats['total_statements']/max(extraction_stats['documents_processed'],1):.1f}")
    
    print(f"\n🔗 Pair Statistics:")
    print(f"  Total pairs generated: {len(pairs)}")
    print(f"  Same-source pairs: {sum(1 for p in pairs if p['same_source'])}")
    print(f"  Opinion pairs: {sum(1 for p in pairs if p['both_have_opinions'])}")
    print(f"  Avg similarity: {sum(p['similarity_score'] for p in pairs)/max(len(pairs),1):.3f}")
    
    print(f"\n📁 Output Files:")
    print(f"  Search results: {config.RAW_DATA_PATH}search_results.csv")
    print(f"  Documents: {config.RAW_DATA_PATH}documents.json")
    print(f"  Statements: {config.PROCESSED_DATA_PATH}statements.json")
    print(f"  Database: {config.DATABASE_PATH}")
    print(f"  Annotation file: {csv_path}")
    
    print(f"\n📋 Next Steps:")
    print(f"  1. Open annotation file: {csv_path}")
    print(f"  2. Manually annotate 200+ pairs:")
    print(f"     - relationship_label: Unrelated/Consistent/Inconsistent")
    print(f"     - inconsistency_subtype: Surface/Factual/Value (if Inconsistent)")
    print(f"  3. Focus on pairs with 'same_source' = True for better examples")
    print(f"  4. Save annotated file for model training")
    
    print("="*80)
    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Pipeline failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
