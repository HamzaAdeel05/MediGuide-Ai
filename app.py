"""
app.py - MediGuide AI Streamlit Application
=============================================

MediGuide AI
Professional Maroon + Navy UI

IMPORTANT:
This is an EDUCATIONAL AI prototype, NOT a medical device.
It does NOT provide confirmed diagnoses.
"""

import streamlit as st
import time

# ---------------------------------------------------------------------------
# Backend imports
# ---------------------------------------------------------------------------

from src.config import (
    get_api_key,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    SYMPTOM_OPTIONS,
    DURATION_OPTIONS,
    GENDER_OPTIONS,
    LANGUAGE_OPTIONS,
    MEDICAL_DISCLAIMER,
    EMERGENCY_WARNING,
    URGENCY_LEVELS,
)

from src.chains import (
    get_llm,
    get_assessment_chain,
    run_assessment_chain,
    stream_narrative,
    demonstrate_messages,
)

from src.prompts import JSON_SCHEMA
from src.cache_manager import setup_cache

from src.utils import (
    safe_parse_json,
    validate_assessment,
    format_symptoms,
    validate_age,
)


# ===========================================================================
# PAGE CONFIG
# ===========================================================================

st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===========================================================================
# MAROON + NAVY THEME
# ===========================================================================

st.markdown(
    """
    <style>

    /* =========================================================
       COLOR PALETTE
    =========================================================

       Navy       #101B33
       Navy 2     #172642
       Navy 3     #1F3154
       Maroon     #7A1F3D
       Burgundy   #641832
       Cream      #FAF8F6
       White      #FFFFFF
       Border     #33415D
       Text       #202938
       Muted      #697386
    ========================================================= */


    /* =========================================================
       APP BACKGROUND
    ========================================================= */

    .stApp {
        background-color: #FAF8F6;
        color: #202938;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =========================================================
       HIDE DEFAULT STREAMLIT UI
    ========================================================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* =========================================================
       TYPOGRAPHY
    ========================================================= */

    h1 {
        color: #101B33 !important;
        font-weight: 850 !important;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #101B33 !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #172642 !important;
        font-weight: 650 !important;
    }

    p {
        color: #697386;
    }


    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {
        background-color: #101B33 !important;
        border-right: 1px solid #253451;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #D7DCE5 !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #AEB7C7 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #2A3854 !important;
    }


    /* =========================================================
       SIDEBAR SELECTBOX
    ========================================================= */

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {

        background-color: #172642 !important;

        border: 1px solid #33415D !important;

        color: #FFFFFF !important;

        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="input"] > div {

        background-color: #172642 !important;

        border: 1px solid #33415D !important;

        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"]
    input {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* =========================================================
       MAIN INPUTS
    ========================================================= */

    div[data-baseweb="input"] > div {

        background-color: #172642 !important;

        border: 1px solid #33415D !important;

        border-radius: 8px !important;

        color: #FFFFFF !important;
    }

    div[data-baseweb="textarea"] > div {

        background-color: #172642 !important;

        border: 1px solid #33415D !important;

        border-radius: 8px !important;

        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] > div {

        background-color: #172642 !important;

        border: 1px solid #33415D !important;

        border-radius: 8px !important;

        color: #FFFFFF !important;
    }


    /* =========================================================
       SELECTBOX TEXT
    ========================================================= */

    div[data-baseweb="select"] span {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }

    div[data-baseweb="select"] input {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* =========================================================
       INPUT TEXT
    ========================================================= */

    input,
    textarea {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* =========================================================
       PLACEHOLDER TEXT
    ========================================================= */

    input::placeholder,
    textarea::placeholder {

        color: #FFFFFF !important;

        opacity: 0.75 !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }

    div[data-baseweb="input"] input::placeholder {

        color: #FFFFFF !important;

        opacity: 0.75 !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }

    div[data-baseweb="textarea"] textarea::placeholder {

        color: #FFFFFF !important;

        opacity: 0.75 !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* =========================================================
       SIDEBAR PLACEHOLDER
    ========================================================= */

    section[data-testid="stSidebar"]
    input::placeholder {

        color: #FFFFFF !important;

        opacity: 0.75 !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* =========================================================
       INPUT FOCUS
    ========================================================= */

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {

        border-color: #7A1F3D !important;

        box-shadow:
            0 0 0 1px #7A1F3D !important;
    }


    /* =========================================================
       LABELS
    ========================================================= */

    label {

        color: #344054 !important;

        font-weight: 600 !important;
    }


    /* =========================================================
       SIDEBAR LABELS
    ========================================================= */

    section[data-testid="stSidebar"] label {

        color: #D7DCE5 !important;
    }


    /* =========================================================
       ANALYSE BUTTON
       GREEN BACKGROUND + WHITE TEXT
    ========================================================= */

    .stButton > button {

        background-color: #198754 !important;

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;

        border: none !important;

        border-radius: 8px !important;

        min-height: 48px;

        font-size: 1rem;

        font-weight: 650 !important;

        transition: all 0.2s ease;

        box-shadow:
            0 4px 12px rgba(25, 135, 84, 0.20);
    }


    /* Force button text to WHITE */

    .stButton > button p,
    .stButton > button span,
    .stButton > button div {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;

        font-weight: 650 !important;
    }


    /* Hover */

    .stButton > button:hover {

        background-color: #157347 !important;

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;

        transform: translateY(-1px);

        box-shadow:
            0 6px 16px rgba(25, 135, 84, 0.28);
    }


    .stButton > button:hover p,
    .stButton > button:hover span,
    .stButton > button:hover div {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* Active */

    .stButton > button:active {

        background-color: #146C43 !important;

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    .stButton > button:active p,
    .stButton > button:active span,
    .stButton > button:active div {

        color: #FFFFFF !important;

        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* =========================================================
       HEADERS / BRAND ACCENT
    ========================================================= */

    .maroon-line {

        height: 3px;

        width: 55px;

        background-color: #7A1F3D;

        border-radius: 10px;

        margin-top: -10px;

        margin-bottom: 25px;
    }


    /* =========================================================
       METRIC CARDS
    ========================================================= */

    div[data-testid="stMetric"] {

        background-color: #FFFFFF;

        border: 1px solid #E5E1E1;

        border-radius: 10px;

        padding: 1rem;

        box-shadow:
            0 3px 12px rgba(16, 27, 51, 0.04);
    }

    div[data-testid="stMetricLabel"] {

        color: #697386 !important;
    }

    div[data-testid="stMetricValue"] {

        color: #7A1F3D !important;

        font-weight: 750 !important;
    }


    /* =========================================================
       TABS
    ========================================================= */

    button[data-baseweb="tab"] {

        color: #697386;

        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        color: #7A1F3D !important;
    }

    div[data-baseweb="tab-highlight"] {

        background-color: #7A1F3D !important;
    }


    /* =========================================================
       EXPANDERS
    ========================================================= */

    div[data-testid="stExpander"] {

        background-color: #FFFFFF;

        border: 1px solid #E5E1E1;

        border-radius: 9px;
    }


    /* =========================================================
       ALERTS
    ========================================================= */

    div[data-testid="stAlert"] {

        border-radius: 9px;
    }


    /* =========================================================
       DIVIDERS
    ========================================================= */

    hr {

        border-color: #E5E1E1 !important;
    }


    /* =========================================================
       SLIDER
    ========================================================= */

    div[data-testid="stSlider"] {

        color: #7A1F3D !important;
    }


    /* =========================================================
       MOBILE
    ========================================================= */

    @media (max-width: 768px) {

        .main .block-container {

            padding-left: 1rem;

            padding-right: 1rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ===========================================================================
# SIDEBAR
# ===========================================================================

def render_sidebar() -> dict:

    with st.sidebar:

        st.markdown(
            """
            <div style="
                font-size:1.45rem;
                font-weight:750;
                color:white;
                margin-bottom:4px;
            ">
                🏥 MediGuide AI
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "Medical Symptom Assessment"
        )

        st.divider()

        st.markdown(
            "### Application"
        )

        st.caption(
            "Use this application to generate "
            "AI-powered educational health guidance "
            "from patient-provided symptoms."
        )

        st.divider()

        st.markdown(
            "### Important"
        )

        st.warning(
            MEDICAL_DISCLAIMER
        )

        st.divider()

        st.markdown(
            "### AI Configuration"
        )

        selected_model = st.selectbox(
            "AI Model",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(
                DEFAULT_MODEL
            ),
            help="Choose the OpenAI model.",
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
            help=(
                "Lower values produce more focused "
                "and deterministic responses."
            ),
        )

        st.divider()

        st.markdown(
            "### Language"
        )

        sidebar_language = st.selectbox(
            "Response Language",
            options=LANGUAGE_OPTIONS,
            index=0,
            key="sidebar_language",
        )

        st.divider()

        st.markdown(
            "### Performance"
        )

        cache_type = st.selectbox(
            "Cache Type",
            options=[
                "None",
                "InMemoryCache",
                "SQLiteCache",
            ],
            index=0,
        )

        cache_status = setup_cache(
            cache_type
        )

        with st.expander(
            "Cache Status"
        ):

            st.markdown(
                cache_status
            )

        st.divider()

        st.caption(
            "MediGuide AI · Educational Prototype"
        )

    return {
        "model": selected_model,
        "temperature": temperature,
        "sidebar_language": sidebar_language,
        "cache_type": cache_type,
    }


