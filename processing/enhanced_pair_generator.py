"""
Enhanced pair generator with intelligent pairing strategies
Prioritizes same-source pairs and controversial topics
"""
from sentence_transformers import SentenceTransformer, util
import numpy as np
import config

class EnhancedPairGenerator:
    def __init__(self):
        print(f"Loading Sentence Transformer model: {config.SENTENCE_TRANSFORMER_MODEL}")
        self.model = SentenceTransformer(config.SENTENCE_TRANSFORMER_MODEL)
    
    def compute_embeddings(self, statements):
        """
        Compute embeddings for all statements
        """
        texts = [s['text'] for s in statements]
        print(f"Computing embeddings for {len(texts)} statements...")
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_tensor=True)
        return embeddings
    
    def generate_all_pairs(self, statements, embeddings, similarity_threshold=None):
        """
        Generate all valid statement pairs based on semantic similarity
        """
        threshold = similarity_threshold or config.SIMILARITY_THRESHOLD
        print(f"Generating statement pairs (threshold: {threshold})...")
        
        # Compute cosine similarity matrix
        similarity_matrix = util.cos_sim(embeddings, embeddings)
        
        pairs = []
        n = len(statements)
        
        for i in range(n):
            for j in range(i+1, n):
                similarity_score = similarity_matrix[i][j].item()
                
                # Check if similarity is above threshold
                if similarity_score >= threshold:
                    
                    stmt_a = statements[i]
                    stmt_b = statements[j]
                    
                    # Check if from same source
                    same_source = (stmt_a.get('source_url') == stmt_b.get('source_url'))
                    same_author = (stmt_a.get('author') == stmt_b.get('author'))
                    
                    # Both have opinions (better for inconsistency detection)
                    both_have_opinions = (stmt_a.get('has_opinion', False) and 
                                         stmt_b.get('has_opinion', False))
                    
                    # Calculate pair quality score
                    quality_score = similarity_score
                    if same_source:
                        quality_score += 0.2  # Bonus for same source (self-inconsistency)
                    if same_author:
                        quality_score += 0.1  # Bonus for same author
                    if both_have_opinions:
                        quality_score += 0.15  # Bonus for opinion statements
                    
                    pairs.append({
                        'statement_a': stmt_a,
                        'statement_b': stmt_b,
                        'similarity_score': similarity_score,
                        'quality_score': quality_score,
                        'same_source': same_source,
                        'same_author': same_author,
                        'both_have_opinions': both_have_opinions
                    })
        
        # Sort by quality score (descending)
        pairs.sort(key=lambda x: x['quality_score'], reverse=True)
        
        print(f"Generated {len(pairs)} candidate pairs")
        
        # Print statistics
        same_source_count = sum(1 for p in pairs if p['same_source'])
        opinion_count = sum(1 for p in pairs if p['both_have_opinions'])
        print(f"  - Same source pairs: {same_source_count} ({same_source_count/max(len(pairs),1)*100:.1f}%)")
        print(f"  - Opinion pairs: {opinion_count} ({opinion_count/max(len(pairs),1)*100:.1f}%)")
        
        return pairs
    
    def filter_diverse_pairs(self, pairs, max_pairs=500, max_per_source=None):
        """
        Filter pairs to ensure diversity while prioritizing quality
        """
        max_per_source = max_per_source or config.MAX_PAIRS_PER_SOURCE
        
        selected_pairs = []
        url_combination_counts = {}
        source_counts = {}
        
        for pair in pairs:
            url_a = pair['statement_a']['source_url']
            url_b = pair['statement_b']['source_url']
            
            # Create a unique key for this URL combination
            url_key = tuple(sorted([url_a, url_b]))
            url_count = url_combination_counts.get(url_key, 0)
            
            # Track individual source usage
            source_a_count = source_counts.get(url_a, 0)
            source_b_count = source_counts.get(url_b, 0)
            
            # Apply diversity constraints
            if url_count < max_per_source:
                selected_pairs.append(pair)
                url_combination_counts[url_key] = url_count + 1
                source_counts[url_a] = source_a_count + 1
                source_counts[url_b] = source_b_count + 1
                
                if len(selected_pairs) >= max_pairs:
                    break
        
        print(f"Selected {len(selected_pairs)} diverse pairs (target: {max_pairs})")
        return selected_pairs
    
    def stratified_sampling(self, pairs, target_count=500):
        """
        Sample pairs ensuring good distribution of different types
        """
        # Separate into categories
        same_source_opinion = [p for p in pairs if p['same_source'] and p['both_have_opinions']]
        same_source_mixed = [p for p in pairs if p['same_source'] and not p['both_have_opinions']]
        diff_source_opinion = [p for p in pairs if not p['same_source'] and p['both_have_opinions']]
        diff_source_mixed = [p for p in pairs if not p['same_source'] and not p['both_have_opinions']]
        
        print(f"\n📊 Pair Distribution:")
        print(f"  Same source + opinions: {len(same_source_opinion)}")
        print(f"  Same source + mixed: {len(same_source_mixed)}")
        print(f"  Diff source + opinions: {len(diff_source_opinion)}")
        print(f"  Diff source + mixed: {len(diff_source_mixed)}")
        
        # Prioritize same-source pairs with opinions (best for inconsistency detection)
        selected = []
        
        # 50% from same source with opinions
        selected.extend(same_source_opinion[:int(target_count * 0.5)])
        
        # 25% from same source mixed
        selected.extend(same_source_mixed[:int(target_count * 0.25)])
        
        # 15% from different source with opinions
        selected.extend(diff_source_opinion[:int(target_count * 0.15)])
        
        # 10% from different source mixed
        selected.extend(diff_source_mixed[:int(target_count * 0.10)])
        
        # If we don't have enough, fill with remaining high-quality pairs
        if len(selected) < target_count:
            remaining = [p for p in pairs if p not in selected]
            selected.extend(remaining[:target_count - len(selected)])
        
        print(f"\n✓ Stratified sampling selected {len(selected)} pairs")
        return selected
    
    def generate_pairs(self, statements, embeddings, max_pairs=500, use_stratified=True):
        """
        Main method to generate pairs with all enhancements
        """
        # Generate all candidate pairs
        all_pairs = self.generate_all_pairs(statements, embeddings)
        
        if not all_pairs:
            print("⚠️  No pairs found above similarity threshold")
            return []
        
        # Apply sampling strategy
        if use_stratified and len(all_pairs) > max_pairs:
            final_pairs = self.stratified_sampling(all_pairs, max_pairs)
        else:
            final_pairs = self.filter_diverse_pairs(all_pairs, max_pairs)
        
        return final_pairs

if __name__ == "__main__":
    # Test the pair generator
    print("Enhanced Pair Generator - Test Mode")
    
    # Mock statements for testing
    test_statements = [
        {'text': 'Farmers need better MSP', 'source_url': 'url1', 'has_opinion': True},
        {'text': 'MSP should be increased', 'source_url': 'url1', 'has_opinion': True},
        {'text': 'Agriculture is important', 'source_url': 'url2', 'has_opinion': False},
    ]
    
    generator = EnhancedPairGenerator()
    embeddings = generator.compute_embeddings(test_statements)
    pairs = generator.generate_pairs(test_statements, embeddings, max_pairs=10)
    
    print(f"\nGenerated {len(pairs)} test pairs")
