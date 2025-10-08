"""
Proxy Manager Module
Handles proxy testing, selection, and management for EWU Course Tool
"""

import requests
import time
from typing import Optional, List
from utils import console, print_info, print_error, print_success


class ProxyManager:
    """Manages proxy testing and selection"""
    
    def __init__(self):
        self.test_url = "https://portal.ewubd.edu/"
        self.timeout = 30
        self.proxy_file = "proxy.txt"
    
    def read_proxy_list(self) -> List[str]:
        """
        Read proxy addresses from proxy.txt file
        
        Returns:
            List of proxy addresses in format 'ip:port'
        """
        try:
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                proxies = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        # Validate format (basic check)
                        if ':' in line and len(line.split(':')) == 2:
                            proxies.append(line)
                        else:
                            print_error(f"Invalid proxy format: {line}")
                
                return proxies
        except FileNotFoundError:
            print_error(f"Proxy file '{self.proxy_file}' not found")
            return []
        except Exception as e:
            print_error(f"Error reading proxy file: {str(e)}")
            return []
    
    def test_proxy(self, proxy_address: str) -> bool:
        """
        Test if a proxy is working by making a request to the test URL
        
        Args:
            proxy_address: Proxy address in format 'ip:port'
            
        Returns:
            True if proxy is working, False otherwise
        """
        try:
            proxy_url = f"http://{proxy_address}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Test the proxy with a quick request
            response = requests.get(
                self.test_url,
                proxies=proxies,
                headers=headers,
                timeout=self.timeout,
                verify=False  # Disable SSL verification as in original code
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_live_proxy(self) -> Optional[str]:
        """
        Find the first working proxy from the proxy list
        
        Returns:
            Working proxy address in format 'ip:port' or None if none work
        """
        proxies = self.read_proxy_list()
        
        if not proxies:
            print_error("No proxies found in proxy.txt")
            return None
        
        print_info(f"Found {len(proxies)} proxies to test")
        console.print()
        
        for i, proxy in enumerate(proxies, 1):
            console.print(f"[cyan]🔍[/cyan] Checking proxy {i}/{len(proxies)}: {proxy} ...")
            
            if self.test_proxy(proxy):
                print_success(f"Working proxy found: {proxy}")
                console.print()
                return proxy
            else:
                console.print(f"[dim]❌[/dim] Proxy {proxy} failed")
        
        print_error("No working proxies found. Switching to direct mode.")
        console.print()
        return None
    
    def get_proxy_config(self, proxy_address: str) -> dict:
        """
        Get proxy configuration dictionary for requests
        
        Args:
            proxy_address: Proxy address in format 'ip:port'
            
        Returns:
            Proxy configuration dictionary
        """
        proxy_url = f"http://{proxy_address}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    def get_extended_timeout(self) -> int:
        """
        Get extended timeout for proxy requests
        
        Returns:
            Extended timeout in seconds
        """
        return 15  # Extended timeout for proxy requests