# ===========================================================================
# INPUT FORM
# ===========================================================================

def render_input_form(
    sidebar_language: str,
) -> dict | None:

    st.title(
        "MediGuide AI"
    )

    st.markdown(
        """
        **AI-powered medical symptom assessment**

        Enter patient information and symptoms below to generate
        structured educational health guidance.
        """
    )

    st.markdown(
        '<div class="maroon-line"></div>',
        unsafe_allow_html=True,
    )

    st.info(
        MEDICAL_DISCLAIMER
    )

    st.header(
        "Patient Information"
    )

    st.caption(
        "Fields marked with * are required."
    )

    col1, col2 = st.columns(
        2,
        gap="large",
    )

    with col1:

        age_input = st.text_input(
            "Patient Age *",
            placeholder="e.g. 25",
            help=(
                "Enter the patient's age "
                "as a whole number."
            ),
        )

        gender = st.selectbox(
            "Gender *",
            options=GENDER_OPTIONS,
            help="Select the patient's gender.",
        )

    with col2:

        duration = st.selectbox(
            "Duration of Symptoms *",
            options=DURATION_OPTIONS,
            help=(
                "How long have the symptoms "
                "been present?"
            ),
        )

        severity = st.slider(
            "Severity (1 = mild, 10 = severe) *",
            min_value=1,
            max_value=10,
            value=5,
            help=(
                "Rate the overall severity "
                "of the symptoms."
            ),
        )

    st.divider()

    st.header(
        "Symptoms"
    )

    selected_symptoms = st.multiselect(
        "Symptoms *",
        options=SYMPTOM_OPTIONS,
        help=(
            "Choose one or more symptoms "
            "from the list."
        ),
    )

    free_text_symptoms = st.text_input(
        "Additional Symptoms",
        placeholder="e.g. ear pain, swollen glands",
        help=(
            "Enter symptoms that aren't "
            "available in the list."
        ),
    )

    st.divider()

    st.header(
        "Medical Background"
    )

    medical_conditions = st.text_area(
        "Existing Medical Conditions",
        placeholder="e.g. diabetes, hypertension, asthma",
        help=(
            "List any pre-existing "
            "medical conditions."
        ),
    )

    medications = st.text_area(
        "Current Medications",
        placeholder="e.g. metformin 500mg, lisinopril 10mg",
        help=(
            "List any medications currently "
            "being taken."
        ),
    )

    additional_notes = st.text_area(
        "Additional Notes",
        placeholder="e.g. recently travelled, family history",
        help=(
            "Any other relevant information."
        ),
    )

    st.divider()

    st.header(
        "Response Preferences"
    )

    language = st.selectbox(
        "Answer Language *",
        options=LANGUAGE_OPTIONS,
        index=LANGUAGE_OPTIONS.index(
            sidebar_language
        ),
        help=(
            "The AI will respond "
            "in this language."
        ),
        key="form_language",
    )

    st.write("")

    submitted = st.button(
        "Analyse Symptoms",
        type="primary",
        use_container_width=True,
    )

    if submitted:

        return {
            "age_input": age_input,
            "gender": gender,
            "selected_symptoms": selected_symptoms,
            "free_text_symptoms": free_text_symptoms,
            "duration": duration,
            "severity": severity,
            "language": language,
            "medical_conditions": (
                medical_conditions
                or "None reported"
            ),
            "medications": (
                medications
                or "None reported"
            ),
            "additional_notes": (
                additional_notes
                or "None"
            ),
        }

    return None


