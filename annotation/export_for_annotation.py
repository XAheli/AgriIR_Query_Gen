"""
Export statement pairs for manual annotation
"""
import pandas as pd
import json
import config
from datetime import datetime

class AnnotationExporter:
    def __init__(self, db):
        self.db = db
    
    def export_to_csv(self, output_path=None):
        """
        Export pairs to CSV for manual annotation
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{config.FINAL_DATA_PATH}pairs_for_annotation_{timestamp}.csv"
        
        # Get all pairs from database
        pairs_df = self.db.get_all_pairs()
        
        # Prepare annotation columns
        pairs_df['relationship_label'] = ''  # To be filled: Unrelated/Consistent/Inconsistent
        pairs_df['inconsistency_subtype'] = ''  # To be filled if Inconsistent
        pairs_df['notes'] = ''
        
        # Reorder columns for annotation
        columns = [
            'id',
            'statement_a',
            'statement_b',
            'similarity_score',
            'same_source',
            'source_a',
            'source_b',
            'author_a',
            'author_b',
            'topic_a',
            'topic_b',
            'relationship_label',
            'inconsistency_subtype',
            'notes'
        ]
        
        pairs_df = pairs_df[columns]
        
        # Save to CSV
        pairs_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Exported {len(pairs_df)} pairs to: {output_path}")
        print(f"\nAnnotation Guidelines:")
        print("  relationship_label options:")
        print("    - Unrelated: Statements discuss different topics")
        print("    - Consistent: Both can be true, support similar conclusions")
        print("    - Inconsistent: Contradictory or conflicting")
        print("\n  inconsistency_subtype (if Inconsistent):")
        print("    - Surface contradiction: Direct logical contradiction")
        print("    - Factual inconsistency: Conflicting facts/statistics")
        print("    - Value inconsistency: Conflicting values/policy positions")
        
        return output_path
    
    def export_to_json(self, output_path=None):
        """
        Export pairs to JSON format (alternative format)
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{config.FINAL_DATA_PATH}pairs_for_annotation_{timestamp}.json"
        
        pairs_df = self.db.get_all_pairs()
        pairs_json = pairs_df.to_dict('records')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(pairs_json, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported to JSON: {output_path}")
        return output_path
