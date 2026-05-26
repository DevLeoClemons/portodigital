from abc import ABC, abstractmethod
from pytrends.request import TrendReq
from openai import OpenAI

import json
import os


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

    def consolidate_creative(self, ideia_prompt):

        keywords = self.get_keywords(ideia_prompt)

        image_prompt, image_text, post_description = (
            self.generate_prompts(
                ideia_prompt,
                keywords
            )
        )

        image = self.generate_image(image_prompt)

        return {
            "keywords": keywords,

            "prompts": {
                "image_prompt": image_prompt,
                "image_text": image_text,
                "description": post_description
            },

            "image": image
        }


class GerarCriativoFake(GerarCriativo):

    def get_keywords(self, ideia_prompt):

        return [
            "marketing",
            "instagram",
            "vendas"
        ]

    def generate_prompts(self, ideia_prompt, keywords):

        image_prompt = (
            f"Imagem sobre {ideia_prompt} "
            f"usando as keywords {keywords}"
        )

        image_text = "Venda mais usando IA"

        description = (
            "Post criado automaticamente "
            "para testes"
        )

        return (
            image_prompt,
            image_text,
            description
        )

    def generate_image(self, image_prompt):

        return (
            f"Imagem fake gerada com o prompt: "
            f"{image_prompt}"
        )


class GerarCriativoIA(GerarCriativo):

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def get_keywords(self, ideia_prompt):

        pytrends = TrendReq(
            hl="pt-BR",
            tz=180
        )

        keywords = [
            ideia_prompt,
            "marketing digital",
            "automação"
        ]

        pytrends.build_payload(
            keywords,
            timeframe="today 3-m",
            geo="BR"
        )

        related_queries = pytrends.related_queries()

        trending_keywords = []

        for keyword in keywords:

            keyword_data = related_queries.get(keyword)

            if (
                keyword_data
                and keyword_data["top"] is not None
            ):

                top_df = keyword_data["top"]

                top_terms = (
                    top_df["query"]
                    .head(5)
                    .tolist()
                )

                trending_keywords.extend(top_terms)

        trending_keywords = list(
            set(trending_keywords)
        )

        return trending_keywords

    def generate_prompts(
        self,
        ideia_prompt,
        keywords
    ):

        response = (
            self.client.chat.completions.create(
                model="gpt-4.1-mini",

                messages=[
                    {
                        "role": "system",

                        "content": """
Você é especialista em:

- marketing digital
- copywriting
- social media
- criação de anúncios
- design de criativos
"""
                    },

                    {
                        "role": "user",

                        "content": f"""
Crie um criativo para Instagram.

TEMA:
{ideia_prompt}

KEYWORDS EM ALTA:
{keywords}

Crie:

1. Um prompt visual muito detalhado para geração de imagem

2. Um texto curto e chamativo para colocar na arte

3. Uma legenda persuasiva para Instagram

Retorne apenas JSON válido.

Formato:

{{
    "image_prompt": "",
    "image_text": "",
    "description": ""
}}
"""
                    }
                ]
            )
        )

        content = (
            response
            .choices[0]
            .message.content
        )

        data = json.loads(content)

        return (
            data["image_prompt"],
            data["image_text"],
            data["description"]
        )

    def generate_image(self, image_prompt):

        response = (
            self.client.images.generate(
                model="gpt-image-1",

                prompt=image_prompt,

                size="1024x1024"
            )
        )

        return response.data[0].url


criativo_fake = GerarCriativoFake()

resultado_fake = (
    criativo_fake.consolidate_creative(
        "automação para empresas"
    )
)

print(json.dumps(
    resultado_fake,
    indent=4,
    ensure_ascii=False
))


criativo_ia = GerarCriativoIA()

resultado_real = (
    criativo_ia.consolidate_creative(
        "automação com inteligência artificial"
    )
)

print(json.dumps(
    resultado_real,
    indent=4,
    ensure_ascii=False
))