# ===========================================================================
# INPUT VALIDATION
# ===========================================================================

def validate_inputs(
    form_data: dict,
) -> tuple[bool, list[str]]:

    errors: list[str] = []

    age_valid, age_msg = validate_age(
        form_data["age_input"]
    )

    if not age_valid:

        errors.append(
            age_msg
        )

    symptoms_combined = format_symptoms(
        form_data["selected_symptoms"],
        form_data["free_text_symptoms"],
    )

    if symptoms_combined == "None reported":

        errors.append(
            "Please select at least one symptom "
            "or type an additional symptom."
        )

    return len(errors) == 0, errors


# ===========================================================================
# URGENCY DISPLAY
# ===========================================================================

def render_urgency_display(
    urgency: str,
) -> None:

    urgency = urgency.upper()

    if urgency == "EMERGENCY":

        st.error(
            EMERGENCY_WARNING
        )

    elif urgency == "HIGH":

        st.error(
            "**Urgency Level: HIGH**\n\n"
            "The symptoms described are concerning. "
            "Please seek medical attention promptly.\n\n"
            "This is an AI-generated preliminary assessment "
            "for educational purposes only — NOT a confirmed diagnosis."
        )

    elif urgency == "MEDIUM":

        st.warning(
            "**Urgency Level: MEDIUM**\n\n"
            "The symptoms described warrant professional "
            "medical evaluation within a reasonable timeframe.\n\n"
            "This is an AI-generated preliminary assessment "
            "for educational purposes only — NOT a confirmed diagnosis."
        )

    else:

        st.success(
            "**Urgency Level: LOW**\n\n"
            "Based on this preliminary assessment, the symptoms "
            "appear minor. Self-care and monitoring may be appropriate.\n\n"
            "Consulting a healthcare professional is still recommended."
        )


