import google.generativeai as genai

def generate_image_prompt(scene):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Create ONE detailed animation image prompt.

Style:
Original 3D animated movie,
Pixar-inspired,
cinematic lighting,
expressive characters,
ultra detailed,
8K quality.

Scene:
{scene}

Return ONLY the image prompt.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {e}"
