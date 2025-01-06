import re

import config
from openai import OpenAI, OpenAIError


def gpt_answer(voice):
    client = OpenAI(
        api_key=config.OPENAI_TOKEN,
    )
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": voice,
                }
            ],
            model="gpt-4o-mini",
        )
    except OpenAIError as error:
        response = "Непредвиденная ошибка"
        print(f"{error}")
        error_message = (re.search(r"'message': '([^:']*)", str(error))).group(1)
        if error_message.startswith("Incorrect API key provided"):
            response = "Предоставлен неверный ключ API"

        if error_message.startswith("Country, region, or territory not supported"):
            response = "Страна, регион или территория не поддерживается"

        return response
    return response.choices[0].message.content
