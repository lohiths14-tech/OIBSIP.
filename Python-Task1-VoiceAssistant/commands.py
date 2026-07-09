"""
commands.py — Command handlers for the Voice Assistant.

Each public function in this module implements one assistant capability:
  • Greetings   (hello, hi, good morning / afternoon / evening)
  • Current time
  • Current date
  • Google search
  • Exit / quit / stop

All handlers call `speech.speak()` so every response is spoken aloud.
"""

import os
import webbrowser
from datetime import datetime

from speech import speak
from utils import get_time_greeting, log_info, log_success


# ──────────────────────────────────────────────
# Greeting Commands
# ──────────────────────────────────────────────

def handle_greeting(command: str) -> None:
    """Respond to a greeting phrase.

    Supports: hello, hi, good morning, good afternoon, good evening.

    Parameters
    ----------
    command : str
        The recognised voice command (lowercase).
    """
    if "good morning" in command:
        speak("Good Morning! How can I help you today?")
    elif "good afternoon" in command:
        speak("Good Afternoon! How can I help you today?")
    elif "good evening" in command:
        speak("Good Evening! How can I help you today?")
    elif "hello" in command:
        speak("Hello! Welcome. How can I help you today?")
    elif "hi" in command:
        speak("Hi there! How can I help you today?")


# ──────────────────────────────────────────────
# Time Command
# ──────────────────────────────────────────────

def handle_time() -> None:
    """Speak the current local time in 12-hour format."""
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")


# ──────────────────────────────────────────────
# Date Command
# ──────────────────────────────────────────────

def handle_date() -> None:
    """Speak today's date in a human-friendly format (e.g. 9 July 2026)."""
    today = datetime.now().strftime("%-d %B %Y") if os.name != "nt" \
        else datetime.now().strftime("%#d %B %Y")
    speak(f"Today's date is {today}.")


# ──────────────────────────────────────────────
# Google Search Command
# ──────────────────────────────────────────────

def handle_search(command: str) -> None:
    """Extract a search query from *command* and open Google in the browser.

    The word "search" is stripped from the beginning so the rest of the
    sentence becomes the query.

    Parameters
    ----------
    command : str
        The recognised voice command (lowercase), e.g. "search python programming".
    """
    # Remove the keyword "search" and any leading whitespace
    query = command.replace("search", "", 1).strip()

    if not query:
        speak("What would you like me to search for?")
        return

    url = f"https://www.google.com/search?q={query}"
    speak(f"Searching Google for {query}.")
    log_info(f"Opening browser → {url}")

    try:
        webbrowser.open(url)
        log_success("Browser opened successfully.")
    except Exception as exc:  # noqa: BLE001
        speak("I'm sorry, I was unable to open the browser.")
        from utils import log_error
        log_error(f"Browser error: {exc}")


# ──────────────────────────────────────────────
# Exit Command
# ──────────────────────────────────────────────

def handle_exit() -> None:
    """Speak a farewell message before the assistant shuts down."""
    greeting = get_time_greeting()
    speak(f"Goodbye! Have a wonderful {greeting.split()[-1].lower()}. Take care!")
