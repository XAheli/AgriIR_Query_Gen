"""
Reddit scraper for agriculture-related posts and comments
Uses PRAW (Python Reddit API Wrapper)
"""
import praw
import time
from datetime import datetime
import config

class RedditScraper:
    def __init__(self, client_id=None, client_secret=None, user_agent=None):
        """
        Initialize Reddit scraper
        To get credentials: https://www.reddit.com/prefs/apps
        """
        self.client_id = client_id or config.REDDIT_CLIENT_ID
        self.client_secret = client_secret or config.REDDIT_CLIENT_SECRET
        self.user_agent = user_agent or getattr(config, 'REDDIT_USER_AGENT', config.USER_AGENT)
        
        if self.client_id and self.client_secret:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
        else:
            print("⚠️  Reddit credentials not configured. Skipping Reddit scraping.")
            self.reddit = None
    
    def search_posts(self, query, subreddits=['india', 'IndiaSpeaks', 'IndianAgriculture', 'agriculture', 'farming', 'IndianNews'], limit=50):
        """
        Search Reddit posts by query across multiple subreddits
        """
        if not self.reddit:
            return []
        
        results = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                print(f"Searching r/{subreddit_name} for: {query}")
                
                # Search posts
                for submission in subreddit.search(query, limit=limit, sort='relevance'):
                    post_data = {
                        'text': submission.title + ". " + submission.selftext,
                        'url': f"https://reddit.com{submission.permalink}",
                        'author': str(submission.author),
                        'date': datetime.fromtimestamp(submission.created_utc).isoformat(),
                        'domain': 'reddit.com',
                        'subreddit': subreddit_name,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'type': 'post'
                    }
                    
                    if post_data['text'].strip():
                        results.append(post_data)
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error searching r/{subreddit_name}: {str(e)}")
        
        return results
    
    def get_post_comments(self, post_url, limit=100):
        """
        Extract comments from a Reddit post
        """
        if not self.reddit:
            return []
        
        try:
            submission = self.reddit.submission(url=post_url)
            submission.comments.replace_more(limit=0)  # Flatten comment tree
            
            comments = []
            for comment in submission.comments.list()[:limit]:
                if hasattr(comment, 'body') and len(comment.body) > 20:
                    comment_data = {
                        'text': comment.body,
                        'url': post_url + comment.id,
                        'author': str(comment.author),
                        'date': datetime.fromtimestamp(comment.created_utc).isoformat(),
                        'domain': 'reddit.com',
                        'score': comment.score,
                        'type': 'comment',
                        'parent_post': post_url
                    }
                    comments.append(comment_data)
            
            return comments
            
        except Exception as e:
            print(f"Error extracting comments from {post_url}: {str(e)}")
            return []
    
    def scrape_agriculture_content(self, queries, max_posts_per_query=30):
        """
        Main method to scrape agriculture-related content from Reddit
        Enhanced for better diversity
        """
        all_results = []
        
        for query in queries:
            posts = self.search_posts(query, limit=max_posts_per_query)
            all_results.extend(posts)
            
            # Also get comments from top posts for opinion diversity
            for post in posts[:10]:  # Get comments from top 10 posts per query
                comments = self.get_post_comments(post['url'], limit=100)
                all_results.extend(comments)
        
        print(f"✓ Collected {len(all_results)} items from Reddit")
        return all_results

if __name__ == "__main__":
    # Test the scraper
    scraper = RedditScraper()
    results = scraper.search_posts("Indian agriculture MSP", limit=5)
    print(f"Found {len(results)} posts")
    for r in results[:3]:
        print(f"\n{r['text'][:100]}...")
