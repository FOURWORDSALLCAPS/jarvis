import openai
import config


system_message = {"role": "system", "content": "Ты голосовой ассистент из железного человека."}
message_log = [system_message]
openai.api_key = config.OPENAI_TOKEN


def gpt_answer():
    model_engine = "gpt-3.5-turbo"
    max_tokens = 256
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=message_log,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=1,
            stop=None
        )
    except openai.OpenAIError as ex:
        print(f"openai error: {ex}")
        return gpt_answer()

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content
