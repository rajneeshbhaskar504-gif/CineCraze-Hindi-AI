import google.generativeai as genai

def generate_scene_prompts(movie_name, script):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an AI Animation Director.

Movie: {movie_name}

Script:
{script}

Convert this script into 20 animation scenes.

For each scene generate:

Scene Number

Scene Description

Animation Style:
Pixar inspired 3D, cinematic lighting, expressive characters, colorful, ultra detailed, original design

Camera Angle

Image Prompt

Return only scene prompts.
"""

    response = model.generate_content(prompt)

    return response.text
