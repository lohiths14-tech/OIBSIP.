"""
utils.py — Utility helpers for the Voice Assistant.

Provides colorful console output, timestamped logging,
and time-based greeting generation.
"""

import os
from datetime import datetime


# ──────────────────────────────────────────────
# ANSI Color Codes (Windows 10+ supports these)
# ──────────────────────────────────────────────

class Colors:
    """ANSI escape-code constants for coloured terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Background
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"
    BG_BLUE = "\033[44m"


def enable_ansi_colors() -> None:
    """Enable ANSI escape sequences on Windows consoles."""
    if os.name == "nt":
        os.system("")  # triggers VT100 mode on Windows 10+


def timestamp() -> str:
    """Return the current local time formatted as [HH:MM:SS]."""
    return datetime.now().strftime("[%H:%M:%S]")


# ──────────────────────────────────────────────
# Console Logging Helpers
# ──────────────────────────────────────────────

def log_info(message: str) -> None:
    """Print a timestamped informational message in cyan."""
    print(f"  {Colors.DIM}{timestamp()}{Colors.RESET}  "
          f"{Colors.CYAN}ℹ {message}{Colors.RESET}")


def log_success(message: str) -> None:
    """Print a timestamped success message in green."""
    print(f"  {Colors.DIM}{timestamp()}{Colors.RESET}  "
          f"{Colors.GREEN}✔ {message}{Colors.RESET}")


def log_warning(message: str) -> None:
    """Print a timestamped warning message in yellow."""
    print(f"  {Colors.DIM}{timestamp()}{Colors.RESET}  "
          f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def log_error(message: str) -> None:
    """Print a timestamped error message in red."""
    print(f"  {Colors.DIM}{timestamp()}{Colors.RESET}  "
          f"{Colors.RED}✖ {message}{Colors.RESET}")


def log_assistant(message: str) -> None:
    """Print a timestamped assistant-speech message in magenta."""
    print(f"  {Colors.DIM}{timestamp()}{Colors.RESET}  "
          f"{Colors.MAGENTA}🔊 Assistant: {message}{Colors.RESET}")


def log_user(message: str) -> None:
    """Print a timestamped user-speech message in blue."""
    print(f"  {Colors.DIM}{timestamp()}{Colors.RESET}  "
          f"{Colors.BLUE}🎤 You: {message}{Colors.RESET}")


# ──────────────────────────────────────────────
# Greeting Logic
# ──────────────────────────────────────────────

def get_time_greeting() -> str:
    """Return a greeting phrase appropriate for the current hour.

    Returns
    -------
    str
        'Good Morning', 'Good Afternoon', or 'Good Evening'.
    """
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"


# ──────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────

def print_banner() -> None:
    """Display a styled startup banner in the console."""
    enable_ansi_colors()

    banner = rf"""
{Colors.CYAN}{Colors.BOLD}
  ╔══════════════════════════════════════════════════╗
  ║                                                  ║
  ║        🎙️  PYTHON VOICE ASSISTANT  🎙️           ║
  ║                                                  ║
  ║   Oasis Infobyte · AICTE Internship · Task 1    ║
  ║                                                  ║
  ╚══════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}  Powered by SpeechRecognition + pyttsx3
  Type Ctrl+C at any time to exit gracefully.{Colors.RESET}
"""
    print(banner)


def print_separator() -> None:
    """Print a thin horizontal rule for visual separation."""
    print(f"  {Colors.DIM}{'─' * 50}{Colors.RESET}")


def print_commands_help() -> None:
    """Print the list of supported voice commands."""
    print(f"""
{Colors.YELLOW}{Colors.BOLD}  Supported Commands:{Colors.RESET}
{Colors.DIM}  ──────────────────────────────────────{Colors.RESET}
  {Colors.GREEN}•{Colors.RESET} "Hello" / "Hi"
  {Colors.GREEN}•{Colors.RESET} "Good Morning" / "Good Afternoon" / "Good Evening"
  {Colors.GREEN}•{Colors.RESET} "What time is it?" / "Tell me the time"
  {Colors.GREEN}•{Colors.RESET} "What is today's date?" / "Tell me today's date"
  {Colors.GREEN}•{Colors.RESET} "Search <query>"   (opens Google in browser)
  {Colors.GREEN}•{Colors.RESET} "Exit" / "Quit" / "Stop"
{Colors.DIM}  ──────────────────────────────────────{Colors.RESET}
""")
