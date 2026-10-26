import os
from google import genai

def generate_ai_remarks(glucose, haemoglobin, cholesterol):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: Gemini API key not configured."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are an AI medical assistant. Analyze the following blood test results for a patient:
        - Glucose: {glucose} mg/dL
        - Haemoglobin: {haemoglobin} g/dL
        - Cholesterol: {cholesterol} mg/dL

        Based on these values, provide a concise risk assessment for potential health conditions 
        (such as Diabetes, Anemia, or Cardiovascular Disease). 
        Keep your response under 3 sentences. Do not provide medical advice, just the risk prediction.
        """

        # Change to a currently supported model name
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )

        return response.text.strip()

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "AI prediction currently unavailable. Please try again later."