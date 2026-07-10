import google.generativeai as genai

def generate_scene_prompts(movie_name, script):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an AI Animation Director.

Movie: {movie_name}

Script:
{script}

Convert this script into 20 animation scenes.

For each scene generate:

1. Scene Number
2. Scene Description
3. Camera Angle
4. Image Prompt

Animation Style:
Pixar inspired 3D animation, cinematic lighting, expressive characters, colorful, ultra detailed, original design.

Return only scene prompts.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {e}"
