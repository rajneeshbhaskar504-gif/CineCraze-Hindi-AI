import google.generativeai as genai

def generate_image_prompt(scene):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
Create one detailed animation image prompt.

Style:
Original 3D animated movie, cinematic lighting, expressive characters, ultra detailed.

Scene:

{scene}

Return only the image prompt.
"""

    response = model.generate_content(prompt)

    return response.text