# ===========================================================================
# RESULTS DASHBOARD
# ===========================================================================

def render_results_dashboard(
    assessment: dict,
    form_data: dict,
) -> None:

    st.divider()

    st.header(
        "Assessment Results"
    )

    st.caption(
        "AI-generated information based on the "
        "patient information provided."
    )

    st.warning(
        "These results are generated by AI for educational "
        "purposes only. They are NOT a confirmed medical diagnosis."
    )

    render_urgency_display(
        assessment["urgency_level"]
    )

    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Summary",
            "Possible Conditions",
            "Next Steps & Questions",
            "Warning Signs",
        ]
    )

    with tab1:

        st.subheader(
            "Patient Summary"
        )

        col1, col2, col3, col4 = st.columns(
            4
        )

        with col1:

            st.metric(
                "Age",
                form_data["age_input"],
            )

        with col2:

            st.metric(
                "Gender",
                form_data["gender"],
            )

        with col3:

            st.metric(
                "Severity",
                f"{form_data['severity']}/10",
            )

        with col4:

            st.metric(
                "Urgency",
                assessment["urgency_level"],
            )

        st.write("")

        symptoms_str = format_symptoms(
            form_data["selected_symptoms"],
            form_data["free_text_symptoms"],
        )

        col1, col2 = st.columns(
            2,
            gap="large",
        )

        with col1:

            st.markdown(
                "**Symptoms**"
            )

            st.write(
                symptoms_str
            )

            st.markdown(
                "**Duration**"
            )

            st.write(
                form_data["duration"]
            )

        with col2:

            st.markdown(
                "**Existing Conditions**"
            )

            st.write(
                form_data["medical_conditions"]
            )

            st.markdown(
                "**Current Medications**"
            )

            st.write(
                form_data["medications"]
            )

        if form_data["additional_notes"] != "None":

            st.markdown(
                "**Additional Notes**"
            )

            st.write(
                form_data["additional_notes"]
            )

        st.divider()

        st.subheader(
            "AI-Generated General Information"
        )

        st.info(
            "Educational information only — "
            "not a medical diagnosis."
        )

        st.markdown(
            assessment["summary"]
        )

    with tab2:

        st.subheader(
            "Possible Conditions"
        )

        st.warning(
            "These are possible conditions for educational "
            "purposes only. They are NOT confirmed diagnoses."
        )

        if assessment["possible_conditions"]:

            for i, condition in enumerate(
                assessment["possible_conditions"],
                1,
            ):

                with st.expander(
                    condition.get(
                        "name",
                        "Unknown",
                    ),
                    expanded=(i == 1),
                ):

                    st.markdown(
                        "**Reason**"
                    )

                    st.write(
                        condition.get(
                            "reason",
                            "N/A",
                        )
                    )

                    st.caption(
                        "Educational information only."
                    )

        else:

            st.info(
                "No specific conditions were "
                "identified by the model."
            )

    with tab3:

        col_steps, col_questions = st.columns(
            2,
            gap="large",
        )

        with col_steps:

            st.subheader(
                "Recommended Next Steps"
            )

            if assessment["recommended_next_steps"]:

                for step in assessment["recommended_next_steps"]:

                    st.markdown(
                        f"- {step}"
                    )

            else:

                st.info(
                    "No specific next steps were provided."
                )

        with col_questions:

            st.subheader(
                "Questions for Your Doctor"
            )

            st.info(
                "Consider asking these questions "
                "during your appointment."
            )

            if assessment["questions_for_doctor"]:

                for question in assessment["questions_for_doctor"]:

                    st.markdown(
                        f"- {question}"
                    )

            else:

                st.info(
                    "No specific questions were suggested."
                )

    with tab4:

        st.subheader(
            "Warning Signs Requiring Immediate Attention"
        )

        if assessment["warning_signs"]:

            for sign in assessment["warning_signs"]:

                st.error(
                    sign
                )

            st.divider()

            st.error(
                "If you experience any of the warning signs "
                "above, seek medical help immediately."
            )

        else:

            st.info(
                "No specific warning signs were identified. "
                "However, if your condition worsens, "
                "please seek medical attention."
            )

    st.divider()

    st.warning(
        "FINAL REMINDER: This assessment is generated by an AI "
        "system for educational purposes only. It is NOT a "
        "substitute for professional medical advice, diagnosis, "
        "or treatment."
    )


