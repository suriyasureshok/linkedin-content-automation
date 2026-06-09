import httpx
import os
from typing import Optional, Dict, Any


class CloudflareTransport:
    """
    Custom HTTP transport that routes all Gemini API requests through Cloudflare Workers
    """
    
    def __init__(self):
        # Cloudflare Worker URLs (each different IP)
        self.proxy_urls = []
        
        us_url = os.getenv("CLOUDFLARE_WORKER_US_URL")
        if us_url:
            self.proxy_urls.append(us_url)
        
        eu_url = os.getenv("CLOUDFLARE_WORKER_EU_URL")
        if eu_url:
            self.proxy_urls.append(eu_url)
        
        asia_url = os.getenv("CLOUDFLARE_WORKER_ASIA_URL")
        if asia_url:
            self.proxy_urls.append(asia_url)
        
        au_url = os.getenv("CLOUDFLARE_WORKER_AU_URL")
        if au_url:
            self.proxy_urls.append(au_url)
        
        self.current_index = 0
        self.client = httpx.Client(timeout=90.0)
    
    def get_next_proxy(self) -> str:
        """Round-robin through different Cloudflare workers"""
        proxy = self.proxy_urls[self.current_index % len(self.proxy_urls)]
        self.current_index += 1
        return proxy
    
    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Intercept and forward request through Cloudflare proxy
        """
        # Get next proxy (different IP)
        proxy_url = self.get_next_proxy()
        
        # Extract the path from the original URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path
        query = parsed.query
        
        # Build new URL through our proxy
        if query:
            new_url = f"{proxy_url}{path}?{query}"
        else:
            new_url = f"{proxy_url}{path}"
        
        print(f"[INFO] Routing through {proxy_url}")
        
        # Forward the request - preserve all kwargs exactly as received
        return self.client.request(method, new_url, **kwargs)
