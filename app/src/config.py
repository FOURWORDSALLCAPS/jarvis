import os

from dotenv import load_dotenv

load_dotenv(".env")

VA_NAME = "Jarvis"
VA_VER = "3.0"
VA_ALIAS = ("джарвис",)
VA_TBR = ("скажи", "покажи", "ответь", "произнеси", "расскажи", "сколько", "слушай")

MICROPHONE_INDEX = -1

PICOVOICE_TOKEN = os.getenv("PICOVOICE_TOKEN")

OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
