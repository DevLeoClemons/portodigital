from abc import ABC, abstractmethod
from google import genai
from playwright.sync_api import sync_playwright
import urllib.parse
import urllib.request
import base64
import json
import os


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.html")


class GerarCriativo(ABC):

    @abstractmethod
    def get_keywords(self, ideia_prompt):
        pass

    @abstractmethod
    def generate_prompts(self, ideia_prompt, keywords):
        pass

    @abstractmethod
    def generate_image(self, image_prompt):
        pass

    def render_post(self, image_url, image_text, tag="", brand="", output_path="post.png"):
        """Renders the HTML template to a 1080x1080 PNG using Playwright."""

        # Download image and embed as base64 so Playwright has no network dependency
        req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            image_data = base64.b64encode(resp.read()).decode("utf-8")

        image_src = f"data:image/jpeg;base64,{image_data}"

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        html = html.replace("{{IMAGE_URL}}", image_src)
        html = html.replace("{{IMAGE_TEXT}}", image_text)
        html = html.replace("{{TAG}}", tag)
        html = html.replace("{{BRAND}}", brand)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.set_content(html, wait_until="domcontentloaded")
            page.screenshot(path=output_path, clip={"x": 0, "y": 0, "width": 1080, "height": 1080})
            browser.close()

        return output_path

    def consolidate_creative(self, ideia_prompt, output_path="post.png", brand=""):

        keywords = self.get_keywords(ideia_prompt)

        image_prompt, image_text, post_description = (
            self.generate_prompts(ideia_prompt, keywords)
        )

        image_url = self.generate_image(image_prompt)

        tag = keywords[0] if keywords else ""

        post_path = self.render_post(
            image_url=image_url,
            image_text=image_text,
            tag=tag,
            brand=brand,
            output_path=output_path
        )

        return {
            "keywords": keywords,
            "prompts": {
                "image_prompt": image_prompt,
                "image_text": image_text,
                "description": post_description
            },
            "image_url": image_url,
            "post_path": post_path
        }


class GerarCriativoFake(GerarCriativo):

    def get_keywords(self, ideia_prompt):
        return ["marketing", "instagram", "vendas"]

    def generate_prompts(self, ideia_prompt, keywords):
        image_prompt = f"Imagem sobre {ideia_prompt} usando as keywords {keywords}"
        image_text = "Venda mais usando IA"
        description = "Post criado automaticamente para testes"
        return image_prompt, image_text, description

    def generate_image(self, image_prompt):
        encoded = urllib.parse.quote(image_prompt)
        return f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"


class GerarCriativoIA(GerarCriativo):

    def __init__(self):

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Variável de ambiente GEMINI_API_KEY não definida."
            )

        self.client = genai.Client(api_key=api_key)

    def get_keywords(self, ideia_prompt):
        return [
            ideia_prompt,
            "marketing digital",
            "automação",
            "inteligência artificial",
            "vendas"
        ]

    def generate_prompts(self, ideia_prompt, keywords):

        prompt_text = f"""
            Você é especialista em:

            - marketing digital
            - copywriting
            - social media
            - criação de anúncios
            - design de criativos

            Crie um criativo para Instagram.

            TEMA:
            {ideia_prompt}

            KEYWORDS:
            {keywords}

            Retorne APENAS JSON válido:

            {{
                "image_prompt": "",
                "image_text": "",
                "description": ""
            }}
            """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config={
                "response_mime_type": "application/json"
            }
        )

        data = json.loads(response.text)

        return (
            data["image_prompt"],
            data["image_text"],
            data["description"]
        )

    def generate_image(self, image_prompt):
        encoded = urllib.parse.quote(image_prompt)
        return f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"