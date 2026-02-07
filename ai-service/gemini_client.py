import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_explanation(code, dtc_info, freeze_frame):
    prompt = f"""
    You are a professional automotive diagnostic assistant.
    Give a response in blog style with proper HTML tags only
    (<h1>, <h2>, <p>, <ol>, <li>, etc).
    Max 300 words.

    Fault Code: {code}
    Description: {dtc_info.get('tcode')}
    Sections: {dtc_info.get('sections')}

    Freeze Frame Sensor Data:
    {freeze_frame}

    Tasks:
    1. Explain what the ECU detected
    2. Interpret freeze-frame data
    3. Identify likely root cause
    4. Give step-by-step troubleshooting
    5. Explain simply for a car owner
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
