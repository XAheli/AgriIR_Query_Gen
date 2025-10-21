"""
Enhanced content scraper with support for multiple content types
Includes better extraction for articles, blogs, and social media
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import config
import time
import re

class EnhancedContentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
    
    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\'\"]', '', text)
        
        return text.strip()
    
    def extract_article_content(self, soup, url):
        """
        Extract main article content using multiple strategies
        """
        # Strategy 1: Look for article tag
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            if paragraphs:
                return ' '.join([p.get_text().strip() for p in paragraphs])
        
        # Strategy 2: Common content class names
        content_classes = [
            'article-content', 'post-content', 'entry-content', 
            'story-content', 'content', 'main-content',
            'article-body', 'post-body', 'entry-body'
        ]
        
        for class_name in content_classes:
            content_div = soup.find('div', class_=re.compile(class_name, re.I))
            if content_div:
                paragraphs = content_div.find_all('p')
                if paragraphs:
                    return ' '.join([p.get_text().strip() for p in paragraphs])
        
        # Strategy 3: Find main content area
        main = soup.find('main')
        if main:
            paragraphs = main.find_all('p')
            if paragraphs:
                return ' '.join([p.get_text().strip() for p in paragraphs])
        
        # Strategy 4: All paragraphs (fallback)
        paragraphs = soup.find_all('p')
        if paragraphs:
            return ' '.join([p.get_text().strip() for p in paragraphs[:20]])  # Limit to first 20
        
        return ""
    
    def extract_metadata(self, soup, url):
        """Extract author, date, and other metadata"""
        metadata = {
            'author': None,
            'date': None,
            'title': None
        }
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Extract author
        author_patterns = [
            soup.find('meta', {'name': 'author'}),
            soup.find('meta', {'property': 'article:author'}),
            soup.find('span', class_=re.compile('author', re.I)),
            soup.find('div', class_=re.compile('author', re.I)),
            soup.find('a', rel='author')
        ]
        
        for pattern in author_patterns:
            if pattern:
                if pattern.get('content'):
                    metadata['author'] = pattern.get('content')
                else:
                    metadata['author'] = pattern.get_text().strip()
                break
        
        # Extract date
        date_patterns = [
            soup.find('meta', {'property': 'article:published_time'}),
            soup.find('time'),
            soup.find('span', class_=re.compile('date|time', re.I)),
            soup.find('div', class_=re.compile('date|time', re.I))
        ]
        
        for pattern in date_patterns:
            if pattern:
                if pattern.get('content'):
                    metadata['date'] = pattern.get('content')
                elif pattern.get('datetime'):
                    metadata['date'] = pattern.get('datetime')
                else:
                    metadata['date'] = pattern.get_text().strip()
                break
        
        return metadata
    
    def scrape_url(self, url, timeout=15):
        """
        Scrape a single URL with enhanced extraction
        """
        try:
            time.sleep(config.SCRAPE_DELAY)
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
                tag.decompose()
            
            # Extract content and metadata
            content = self.extract_article_content(soup, url)
            metadata = self.extract_metadata(soup, url)
            
            if not content or len(content) < 100:
                print(f"  ⚠️  Insufficient content from {url[:50]}")
                return None
            
            return {
                'url': url,
                'text': self.clean_text(content),
                'author': metadata['author'],
                'date': metadata['date'],
                'title': metadata['title'],
                'domain': urlparse(url).netloc,
                'word_count': len(content.split())
            }
            
        except requests.exceptions.Timeout:
            print(f"  ⏱️  Timeout for {url[:50]}")
            return None
        except Exception as e:
            print(f"  ❌ Error scraping {url[:50]}: {str(e)}")
            return None
    
    def scrape_multiple_urls(self, urls, max_urls=None):
        """
        Scrape content from multiple URLs with progress tracking
        """
        results = []
        urls_to_scrape = urls[:max_urls] if max_urls else urls
        
        for i, url in enumerate(urls_to_scrape, 1):
            print(f"[{i}/{len(urls_to_scrape)}] Scraping: {url[:60]}...")
            content = self.scrape_url(url)
            if content:
                results.append(content)
                print(f"  ✓ Extracted {content['word_count']} words")
            
            # Rate limiting
            if i % 10 == 0:
                print(f"  💤 Rate limit pause...")
                time.sleep(5)
        
        success_rate = len(results) / len(urls_to_scrape) * 100 if urls_to_scrape else 0
        print(f"\n✓ Successfully scraped {len(results)}/{len(urls_to_scrape)} URLs ({success_rate:.1f}%)")
        return results

if __name__ == "__main__":
    # Test the scraper
    scraper = EnhancedContentScraper()
    test_url = "https://thehindu.com"
    result = scraper.scrape_url(test_url)
    if result:
        print(f"Title: {result['title']}")
        print(f"Author: {result['author']}")
        print(f"Content: {result['text'][:200]}...")
