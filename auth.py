"""
EWU Portal Authentication Module
Handles user authentication with the EWU portal system
"""

import requests
import re
from typing import Dict, Optional


class EWUAuthenticator:
    """Handles authentication with EWU portal"""
    
    def __init__(self):
        self.portal_url = "https://portal.ewubd.edu/"
        self.session_id = None
        self.session = requests.Session()
        
    def authenticate(self, username: str, password: str, proxy_address: Optional[str] = None) -> Dict[str, any]:
        """
        Authenticate user with EWU portal
        
        Args:
            username: Student ID
            password: User password
            proxy_address: Optional proxy address in format 'ip:port'
            
        Returns:
            Dictionary with status and message
        """
        try:
            # Setup proxy configuration if provided
            proxies = None
            timeout = 10
            
            if proxy_address:
                proxy_url = f"http://{proxy_address}"
                proxies = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                timeout = 15  # Extended timeout for proxy requests
            
            # Step 1: Initial GET request to retrieve hidden values and session
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Pragma': 'no-cache',
                'Accept': '*/*'
            }
            
            response = self.session.get(
                self.portal_url, 
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=False
            )
            
            if response.status_code != 200:
                return {
                    'status': 'error',
                    'message': 'Failed to connect to portal. Please try again later.'
                }
            
            # Step 2: Parse hidden form values (FirstNo and SecondNo)
            first_no_match = re.search(r'<input type="hidden" name="FirstNo" value="([^"]+)"', response.text)
            second_no_match = re.search(r'<input type="hidden" name="SecondNo" value="([^"]+)"', response.text)
            
            if not first_no_match or not second_no_match:
                return {
                    'status': 'error',
                    'message': 'Failed to parse portal form values'
                }
            
            first_no = first_no_match.group(1)
            second_no = second_no_match.group(1)
            
            # Step 3: Calculate sum for verification
            verification_sum = int(first_no) + int(second_no)
            
            # Step 4: Extract ASP.NET session cookie
            session_id = None
            for cookie in response.cookies:
                if cookie.name == 'ASP.NET_SessionId':
                    session_id = cookie.value
                    break
            
            if not session_id:
                return {
                    'status': 'error',
                    'message': 'Failed to retrieve session cookie from portal'
                }
            
            self.session_id = session_id
            
            # Step 5: Prepare POST data with user credentials
            post_data = {
                'Username': username,
                'Password': password,
                'Answer': str(verification_sum),
                'FirstNo': first_no,
                'SecondNo': second_no
            }
            
            # Step 6: Submit login POST request
            login_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Cookie': f'ASP.NET_SessionId={session_id}'
            }
            
            login_response = self.session.post(
                self.portal_url,
                data=post_data,
                headers=login_headers,
                proxies=proxies,
                timeout=timeout,
                allow_redirects=True,
                verify=False
            )
            
            if login_response.status_code != 200:
                return {
                    'status': 'error',
                    'message': 'Login request failed. Please try again.'
                }
            
            # Step 7: Verify login success
            if 'View Profile' in login_response.text:
                return {
                    'status': 'success',
                    'message': 'Login successful',
                    'session_id': session_id
                }
            elif 'Username or password is incorrect' in login_response.text:
                return {
                    'status': 'error',
                    'message': 'Username or password is incorrect'
                }
            elif 'Invalid answer' in login_response.text:
                return {
                    'status': 'error',
                    'message': 'Portal verification failed. Please try again.'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Could not determine login status. Please try again.'
                }
                
        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }
    
    def get_session_id(self) -> Optional[str]:
        """Get the current session ID"""
        return self.session_id

