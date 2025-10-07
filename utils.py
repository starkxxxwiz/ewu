"""
Utility Functions for Terminal UI
Provides colored output, progress tracking, and visual elements
"""

from rich.console import Console
from rich.table import Table
from rich import box
import pyfiglet


console = Console()


def clear_screen():
    """Clear the terminal screen"""
    console.clear()


def display_banner():
    """Display ASCII art banner"""
    # Create ASCII art
    banner_text = pyfiglet.figlet_format("EWU Tool", font="slant")
    
    # Display with styling
    console.print()
    console.print(banner_text, style="bold cyan")
    console.print("=" * 70, style="blue")
    console.print(
        "EWU Course Fetching Tool".center(70),
        style="bold white"
    )
    console.print(
        "Secure • Fast • Reliable".center(70),
        style="dim white"
    )
    console.print(
        "This is educational tool just for course fetching.".center(70),
        style="dim yellow"
    )
    console.print("=" * 70, style="blue")
    console.print()


def print_success(message: str):
    """Print success message"""
    console.print(f"[bold green]✅[/bold green] {message}")


def print_error(message: str):
    """Print error message"""
    console.print(f"[bold red]❌[/bold red] {message}")


def print_info(message: str):
    """Print info message"""
    console.print(f"[bold blue]ℹ️[/bold blue]  {message}")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[bold yellow]⚠️[/bold yellow]  {message}")


def print_step(message: str):
    """Print step message"""
    console.print(f"[bold cyan]🔐[/bold cyan] {message}")


def display_course_summary(courses: list, fetch_time: float):
    """
    Display course summary in a formatted table
    
    Args:
        courses: List of course dictionaries
        fetch_time: Time taken to fetch courses
    """
    console.print()
    console.print("=" * 70, style="cyan")
    console.print()
    
    # Summary statistics
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Label", style="bold cyan")
    table.add_column("Value", style="bold white")
    
    table.add_row("📚 Total Courses:", str(len(courses)))
    table.add_row("⏱️  Fetch Time:", f"{fetch_time:.2f}s")
    
    # Calculate some stats
    total_capacity = sum(c.get('SeatCapacity', 0) for c in courses)
    total_taken = sum(c.get('SeatTaken', 0) for c in courses)
    total_available = total_capacity - total_taken
    
    table.add_row("💺 Total Capacity:", str(total_capacity))
    table.add_row("✅ Total Taken:", str(total_taken))
    table.add_row("🎯 Total Available:", str(total_available))
    
    console.print(table)
    console.print()
    console.print("=" * 70, style="cyan")
    console.print()


def display_goodbye():
    """Display goodbye message"""
    console.print()
    console.print("=" * 70, style="cyan")
    console.print(
        "Thank you for using EWU Course Filter Tool!".center(70),
        style="bold cyan"
    )
    console.print(
        "Have a productive day 👋".center(70),
        style="bold white"
    )
    console.print("=" * 70, style="cyan")
    console.print()


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """
    Prompt user for yes/no response
    
    Args:
        question: Question to ask
        default: Default value if user just presses enter
        
    Returns:
        True for yes, False for no
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    console.print(f"[bold cyan]❓[/bold cyan] {question}{suffix}", end="")
    
    response = input().strip().lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes']

