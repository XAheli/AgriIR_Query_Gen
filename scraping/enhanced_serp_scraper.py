"""
Enhanced Google SERP scraper with SerpAPI support
Falls back to BeautifulSoup scraping if API not available
"""
import requests
from bs4 import BeautifulSoup
import time
import json
import config
from urllib.parse import urlparse

class EnhancedSERPScraper:
    def __init__(self, api_key=None):
        self.api_key = api_key or config.SERP_API_KEY
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
    
    def search_with_api(self, query, num_results=10):
        """
        Search using SerpAPI (100 free searches/month)
        Sign up at: https://serpapi.com/
        """
        if not self.api_key:
            return None
        
        try:
            url = "https://serpapi.com/search"
            params = {
                'q': query,
                'api_key': self.api_key,
                'num': num_results,
                'gl': 'in',  # India
                'hl': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for result in data.get('organic_results', []):
                results.append({
                    'url': result.get('link'),
                    'title': result.get('title'),
                    'snippet': result.get('snippet'),
                    'query': query,
                    'position': result.get('position')
                })
            
            return results
            
        except Exception as e:
            print(f"  SerpAPI error: {str(e)}")
            return None
    
    def search_with_scraping(self, query, num_results=10):
        """
        Fallback: Search Google and extract URLs using BeautifulSoup
        """
        search_url = "https://www.google.com/search"
        params = {
            'q': query,
            'num': num_results,
            'hl': 'en',
            'gl': 'in'
        }
        
        try:
            time.sleep(config.SCRAPE_DELAY)
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extract search results (Google's HTML structure changes frequently)
            for g in soup.find_all('div', class_='g'):
                link_tag = g.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    url = link_tag['href']
                    if url.startswith('http'):
                        # Extract title
                        title_tag = g.find('h3')
                        title = title_tag.text if title_tag else ""
                        
                        # Extract snippet
                        snippet_tags = g.find_all(['div', 'span'], class_=lambda x: x and 'VwiC3b' in str(x))
                        snippet = snippet_tags[0].text if snippet_tags else ""
                        
                        results.append({
                            'url': url,
                            'title': title,
                            'snippet': snippet,
                            'query': query
                        })
            
            return results
            
        except Exception as e:
            print(f"  Scraping error: {str(e)}")
            return []
    
    def search_google(self, query, num_results=10):
        """
        Main search method: tries API first, falls back to scraping
        """
        print(f"Searching: {query}")
        
        # Try API first
        if self.api_key:
            results = self.search_with_api(query, num_results)
            if results:
                print(f"  ✓ Found {len(results)} results (via API)")
                return results
        
        # Fallback to scraping
        results = self.search_with_scraping(query, num_results)
        print(f"  ✓ Found {len(results)} results (via scraping)")
        return results
    
    def filter_by_domains(self, results, target_domains=None):
        """
        Filter results to keep only target domains
        If target_domains is empty, return all results
        """
        if not target_domains or len(target_domains) == 0:
            return results
        
        filtered = []
        for result in results:
            domain = urlparse(result['url']).netloc
            if any(target in domain for target in target_domains):
                filtered.append(result)
        
        return filtered
    
    def scrape_all_queries(self, queries, num_results=10, filter_domains=True):
        """
        Scrape all queries and return consolidated results
        """
        all_results = []
        
        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] ", end="")
            results = self.search_google(query, num_results)
            
            # Filter by target domains if enabled
            if filter_domains and config.TARGET_DOMAINS:
                original_count = len(results)
                results = self.filter_by_domains(results, config.TARGET_DOMAINS)
                if len(results) < original_count:
                    print(f"  ℹ️  Filtered to {len(results)} results from target domains")
            
            all_results.extend(results)
            
            # Rate limiting
            if i % 5 == 0:
                print("  💤 Rate limit pause...")
                time.sleep(10)
        
        # Remove duplicates by URL
        unique_results = {r['url']: r for r in all_results}.values()
        unique_results = list(unique_results)
        
        print(f"\n✓ Total unique URLs collected: {len(unique_results)}")
        return unique_results
    
    def get_diverse_results(self, results, max_per_domain=5):
        """
        Ensure diversity by limiting results per domain
        """
        domain_counts = {}
        diverse_results = []
        
        for result in results:
            domain = urlparse(result['url']).netloc
            count = domain_counts.get(domain, 0)
            
            if count < max_per_domain:
                diverse_results.append(result)
                domain_counts[domain] = count + 1
        
        return diverse_results

if __name__ == "__main__":
    # Test the scraper
    scraper = EnhancedSERPScraper()
    results = scraper.search_google("Indian agriculture MSP policy", num_results=5)
    print(f"\nFound {len(results)} results:")
    for r in results[:3]:
        print(f"  - {r['title'][:60]}...")
        print(f"    {r['url']}")
