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
    prompt = f"""
    You are a professional automotive diagnostic assistant. Give me a response in a blog style with correct headers, etc. Do not respond as if you are responding in a conversation. Response should be a maximum of 300 words. Response should be in HTML format without <div>. Must consist only tags like <h1>, <p>, <h2>, <ol>, <li>, etc.

    Fault Code: {code}
    Description: {dtc_info['tcode']}
    Sections: {dtc_info.get('sections')}

    Freeze Frame Sensor Data:
    {freeze_frame}

    TASK:
    1. Briefly explain what the ECU detected.
    2. Briefly Interpret freeze-frame data in context.
    3. Briefly provide the most likely root cause.
    4. Give clear, step-by-step troubleshooting/fix instructions.
    5. Explain in simple terms for a normal car owner.

    Response format:
    1. Code and description. Then Task 1 and task 2 respectively.
    2. One - Two sentences on Symptoms then task 3.
    3. Task 4
    4. Briefly do task 5
    """


    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"