"""
Enhanced statement extractor with better filtering and opinion detection
"""
import spacy
import re
import config

class EnhancedStatementExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load(config.SPACY_MODEL)
        except:
            print(f"SpaCy model '{config.SPACY_MODEL}' not found.")
            print("Please run: python -m spacy download en_core_web_sm")
            raise
        
        # Keywords that indicate opinions/stances (good for inconsistency detection)
        self.opinion_keywords = [
            'should', 'must', 'need to', 'believe', 'think', 'support', 'oppose',
            'agree', 'disagree', 'claim', 'argue', 'suggest', 'propose', 'recommend',
            'important', 'necessary', 'essential', 'critical', 'crucial', 'better', 'worse',
            'right', 'wrong', 'good', 'bad', 'fair', 'unfair', 'beneficial', 'harmful'
        ]
        
        # Agriculture-specific keywords for relevance filtering
        self.agriculture_keywords = [
            'farm', 'crop', 'agriculture', 'agri', 'farmer', 'cultivation',
            'harvest', 'irrigation', 'soil', 'pesticide', 'fertilizer', 'seed',
            'msp', 'apmc', 'mandi', 'subsidy', 'loan', 'kisan', 'agricultural',
            'rural', 'wheat', 'rice', 'paddy', 'sugarcane', 'cotton', 'dairy'
        ]
    
    def is_relevant_to_agriculture(self, text):
        """
        Check if statement is relevant to agriculture
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.agriculture_keywords)
    
    def has_opinion_or_stance(self, text):
        """
        Check if statement contains opinion/stance (useful for inconsistency)
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.opinion_keywords)
    
    def is_valid_statement(self, text):
        """
        Comprehensive validation of statement quality
        """
        # Length check
        if len(text) < config.MIN_STATEMENT_LENGTH or len(text) > config.MAX_STATEMENT_LENGTH:
            return False
        
        # Word count check
        words = text.split()
        if len(words) < 5 or len(words) > 100:
            return False
        
        # Remove questions
        if text.strip().endswith('?'):
            return False
        
        # Remove promotional/navigation text
        promotional_patterns = [
            r'click here', r'read more', r'subscribe', r'download',
            r'share this', r'follow us', r'copyright', r'all rights reserved',
            r'advertisement', r'sponsored'
        ]
        
        text_lower = text.lower()
        if any(re.search(pattern, text_lower) for pattern in promotional_patterns):
            return False
        
        # Check for meaningful content (not just numbers/dates)
        alpha_chars = sum(c.isalpha() for c in text)
        if alpha_chars < 20:
            return False
        
        return True
    
    def extract_statements(self, text):
        """
        Extract individual statements with enhanced filtering
        """
        if not text or len(text) < config.MIN_STATEMENT_LENGTH:
            return []
        
        # Process with SpaCy
        doc = self.nlp(text[:1000000])  # Limit text length for processing
        
        statements = []
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Basic validation
            if not self.is_valid_statement(sent_text):
                continue
            
            # Check relevance to agriculture
            if not self.is_relevant_to_agriculture(sent_text):
                continue
            
            # Clean the statement
            sent_text = self.clean_statement(sent_text)
            
            # Add metadata about statement type
            statement_info = {
                'text': sent_text,
                'has_opinion': self.has_opinion_or_stance(sent_text),
                'length': len(sent_text),
                'word_count': len(sent_text.split())
            }
            
            statements.append(statement_info)
        
        return statements
    
    def clean_statement(self, text):
        """
        Clean and normalize statement text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        # Fix common issues
        text = text.replace('\n', ' ').replace('\t', ' ')
        
        # Remove leading/trailing punctuation except sentence-ending ones
        text = text.strip(',.;:- ')
        
        return text.strip()
    
    def extract_from_document(self, document):
        """
        Extract statements from a document dict with metadata
        """
        statements = self.extract_statements(document.get('text', ''))
        
        # Add document metadata to each statement
        result = []
        for stmt in statements:
            result.append({
                'text': stmt['text'],
                'source_url': document.get('url'),
                'author': document.get('author'),
                'date': document.get('date'),
                'domain': document.get('domain'),
                'source_type': document.get('type', 'article'),
                'has_opinion': stmt['has_opinion'],
                'word_count': stmt['word_count']
            })
        
        return result
    
    def extract_from_multiple_documents(self, documents, verbose=True):
        """
        Extract statements from multiple documents with statistics
        """
        all_statements = []
        stats = {
            'total_documents': len(documents),
            'documents_processed': 0,
            'total_statements': 0,
            'opinion_statements': 0,
            'statements_per_source': {}
        }
        
        for doc in documents:
            statements = self.extract_from_document(doc)
            all_statements.extend(statements)
            
            if statements:
                stats['documents_processed'] += 1
                stats['total_statements'] += len(statements)
                stats['opinion_statements'] += sum(1 for s in statements if s['has_opinion'])
                
                domain = doc.get('domain', 'unknown')
                stats['statements_per_source'][domain] = stats['statements_per_source'].get(domain, 0) + len(statements)
                
                if verbose:
                    opinion_count = sum(1 for s in statements if s['has_opinion'])
                    print(f"  ✓ {len(statements)} statements ({opinion_count} with opinions) from {doc['url'][:50]}...")
        
        if verbose:
            print(f"\n📊 Extraction Statistics:")
            print(f"  Total documents: {stats['total_documents']}")
            print(f"  Documents processed: {stats['documents_processed']}")
            print(f"  Total statements: {stats['total_statements']}")
            print(f"  Statements with opinions: {stats['opinion_statements']} ({stats['opinion_statements']/max(stats['total_statements'],1)*100:.1f}%)")
            print(f"  Avg statements per document: {stats['total_statements']/max(stats['documents_processed'],1):.1f}")
        
        return all_statements, stats

if __name__ == "__main__":
    # Test the extractor
    extractor = EnhancedStatementExtractor()
    test_text = """
    Indian farmers need better support from the government. The MSP should be increased 
    to ensure fair prices. However, some argue that subsidies are not sustainable. 
    Agriculture contributes significantly to India's GDP.
    """
    statements = extractor.extract_statements(test_text)
    print(f"Extracted {len(statements)} statements:")
    for s in statements:
        print(f"  - {s['text']} [Opinion: {s['has_opinion']}]")
