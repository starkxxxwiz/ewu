"""
EWU Course Data Fetching Module
Retrieves and parses course schedule data from the portal
"""

import requests
from typing import Dict, List, Optional


class CourseFetcher:
    """Fetches course data from EWU portal"""
    
    def __init__(self, session_id: str, proxy_address: Optional[str] = None):
        self.session_id = session_id
        self.proxy_address = proxy_address
        self.api_url = "https://portal.ewubd.edu/api/Advising/GetAllRoutine"
        
    def fetch_courses(self) -> Dict[str, any]:
        """
        Fetch course data from the portal API
        
        Returns:
            Dictionary with status and course data
        """
        try:
            # Setup proxy configuration if provided
            proxies = None
            timeout = 10
            
            if self.proxy_address:
                proxy_url = f"http://{self.proxy_address}"
                proxies = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                timeout = 15  # Extended timeout for proxy requests
            
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 26_0_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/141.0.7390.41 Mobile/15E148 Safari/604.1',
                'Referer': 'https://portal.ewubd.edu/Home/Advising',
                'Cookie': f'ASP.NET_SessionId={self.session_id}; perf_dv6Tr4n=1'
            }
            
            response = requests.get(
                self.api_url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=False  # SSL verification disabled as in original PHP
            )
            
            if response.status_code == 401 or response.status_code == 403:
                return {
                    'status': 'error',
                    'message': 'Session expired or unauthorized'
                }
            
            if response.status_code != 200:
                return {
                    'status': 'error',
                    'message': f'Failed to fetch courses (HTTP {response.status_code})'
                }
            
            courses_data = response.json()
            
            if not isinstance(courses_data, list):
                return {
                    'status': 'error',
                    'message': 'Invalid course data format'
                }
            
            return {
                'status': 'success',
                'courses': courses_data,
                'count': len(courses_data)
            }
            
        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error parsing course data: {str(e)}'
            }
    
    @staticmethod
    def parse_day_time(time_slot_name: str) -> Dict[str, str]:
        """
        Parse day and time from TimeSlotName
        
        Args:
            time_slot_name: Time slot string like "MW 10:00-11:30"
            
        Returns:
            Dictionary with 'day' and 'time' keys
        """
        if not time_slot_name:
            return {'day': '', 'time': ''}
        
        day_mapping = {
            'A': 'SATURDAY',
            'S': 'SUNDAY',
            'M': 'MONDAY',
            'T': 'TUESDAY',
            'W': 'WEDNESDAY',
            'R': 'THURSDAY'
        }
        
        # Extract day abbreviations (capital letters at the start)
        import re
        day_match = re.match(r'^[ASMTWR]+', time_slot_name)
        day_abbr = day_match.group(0) if day_match else ''
        
        # Convert abbreviations to full day names
        day_names = ', '.join([day_mapping.get(d, d) for d in day_abbr])
        
        # Extract time (everything after day abbreviations)
        time = re.sub(r'^[ASMTWR]+\s*', '', time_slot_name).strip()
        
        return {'day': day_names, 'time': time}

