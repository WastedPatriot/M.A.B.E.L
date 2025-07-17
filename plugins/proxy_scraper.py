from core.plugin_base import PluginBase
import requests

class ProxyScraperPlugin(PluginBase):
    @property
    def name(self): return "proxy_scraper"
    @property
    def description(self): return "Finds and returns a list of free SOCKS5/HTTP proxies for OPSEC."
    def run(self, protocol="socks5", **kwargs):
        # Scrape a free proxy site
        url = "https://www.proxy-list.download/api/v1/get?type=socks5" if protocol == "socks5" else "https://www.proxy-list.download/api/v1/get?type=http"
        try:
            resp = requests.get(url, timeout=15)
            proxies = [line.strip() for line in resp.text.splitlines() if line.strip()]
            if proxies:
                # (Optionally) Test the top 5 for reachability
                return f"Found {len(proxies)} {protocol} proxies:\n" + "\n".join(proxies[:5])
            return "No proxies found."
        except Exception as e:
            return f"Proxy scrape error: {e}"

def get_plugin(): return ProxyScraperPlugin()
# plugins/proxy_scraper.py