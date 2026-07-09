"""
assistant.py — Core orchestrator for the Voice Assistant.

Owns the main listen → parse → dispatch → respond loop.
Routes recognised speech to the appropriate handler in `commands.py`.
"""

from commands import (
    handle_date,
    handle_exit,
    handle_greeting,
    handle_search,
    handle_time,
)
from speech import listen, speak
from utils import (
    get_time_greeting,
    log_info,
    log_warning,
    print_commands_help,
    print_separator,
)


# ──────────────────────────────────────────────
# Keyword constants
# ──────────────────────────────────────────────

GREETING_KEYWORDS: list[str] = [
    "hello",
    "hi",
    "good morning",
    "good afternoon",
    "good evening",
]

TIME_KEYWORDS: list[str] = [
    "what time",
    "tell me the time",
    "current time",
    "time now",
    "what's the time",
]

DATE_KEYWORDS: list[str] = [
    "today's date",
    "what is today",
    "tell me today",
    "current date",
    "date today",
    "what date",
    "today date",
]

EXIT_KEYWORDS: list[str] = [
    "exit",
    "quit",
    "stop",
    "bye",
    "goodbye",
    "shut down",
    "shutdown",
]


# ──────────────────────────────────────────────
# Command Router
# ──────────────────────────────────────────────

def _route_command(command: str) -> bool:
    """Match *command* to a handler and execute it.

    Parameters
    ----------
    command : str
        The recognised voice command (already lowercased).

    Returns
    -------
    bool
        ``True`` if the assistant should keep running,
        ``False`` if the user asked to exit.
    """
    # 1. Exit / Quit / Stop
    if any(kw in command for kw in EXIT_KEYWORDS):
        handle_exit()
        return False

    # 2. Greetings
    if any(kw in command for kw in GREETING_KEYWORDS):
        handle_greeting(command)
        return True

    # 3. Time
    if any(kw in command for kw in TIME_KEYWORDS):
        handle_time()
        return True

    # 4. Date
    if any(kw in command for kw in DATE_KEYWORDS):
        handle_date()
        return True

    # 5. Google Search (must start with "search")
    if command.startswith("search"):
        handle_search(command)
        return True

    # 6. Unknown command
    log_warning(f"Unrecognised command: '{command}'")
    speak(
        "I'm sorry, I didn't understand that command. "
        "You can say hello, ask for the time or date, "
        "search Google, or say exit to quit."
    )
    return True


# ──────────────────────────────────────────────
# Main Loop
# ──────────────────────────────────────────────

def run_assistant() -> None:
    """Start the voice assistant's continuous listening loop.

    The loop:
      1. Greets the user based on the current time of day.
      2. Shows the list of supported commands.
      3. Continuously listens → routes → responds.
      4. Exits gracefully on "exit" / "quit" / "stop" or Ctrl+C.
    """
    # Welcome message
    greeting = get_time_greeting()
    speak(f"{greeting}! I am your Voice Assistant. How can I help you today?")
    print_commands_help()

    running = True

    while running:
        print_separator()
        command = listen()

        if command is None:
            # Recognition failed or timed out — retry silently
            continue

        running = _route_command(command)

    log_info("Assistant session ended.")
