import base64
import requests
import os

class Together:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.together.ai"

    def create_completion(self, model, messages):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

def ocr(file_path, api_key=None, model="Llama-3.2-90B-Vision"):
    api_key = api_key or os.getenv("TOGETHER_API_KEY")
    vision_llm = (
        "meta-llama/Llama-Vision-Free"
        if model == "free"
        else f"meta-llama/{model}-Instruct-Turbo"
    )

    together = Together(api_key)
    final_markdown = get_markdown(together, vision_llm, file_path)
    return final_markdown

def get_markdown(together, vision_llm, file_path):
    system_prompt = """Convert the provided image into Markdown format. Ensure that all content from the page is included, such as headers, footers, subtexts, images (with alt text if possible), tables, and any other elements.

Requirements:

- Output Only Markdown: Return solely the Markdown content without any additional explanations or comments.
- No Delimiters: Do not use code fences or delimiters like ```markdown.
- Complete Content: Do not omit any part of the page, including headers, footers, and subtext."""

    final_image_url = (
        file_path if is_remote_file(file_path) else f"data:image/jpeg;base64,{encode_image(file_path)}"
    )

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": system_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": final_image_url,
                    },
                },
            ],
        }
    ]

    output = together.create_completion(model=vision_llm, messages=messages)
    return output["choices"][0]["message"]["content"]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def is_remote_file(file_path):
    return file_path.startswith("http://") or file_path.startswith("https://")
