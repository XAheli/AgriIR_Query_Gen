#!/usr/bin/env python3
"""
Agriculture Inconsistency Detection - Pair Generation
Standalone GPU script (converted from Colab notebook)

Usage: python generate_pairs_gpu.py

Required files:
    - data/processed/statements.json (22,198 statements)
    
Output:
    - data/final/pairs_for_annotation_[timestamp].csv
"""

import json
import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from datetime import datetime
import os
import sys


# ============================================================================
# CONFIGURATION 
# ============================================================================

class Config:
    # Model
    SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L12-v2"
    
    # Pairing parameters
    SIMILARITY_THRESHOLD = 0.3  # Minimum similarity for pairing
    MAX_PAIRS_PER_SOURCE = 100  # Max pairs from same URL combination
    
    # Target
    TARGET_PAIRS = 1000  # Generate 1000 pairs (annotate 300+)
    
    # Batch processing
    BATCH_SIZE = 128  # For embedding computation
    MAX_STATEMENTS = None  # None = use all, or set number to limit
    
    # Paths
    STATEMENTS_PATH = "data/processed/statements.json"
    OUTPUT_DIR = "data/final/"


config = Config()


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    print("="*70)
    print("AGRICULTURE INCONSISTENCY DETECTION - PAIR GENERATION")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check GPU
    print("GPU Information:")
    print("="*50)
    if torch.cuda.is_available():
        print(f"✓ GPU Available: {torch.cuda.get_device_name(0)}")
        print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print(f"✓ CUDA Version: {torch.version.cuda}")
        device = 'cuda'
    else:
        print("⚠️  No GPU available - will use CPU (slower)")
        device = 'cpu'
    print(f"\nUsing device: {device}")
    
    # Show Configuration
    print("\nConfiguration:")
    print("="*50)
    print(f"Model: {config.SENTENCE_TRANSFORMER_MODEL}")
    print(f"Similarity threshold: {config.SIMILARITY_THRESHOLD}")
    print(f"Target pairs: {config.TARGET_PAIRS}")
    print(f"Batch size: {config.BATCH_SIZE}")
    print(f"Max statements: {config.MAX_STATEMENTS or 'All'}")
    
    # Load statements
    print("\nLoading statements...")
    if not os.path.exists(config.STATEMENTS_PATH):
        print(f"❌ Error: File not found: {config.STATEMENTS_PATH}")
        sys.exit(1)
    
    with open(config.STATEMENTS_PATH, 'r', encoding='utf-8') as f:
        statements = json.load(f)
    print(f"✓ Loaded {len(statements)} statements")
    
    # Apply limit if set
    if config.MAX_STATEMENTS and len(statements) > config.MAX_STATEMENTS:
        print(f"⚠️  Limiting to {config.MAX_STATEMENTS} statements for testing")
        statements = statements[:config.MAX_STATEMENTS]
    
    # Show statistics
    print("\nDataset Statistics:")
    print("="*50)
    print(f"Total statements: {len(statements)}")
    
    opinion_count = sum(1 for s in statements if s.get('has_opinion', False))
    print(f"Opinion statements: {opinion_count} ({opinion_count/len(statements)*100:.1f}%)")
    
    unique_sources = len(set(s['source_url'] for s in statements if s.get('source_url')))
    print(f"Unique sources: {unique_sources}")
    
    domains = set(s.get('domain') for s in statements if s.get('domain'))
    print(f"Unique domains: {len(domains)}")
    
    # Show samples
    print("\nSample statements:")
    print("="*50)
    for i, stmt in enumerate(statements[:3], 1):
        print(f"{i}. {stmt['text'][:100]}...")
        print(f"   Source: {stmt.get('domain', 'Unknown')}")
        print(f"   Opinion: {stmt.get('has_opinion', False)}")
        print()
    
    # Load model
    print("Loading Sentence Transformer model...")
    model = SentenceTransformer(config.SENTENCE_TRANSFORMER_MODEL)
    
    if torch.cuda.is_available():
        model = model.to('cuda')
        print(f"✓ Model loaded on GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("✓ Model loaded on CPU")
    
    # Compute embeddings
    texts = [s['text'] for s in statements]
    print(f"\nComputing embeddings for {len(texts)} statements...")
    print("This may take 5-10 minutes with GPU...")
    
    embeddings = model.encode(
        texts,
        batch_size=config.BATCH_SIZE,
        show_progress_bar=True,
        convert_to_tensor=True,
        device=device
    )
    
    print(f"\n✓ Embeddings computed: {embeddings.shape}")
    print(f"  Dimension: {embeddings.shape[1]}")
    print(f"  Memory: {embeddings.element_size() * embeddings.nelement() / 1e6:.2f} MB")
    
    # Generate pairs
    print("\nGenerating statement pairs...")
    print("="*50)
    print("Computing similarity matrix...")
    similarity_matrix = util.cos_sim(embeddings, embeddings)
    print(f"✓ Similarity matrix: {similarity_matrix.shape}")
    
    print(f"\nFinding pairs above threshold {config.SIMILARITY_THRESHOLD}...")
    pairs = []
    n = len(statements)
    
    for i in tqdm(range(n), desc="Processing statements"):
        for j in range(i+1, n):
            similarity_score = similarity_matrix[i][j].item()
            
            if similarity_score >= config.SIMILARITY_THRESHOLD:
                stmt_a = statements[i]
                stmt_b = statements[j]
                
                same_source = (stmt_a.get('source_url') == stmt_b.get('source_url'))
                same_author = (stmt_a.get('author') == stmt_b.get('author'))
                both_have_opinions = (stmt_a.get('has_opinion', False) and 
                                     stmt_b.get('has_opinion', False))
                
                # Calculate quality score
                quality_score = similarity_score
                if same_source:
                    quality_score += 0.2
                if same_author:
                    quality_score += 0.1
                if both_have_opinions:
                    quality_score += 0.15
                
                pairs.append({
                    'statement_a': stmt_a,
                    'statement_b': stmt_b,
                    'similarity_score': similarity_score,
                    'quality_score': quality_score,
                    'same_source': same_source,
                    'same_author': same_author,
                    'both_have_opinions': both_have_opinions
                })
    
    print(f"\n✓ Generated {len(pairs)} candidate pairs")
    same_source_count = sum(1 for p in pairs if p['same_source'])
    opinion_count = sum(1 for p in pairs if p['both_have_opinions'])
    print(f"  - Same source pairs: {same_source_count} ({same_source_count/len(pairs)*100:.1f}%)")
    print(f"  - Opinion pairs: {opinion_count} ({opinion_count/len(pairs)*100:.1f}%)")
    print(f"  - Avg similarity: {np.mean([p['similarity_score'] for p in pairs]):.3f}")
    
    # Stratified sampling
    pairs.sort(key=lambda x: x['quality_score'], reverse=True)
    print("\nApplying stratified sampling...")
    print("="*50)
    
    same_source_opinion = [p for p in pairs if p['same_source'] and p['both_have_opinions']]
    same_source_mixed = [p for p in pairs if p['same_source'] and not p['both_have_opinions']]
    diff_source_opinion = [p for p in pairs if not p['same_source'] and p['both_have_opinions']]
    diff_source_mixed = [p for p in pairs if not p['same_source'] and not p['both_have_opinions']]
    
    print(f"\n📊 Pair Distribution (Before Sampling):")
    print(f"  Same source + opinions: {len(same_source_opinion)}")
    print(f"  Same source + mixed: {len(same_source_mixed)}")
    print(f"  Diff source + opinions: {len(diff_source_opinion)}")
    print(f"  Diff source + mixed: {len(diff_source_mixed)}")
    
    target = config.TARGET_PAIRS
    selected = []
    
    n_same_opinion = int(target * 0.5)
    selected.extend(same_source_opinion[:n_same_opinion])
    print(f"\n✓ Selected {len(selected)} same-source opinion pairs (target: {n_same_opinion}, 50%)")
    
    n_same_mixed = int(target * 0.25)
    selected.extend(same_source_mixed[:n_same_mixed])
    print(f"✓ Added {min(len(same_source_mixed), n_same_mixed)} same-source mixed pairs (target: {n_same_mixed}, 25%)")
    
    n_diff_opinion = int(target * 0.15)
    selected.extend(diff_source_opinion[:n_diff_opinion])
    print(f"✓ Added {min(len(diff_source_opinion), n_diff_opinion)} diff-source opinion pairs (target: {n_diff_opinion}, 15%)")
    
    n_diff_mixed = int(target * 0.10)
    selected.extend(diff_source_mixed[:n_diff_mixed])
    print(f"✓ Added {min(len(diff_source_mixed), n_diff_mixed)} diff-source mixed pairs (target: {n_diff_mixed}, 10%)")
    
    if len(selected) < target:
        remaining = [p for p in pairs if p not in selected]
        needed = target - len(selected)
        selected.extend(remaining[:needed])
        print(f"✓ Added {min(len(remaining), needed)} remaining high-quality pairs")
    
    print(f"\n✓ Final selection: {len(selected)} pairs (target was {target})")
    
    # Diversity filtering
    print("\nApplying diversity filtering...")
    print("="*50)
    
    url_combination_counts = {}
    source_counts = {}
    diverse_pairs = []
    
    for pair in selected:
        url_a = pair['statement_a'].get('source_url', '')
        url_b = pair['statement_b'].get('source_url', '')
        
        url_key = tuple(sorted([url_a, url_b]))
        url_count = url_combination_counts.get(url_key, 0)
        
        source_a_count = source_counts.get(url_a, 0)
        source_b_count = source_counts.get(url_b, 0)
        
        if url_count < config.MAX_PAIRS_PER_SOURCE:
            diverse_pairs.append(pair)
            url_combination_counts[url_key] = url_count + 1
            source_counts[url_a] = source_a_count + 1
            source_counts[url_b] = source_b_count + 1
    
    print(f"✓ After diversity filtering: {len(diverse_pairs)} pairs")
    print(f"  Unique URL combinations: {len(url_combination_counts)}")
    print(f"  Unique sources: {len(source_counts)}")
    
    final_pairs = diverse_pairs
    
    # Export
    print("\nPreparing export...")
    print("="*50)
    
    export_data = []
    for i, pair in enumerate(final_pairs, 1):
        export_data.append({
            'id': i,
            'statement_a': pair['statement_a']['text'],
            'statement_b': pair['statement_b']['text'],
            'similarity_score': round(pair['similarity_score'], 3),
            'quality_score': round(pair['quality_score'], 3),
            'same_source': pair['same_source'],
            'both_have_opinions': pair['both_have_opinions'],
            'source_a': pair['statement_a'].get('source_url', ''),
            'source_b': pair['statement_b'].get('source_url', ''),
            'domain_a': pair['statement_a'].get('domain', ''),
            'domain_b': pair['statement_b'].get('domain', ''),
            'author_a': pair['statement_a'].get('author', ''),
            'author_b': pair['statement_b'].get('author', ''),
            'relationship_label': '',
            'inconsistency_subtype': '',
            'notes': ''
        })
    
    df = pd.DataFrame(export_data)
    
    # Create output directory
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Save files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(config.OUTPUT_DIR, f'pairs_for_annotation_{timestamp}.csv')
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"\n✓ Exported {len(df)} pairs to: {filename}")
    
    # Also save JSON
    json_filename = filename.replace('.csv', '.json')
    df.to_json(json_filename, orient='records', indent=2)
    print(f"✓ Also saved as: {json_filename}")
    
    # Save sample
    sample_filename = filename.replace('.csv', '_sample_50.csv')
    df.head(50).to_csv(sample_filename, index=False)
    print(f"✓ Sample (50 pairs) saved: {sample_filename}")
    
    # Summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETE - SUMMARY REPORT")
    print("="*70)
    print(f"\n📊 Final Statistics:")
    print(f"  Total statements processed: {len(statements):,}")
    print(f"  Candidate pairs generated: {len(pairs):,}")
    print(f"  Final pairs exported: {len(final_pairs):,}")
    
    print(f"\n🔍 Pair Quality:")
    same_src = sum(1 for p in final_pairs if p['same_source'])
    opinions = sum(1 for p in final_pairs if p['both_have_opinions'])
    print(f"  Same-source pairs: {same_src} ({same_src/len(final_pairs)*100:.1f}%)")
    print(f"  Opinion pairs: {opinions} ({opinions/len(final_pairs)*100:.1f}%)")
    print(f"  Avg similarity: {np.mean([p['similarity_score'] for p in final_pairs]):.3f}")
    print(f"  Avg quality score: {np.mean([p['quality_score'] for p in final_pairs]):.3f}")
    
    print(f"\n📝 Annotation Guidelines:")
    print("  relationship_label options:")
    print("    - Unrelated: Different topics")
    print("    - Consistent: Both can be true")
    print("    - Inconsistent: Contradictory")
    print("\n  inconsistency_subtype (if Inconsistent):")
    print("    - Surface: Direct logical contradiction")
    print("    - Factual: Conflicting facts/numbers")
    print("    - Value: Conflicting values/opinions")
    
    print(f"\n📋 Next Steps:")
    print(f"  1. Open: {filename}")
    print(f"  2. Manually annotate 300+ pairs")
    print(f"  3. Prioritize same_source=True pairs")
    print(f"  4. Focus on both_have_opinions=True pairs")
    
    print("\n" + "="*70)
    print("✅ SUCCESS - Ready for annotation!")
    print("="*70)
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
