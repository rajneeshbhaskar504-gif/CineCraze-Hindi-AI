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

Return in a format where each scene starts with the word 'Scene'.
"""

        response = model.generate_content(prompt)

        # 20 Scenes ki List generate karna
        scenes = [
            "Scene" + scene.strip()
            for scene in response.text.split("Scene")
            if scene.strip()
        ]

        return scenes

    except Exception as e:
        return [f"Error: {e}"]
