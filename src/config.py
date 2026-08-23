"""
config.py - Application Configuration
======================================
Loads environment variables, defines form options (symptom lists,
duration choices, languages), and stores project-wide constants.

IMPORTANT: This is an educational AI prototype, NOT a medical device.
"""

import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load environment variables from .env file
# ---------------------------------------------------------------------------
load_dotenv()


def get_api_key() -> str:
    """
    Retrieve the OpenAI API key from the environment.

    Returns:
        str: The API key, or an empty string if not set.

    The key is NEVER hard-coded. Users must create a .env file
    with OPENAI_API_KEY=sk-... (see .env.example).
    """
    return os.getenv("OPENAI_API_KEY", "")


# ---------------------------------------------------------------------------
# Default model settings
# ---------------------------------------------------------------------------
DEFAULT_MODEL: str = "gpt-4o-mini"
DEFAULT_TEMPERATURE: float = 0.3          # Lower = more deterministic output
AVAILABLE_MODELS: list[str] = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

# ---------------------------------------------------------------------------
# Symptom options for the multiselect widget
# ---------------------------------------------------------------------------
SYMPTOM_OPTIONS: list[str] = [
    "Headache",
    "Fever",
    "Cough",
    "Sore Throat",
    "Runny Nose",
    "Body Aches",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Shortness of Breath",
    "Chest Pain",
    "Dizziness",
    "Rash",
    "Joint Pain",
    "Back Pain",
    "Abdominal Pain",
    "Loss of Appetite",
    "Difficulty Sleeping",
    "Anxiety",
    "Blurred Vision",
    "Numbness or Tingling",
    "Swelling",
    "Weight Loss (unexplained)",
    "Palpitations",
]

# ---------------------------------------------------------------------------
# Duration options for the selectbox widget
# ---------------------------------------------------------------------------
DURATION_OPTIONS: list[str] = [
    "Less than 24 hours",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "2-4 weeks",
    "More than a month",
]

# ---------------------------------------------------------------------------
# Gender options for the selectbox widget
# ---------------------------------------------------------------------------
GENDER_OPTIONS: list[str] = [
    "Male",
    "Female",
    "Other",
    "Prefer not to say",
]

# ---------------------------------------------------------------------------
# Language options for the selectbox widget
# ---------------------------------------------------------------------------
LANGUAGE_OPTIONS: list[str] = [
    "English",
    "Urdu",
    "Arabic",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Hindi",
    "Turkish",
    "Portuguese",
]

# ---------------------------------------------------------------------------
# Urgency levels (controlled vocabulary)
# ---------------------------------------------------------------------------
URGENCY_LEVELS: list[str] = ["LOW", "MEDIUM", "HIGH", "EMERGENCY"]

# ---------------------------------------------------------------------------
# Required keys in the JSON assessment response
# ---------------------------------------------------------------------------
REQUIRED_JSON_KEYS: list[str] = [
    "summary",
    "possible_conditions",
    "urgency_level",
    "recommended_next_steps",
    "questions_for_doctor",
    "warning_signs",
]

# ---------------------------------------------------------------------------
# Medical disclaimer text
# ---------------------------------------------------------------------------
MEDICAL_DISCLAIMER: str = (
    "⚠️ **IMPORTANT MEDICAL DISCLAIMER**\n\n"
    "This application is an **educational AI prototype** only. "
    "It is **NOT** a replacement for a licensed doctor, professional "
    "diagnosis, emergency service, or medical treatment.\n\n"
    "• It does **NOT** provide confirmed diagnoses.\n"
    "• Always consult a **qualified healthcare professional**.\n"
    "• In an emergency, call your local emergency number **immediately**.\n\n"
    "Any information provided is for **educational purposes only** and "
    "should not be used as the basis for medical decisions."
)

# ---------------------------------------------------------------------------
# Emergency warning text
# ---------------------------------------------------------------------------
EMERGENCY_WARNING: str = (
    "🚨 **SEEK EMERGENCY MEDICAL HELP IMMEDIATELY** 🚨\n\n"
    "Based on the information provided, this assessment indicates a "
    "**possible emergency**. Please:\n\n"
    "1. **Call your local emergency number** (e.g. 911, 999, 1122, 115) immediately.\n"
    "2. **Go to the nearest emergency room** if you can.\n"
    "3. **Do NOT wait** — time may be critical.\n\n"
    "This is an AI-generated preliminary assessment for educational "
    "purposes only. It is NOT a confirmed diagnosis."
)

# ---------------------------------------------------------------------------
# SQLite cache database path
# ---------------------------------------------------------------------------
SQLITE_CACHE_DB: str = ".langchain_cache.db"
