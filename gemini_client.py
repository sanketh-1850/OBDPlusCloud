import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_explanation(code, dtc_info, freeze_frame):
    """
    Creates a diagnostic explanation using Gemini.
    Uses:
      - DTC description
      - Causes & fixes from DB
      - Freeze-frame sensor data
    """
    prompt = f"""
    You are a professional automotive diagnostic assistant.

    Fault Code: {code}
    Description: {dtc_info['tcode']}
    Sections: {dtc_info.get('sections')}

    Freeze Frame Sensor Data:
    {freeze_frame}

    TASK:
    1. Explain what the ECU detected.
    2. Interpret freeze-frame data in context.
    3. Provide the most likely root cause.
    4. Give clear, step-by-step troubleshooting instructions.
    5. Explain in simple terms for a normal car owner.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"