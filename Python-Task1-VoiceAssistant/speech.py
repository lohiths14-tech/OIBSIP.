"""
speech.py — Speech input / output engine for the Voice Assistant.

Handles:
  • Text-to-Speech via pyttsx3
  • Voice capture via SpeechRecognition + PyAudio
  • Robust error handling for microphone & network issues
"""

import pyttsx3
import speech_recognition as sr

from utils import (
    log_assistant,
    log_error,
    log_info,
    log_user,
    log_warning,
)


# ──────────────────────────────────────────────
# Text-to-Speech (TTS)
# ──────────────────────────────────────────────

def _init_tts_engine() -> pyttsx3.Engine:
    """Create and configure a pyttsx3 TTS engine singleton."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    if len(voices) >= 2:
        engine.setProperty("voice", voices[1].id)
    return engine


# Global TTS engine instance
_TTS_ENGINE = _init_tts_engine()


def speak(text: str) -> None:
    """Speak *text* aloud and log it to the console.

    Parameters
    ----------
    text : str
        The sentence the assistant should say.
    """
    log_assistant(text)

    try:
        _TTS_ENGINE.say(text)
        _TTS_ENGINE.runAndWait()
    except RuntimeError as exc:
        log_error(f"TTS engine error: {exc}")
    except Exception as exc:  # noqa: BLE001 – defensive fallback
        log_error(f"Unexpected TTS error: {exc}")


# ──────────────────────────────────────────────
# Speech Recognition (STT)
# ──────────────────────────────────────────────

def listen(timeout: int = 5, phrase_time_limit: int = 10) -> str | None:
    """Capture audio from the default microphone and return recognised text.

    Uses Google's free Web Speech API via ``sr.Recognizer.recognize_google``.

    Parameters
    ----------
    timeout : int
        Max seconds to wait for a phrase to begin (default 5).
    phrase_time_limit : int
        Max seconds a single phrase may last (default 10).

    Returns
    -------
    str or None
        Lowercase transcription of the spoken phrase, or *None* when
        recognition fails for any reason.
    """
    recognizer = sr.Recognizer()

    # Dynamic energy threshold adapts to ambient noise each call
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            log_info("Listening … (speak now)")

            # Quick ambient-noise calibration (0.5 s)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

    except sr.WaitTimeoutError:
        log_warning("No speech detected (timed out). Try again.")
        return None

    except OSError:
        log_error(
            "Microphone not found or unavailable. "
            "Please check your audio input device."
        )
        speak("I cannot access the microphone. Please check your audio settings.")
        return None

    except Exception as exc:  # noqa: BLE001
        log_error(f"Microphone error: {exc}")
        return None

    # ── Attempt recognition ──────────────────
    try:
        text = recognizer.recognize_google(audio, language="en-US")
        text = text.lower().strip()
        log_user(text)
        return text

    except sr.UnknownValueError:
        log_warning("Could not understand audio.")
        speak("I'm sorry, I didn't understand that. Please say it again.")
        return None

    except sr.RequestError:
        log_error("Speech Recognition service unreachable (no internet?).")
        speak(
            "I'm sorry, I cannot reach the speech recognition service. "
            "Please check your internet connection."
        )
        return None

    except Exception as exc:  # noqa: BLE001
        log_error(f"Recognition error: {exc}")
        return None
