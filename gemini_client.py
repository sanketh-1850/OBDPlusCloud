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
    You are a professional automotive diagnostic writer.

    Generate a short, blog-style explanation of this fault code as clean HTML.

    STRICT FORMAT & STYLE RULES (VERY IMPORTANT):
    - Output MUST be ONLY HTML tags, with NO surrounding ``` blocks, NO plain text, and NO markdown.
    - Do NOT include <!DOCTYPE>, <html>, <head>, <body>, <style>, or <div> tags.
    - Use ONLY these tags: <h1>, <h2>, <p>, <strong>, <em>, <ol>, <ul>, <li>, <br>.
    - Every line of content MUST be inside one of those tags (no bare text).
    - Do NOT use **bold** markdown or \\n for newlines. Use <strong> for emphasis and proper block tags for structure.
    - Keep the response under 300 words.

    FAULT CONTEXT:
    - Fault Code: {code}
    - Description: {dtc_info['tcode']}
    - Sections (technical info, causes, fixes, etc.): {dtc_info.get('sections')}
    - Freeze Frame Sensor Data: {freeze_frame}

    WRITING TASK:
    1. Briefly explain what the ECU detected.
    2. Briefly interpret the freeze-frame data in context (only the key signals that matter).
    3. Briefly state the most likely root cause.
    4. Give clear, step-by-step troubleshooting / fix instructions.
    5. Finish with a simple explanation for a normal car owner.

    HTML STRUCTURE YOU MUST FOLLOW (IN THIS ORDER):

    1) Title and basic info:
    - One <h1> like: "Diagnosing {code}: {dtc_info['tcode']}"
    - One <p><strong>Fault Code: ...</strong></p>
    - One <p><strong>Description: ...</strong></p>

    2) ECU detection + freeze-frame interpretation:
    - <h2>ECU Detection Summary</h2>
    - One or two <p> elements for what the ECU detected. (Task 1)
    - <h2>Freeze-Frame Data Interpretation</h2>
    - One or two <p> elements that interpret key freeze-frame values. (Task 2)

    3) Symptoms + likely cause:
    - <h2>Symptoms and Likely Cause</h2>
    - One <p> describing typical symptoms in 1–2 sentences.
    - One <p> explaining the most likely root cause. (Task 3)

    4) Troubleshooting steps:
    - <h2>Step-by-Step Troubleshooting and Fix</h2>
    - One <ol> with 4–7 <li> steps, each starting with a short <strong>label</strong> and then a brief explanation. (Task 4)

    5) Simple owner-facing summary:
    - <h2>Simple Explanation for Car Owners</h2>
    - One <p> that explains the issue in simple, non-technical language. (Task 5)

    REMEMBER:
    - Do NOT include any tags other than the ones listed.
    - Do NOT escape the HTML; write real tags like <h1> and <p>, not &lt;h1&gt;.
    - Do NOT include any extra commentary or explanation outside of the HTML.
    """
    
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"