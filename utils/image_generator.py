import requests
import os

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def generate_image(prompt, output_file, hf_token):
    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=300
    )

    if response.status_code != 200:
        raise Exception(f"Hugging Face Error: {response.text}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "wb") as f:
        f.write(response.content)

    return output_file
