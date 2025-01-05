from dotenv import load_dotenv
import os

load_dotenv(".env")

VA_NAME = 'Jarvis'
VA_VER = "3.0"
VA_ALIAS = ('джарвис',)
VA_TBR = ('скажи', 'покажи', 'ответь', 'произнеси', 'расскажи', 'сколько', 'слушай')

MICROPHONE_INDEX = -1

CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

PICOVOICE_TOKEN = os.getenv('PICOVOICE_TOKEN')

OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
