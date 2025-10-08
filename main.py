#!/usr/bin/env python3
"""
EWU Course Fetching Tool - Main Application
Interactive terminal-based tool for fetching and managing EWU course schedules
"""

import sys
import time
import getpass
import urllib3
from typing import Optional

from auth import EWUAuthenticator
from fetch_courses import CourseFetcher
from pdf_export import PDFExporter
from proxy_manager import ProxyManager
from utils import (
    display_banner,
    clear_screen,
    print_success,
    print_error,
    print_info,
    print_step,
    display_course_summary,
    display_goodbye,
    prompt_yes_no,
    console
)

# Disable SSL warnings (as in original PHP code)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class EWUCourseTool:
    """Main application class for EWU Course Fetching Tool"""
    
    def __init__(self):
        self.authenticator = EWUAuthenticator()
        self.course_fetcher: Optional[CourseFetcher] = None
        self.user_id: Optional[str] = None
        self.courses: list = []
        self.fetch_time: float = 0.0
        self.proxy_manager = ProxyManager()
        self.active_proxy: Optional[str] = None
    
    def run(self):
        """Main application flow"""
        # Display banner
        display_banner()
        
        # Step 0: Proxy Mode Selection
        if not self.setup_proxy_mode():
            print_error("Proxy setup failed. Exiting...")
            sys.exit(1)
        
        # Step 1: Authentication
        if not self.authenticate():
            print_error("Authentication failed. Exiting...")
            sys.exit(1)
        
        # Clear screen and show banner again after authentication
        clear_screen()
        display_banner()
        
        # Step 2: Fetch courses
        if not self.fetch_courses():
            print_error("Failed to fetch courses. Exiting...")
            sys.exit(1)
        
        # Step 3: Display summary
        display_course_summary(self.courses, self.fetch_time)
        
        # Step 4: Offer PDF export (automatically if courses are available)
        if self.courses:
            self.offer_pdf_export()
        else:
            # No courses, just show goodbye
            display_goodbye()
    
    def setup_proxy_mode(self) -> bool:
        """
        Setup proxy mode based on user choice
        
        Returns:
            True if setup successful, False otherwise
        """
        console.print()
        console.print("[bold cyan]═══ Connection Mode ═══[/bold cyan]")
        console.print()
        
        try:
            # Ask user about proxy mode
            enable_proxy = prompt_yes_no("🌐 Do you want to enable Proxy Mode?", default=False)
            
            if enable_proxy:
                console.print()
                print_info("Testing available proxies...")
                
                # Find working proxy
                self.active_proxy = self.proxy_manager.get_live_proxy()
                
                if self.active_proxy:
                    print_success(f"Using Proxy Mode: {self.active_proxy}")
                    console.print()
                else:
                    print_info("No working proxies found. Switching to direct mode.")
                    console.print()
            else:
                print_info("Using Direct Connection")
                console.print()
            
            return True
            
        except KeyboardInterrupt:
            console.print()
            print_info("Proxy setup cancelled by user")
            return False
        except Exception as e:
            print_error(f"Unexpected error during proxy setup: {str(e)}")
            return False
    
    def authenticate(self) -> bool:
        """
        Handle user authentication
        
        Returns:
            True if authentication successful, False otherwise
        """
        console.print()
        console.print("[bold cyan]═══ Authentication ═══[/bold cyan]")
        console.print()
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                # Get credentials
                self.user_id = input("🆔 Student ID: ").strip()
                
                if not self.user_id:
                    print_error("Student ID cannot be empty")
                    attempts += 1
                    continue
                
                password = getpass.getpass("🔒 Password: ")
                
                if not password:
                    print_error("Password cannot be empty")
                    attempts += 1
                    continue
                
                console.print()
                print_step("Authenticating user...")
                
                # Simulate authentication process with progress
                start_time = time.time()
                
                # Perform authentication
                result = self.authenticator.authenticate(self.user_id, password, self.active_proxy)
                
                auth_time = time.time() - start_time
                
                if result['status'] == 'success':
                    print_success(f"Login successful! (took {auth_time:.2f}s)")
                    console.print()
                    
                    # Initialize course fetcher
                    session_id = self.authenticator.get_session_id()
                    self.course_fetcher = CourseFetcher(session_id, self.active_proxy)
                    
                    return True
                else:
                    print_error(result['message'])
                    attempts += 1
                    
                    if attempts < max_attempts:
                        console.print(f"[dim]Attempts remaining: {max_attempts - attempts}[/dim]")
                        console.print()
            
            except KeyboardInterrupt:
                console.print()
                print_info("Authentication cancelled by user")
                return False
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}")
                attempts += 1
        
        print_error(f"Maximum authentication attempts ({max_attempts}) exceeded")
        return False
    
    def fetch_courses(self) -> bool:
        """
        Fetch course data from portal
        
        Returns:
            True if fetch successful, False otherwise
        """
        if not self.course_fetcher:
            print_error("Not authenticated. Cannot fetch courses.")
            return False
        
        console.print("[bold cyan]═══ Fetching Courses ═══[/bold cyan]")
        console.print()
        
        try:
            # Animated progress steps
            steps = [
                ("⏳ Connecting to server...", 0.5),
                ("📡 Fetching course data...", 1.5),
                ("📋 Parsing response...", 0.8),
            ]
            
            start_time = time.time()
            
            for message, duration in steps:
                console.print(f"[cyan]{message}[/cyan]")
                time.sleep(duration)
            
            # Actual fetch
            result = self.course_fetcher.fetch_courses()
            
            self.fetch_time = time.time() - start_time
            
            if result['status'] == 'success':
                self.courses = result['courses']
                console.print()
                print_success(f"Successfully fetched {result['count']} courses!")
                console.print(f"[dim]⏱️  Completed in {self.fetch_time:.2f} seconds[/dim]")
                console.print()
                return True
            else:
                print_error(result['message'])
                return False
                
        except KeyboardInterrupt:
            console.print()
            print_info("Fetch cancelled by user")
            return False
        except Exception as e:
            print_error(f"Unexpected error during fetch: {str(e)}")
            return False
    
    def offer_pdf_export(self):
        """Offer to export courses to PDF"""
        console.print()
        
        if prompt_yes_no("Would you like to save this data as a PDF report?", default=True):
            self.export_to_pdf()
        else:
            # User declined, clear screen and show goodbye
            clear_screen()
            display_banner()
            console.print()
            display_goodbye()
    
    def export_to_pdf(self):
        """Export courses to PDF"""
        try:
            console.print()
            print_step("Generating PDF report...")
            
            exporter = PDFExporter()
            
            # Generate filename
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'EWU_Courses_{timestamp}.pdf'
            
            # Export
            filepath = exporter.export_to_pdf(
                self.courses,
                self.user_id or 'Unknown',
                filename
            )
            
            # Clear screen and show banner again
            clear_screen()
            display_banner()
            
            # Show success message
            print_success(f"PDF saved successfully!")
            print_info(f"Location: {filepath}")
            console.print()
            
            # Show goodbye
            display_goodbye()
            
        except Exception as e:
            print_error(f"Failed to generate PDF: {str(e)}")


def main():
    """Entry point"""
    try:
        tool = EWUCourseTool()
        tool.run()
    except KeyboardInterrupt:
        console.print()
        print_info("Application interrupted by user")
        display_goodbye()
        sys.exit(0)
    except Exception as e:
        console.print()
        print_error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

