"""
main.py — Entry point for the Python Voice Assistant.

Oasis Infobyte · AICTE Internship · Task 1 (Beginner Tier)

Run:
    python main.py

The program starts a continuous voice-listening loop.
Press Ctrl+C at any time to exit gracefully.
"""

import sys

from assistant import run_assistant
from utils import (
    enable_ansi_colors,
    log_error,
    log_info,
    log_success,
    print_banner,
)


def main() -> None:
    """Launch the Voice Assistant application."""
    enable_ansi_colors()
    print_banner()

    log_info("Initialising Voice Assistant …")

    try:
        # Quick sanity check — import the heavy dependencies early
        import pyttsx3            # noqa: F401
        import speech_recognition  # noqa: F401
        log_success("All dependencies loaded successfully.")
    except ImportError as exc:
        log_error(
            f"Missing dependency: {exc.name}. "
            "Run  pip install -r requirements.txt  first."
        )
        sys.exit(1)

    try:
        run_assistant()
    except KeyboardInterrupt:
        # Ctrl+C — exit cleanly without a traceback
        print()  # move past the ^C line
        log_info("Keyboard interrupt received.")
        from speech import speak
        speak("Goodbye! Have a great day!")
    except Exception as exc:  # noqa: BLE001
        log_error(f"Unexpected error: {exc}")
        sys.exit(1)
    finally:
        log_success("Voice Assistant shut down cleanly. See you next time!")


if __name__ == "__main__":
    main()