# ===========================================================================
# MAIN APPLICATION
# ===========================================================================

def main():

    sidebar_config = render_sidebar()

    form_data = render_input_form(
        sidebar_config["sidebar_language"]
    )

    if form_data is None:

        return

    is_valid, errors = validate_inputs(
        form_data
    )

    if not is_valid:

        for error in errors:

            st.warning(
                error
            )

        st.info(
            "Please correct the above issues "
            "and try again."
        )

        return

    api_key = get_api_key()

    if not api_key:

        st.error(
            "OpenAI API key not found!"
        )

        st.code(
            "OPENAI_API_KEY=sk-your-key-here",
            language="bash",
        )

        return

    symptoms_str = format_symptoms(
        form_data["selected_symptoms"],
        form_data["free_text_symptoms"],
    )

    chain_inputs = {
        "age": form_data["age_input"],
        "gender": form_data["gender"],
        "symptoms": symptoms_str,
        "duration": form_data["duration"],
        "severity": str(
            form_data["severity"]
        ),
        "medical_conditions": form_data["medical_conditions"],
        "medications": form_data["medications"],
        "additional_notes": form_data["additional_notes"],
        "language": form_data["language"],
    }

    try:

        llm = get_llm(
            api_key=api_key,
            model=sidebar_config["model"],
            temperature=sidebar_config["temperature"],
        )

    except Exception as e:

        st.error(
            f"Failed to initialize the AI model: {e}"
        )

        return

    st.divider()

    st.subheader(
        "Generating Assessment"
    )

    try:

        start_time = time.time()

        chain = get_assessment_chain(
            llm
        )

        raw_response = run_assessment_chain(
            chain,
            chain_inputs,
        )

        elapsed = time.time() - start_time

        st.success(
            f"Assessment generated successfully "
            f"in {elapsed:.1f} seconds."
        )

    except Exception as e:

        st.error(
            f"API Error: {e}\n\n"
            "Please check your API key and internet connection."
        )

        return

    parsed, parse_error = safe_parse_json(
        raw_response
    )

    if parse_error:

        st.error(
            "Failed to parse the AI response."
        )

        st.warning(
            parse_error
        )

        return

    assessment, validation_warnings = validate_assessment(
        parsed
    )

    if validation_warnings:

        with st.expander(
            "Response Validation Warnings"
        ):

            for warning in validation_warnings:

                st.warning(
                    warning
                )

    st.divider()

    st.subheader(
        "AI Health Guidance"
    )

    st.caption(
        "Live educational guidance generated by the AI."
    )

    st.info(
        "This guidance is educational information only "
        "and is NOT a medical diagnosis."
    )

    try:

        st.write_stream(
            stream_narrative(
                llm,
                chain_inputs,
            )
        )

    except Exception as e:

        st.warning(
            f"Streaming encountered an issue: {e}\n\n"
            "The structured assessment below is still available."
        )

    render_results_dashboard(
        assessment,
        form_data,
    )

    with st.expander(
        "LangChain Message Types Demo"
    ):

        st.markdown(
            """
            **SystemMessage** — defines rules and behaviour.

            **HumanMessage** — represents user input.

            **AIMessage** — represents the AI response.
            """
        )

        try:

            demo_result = demonstrate_messages(
                llm,
                symptoms_str,
            )

            st.markdown(
                demo_result
            )

        except Exception as e:

            st.warning(
                f"Demo encountered an issue: {e}"
            )

        st.caption(
            "This demonstrates how SystemMessage, "
            "HumanMessage, and AIMessage work together."
        )

    st.divider()

    st.caption(
        "MediGuide AI · Educational Prototype · "
        "Not a substitute for professional medical advice"
    )


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    main()