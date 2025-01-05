import json
import os
import queue
import random
import struct
import subprocess
import sys
import time

import pvporcupine
import simpleaudio as sa
import vosk
import yaml
from fuzzywuzzy import fuzz
from pvrecorder import PvRecorder
from rich import print

import config

from integrations.openai_api import gpt_answer


VA_CMD_LIST = yaml.safe_load(
    open('../commands/commands.yaml', 'rt', encoding='utf8'),
)


def play_sound(phrase):
    filename = f"../sound/"

    if phrase == "greet":
        filename += f"greet{random.choice([1, 2, 3])}.wav"
    elif phrase == "ok":
        filename += f"ok{random.choice([1, 2, 3])}.wav"
    elif phrase == "not_found":
        filename += "not_found.wav"
    elif phrase == "thanks":
        filename += "thanks.wav"
    elif phrase == "run":
        filename += "run.wav"
    elif phrase == "stupid":
        filename += "stupid.wav"
    elif phrase == "ready":
        filename += "ready.wav"
    elif phrase == "off":
        filename += "off.wav"

    wave_obj = sa.WaveObject.from_wave_file(filename)
    wave_obj.play()


def va_respond(voice: str):
    print(f"Распознано: {voice}")

    cmd = recognize_cmd(filter_cmd(voice))

    print(cmd)

    if len(cmd['cmd'].strip()) <= 0:
        return False
    elif cmd['percent'] < 70 or cmd['cmd'] not in VA_CMD_LIST.keys():
        if fuzz.ratio(voice.join(voice.split()[:1]).strip(), "скажи") > 75:

            message_log.append({"role": "user", "content": voice})
            response = gpt_answer()
            message_log.append({"role": "assistant", "content": response})

            recorder.stop()
            time.sleep(0.5)
            recorder.start()
            return False
        else:
            play_sound("not_found")
            time.sleep(1)

        return False
    else:
        execute_cmd(cmd['cmd'], voice)
        return True


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str, voice: str):
    if cmd == 'open_google':
        subprocess.Popen(['osascript', '../commands/run_google.scpt'])
        play_sound("ok")

    elif cmd == 'open_minecraft':
        subprocess.Popen(['osascript', '../commands/run_minecraft.scpt'])
        play_sound("ok")

    elif cmd == 'thanks':
        play_sound("thanks")

    elif cmd == 'stupid':
        play_sound("stupid")

    elif cmd == 'off':
        play_sound("off")

        porcupine.delete()
        exit(0)


def main():
    # ChatGPT vars
    system_message = {"role": "system", "content": "Ты голосовой ассистент из железного человека."}
    message_log = [system_message]

    # PORCUPINE
    porcupine = pvporcupine.create(
        access_key=config.PICOVOICE_TOKEN,
        keywords=['jarvis'],
        sensitivities=[1]
    )

    # VOSK
    model = vosk.Model("../vosk_model")
    samplerate = 16000
    device = config.MICROPHONE_INDEX
    kaldi_rec = vosk.KaldiRecognizer(model, samplerate)
    q = queue.Queue()

    # `-1` is the default input audio device.
    recorder = PvRecorder(device_index=config.MICROPHONE_INDEX, frame_length=porcupine.frame_length)
    recorder.start()
    print('Using device: %s' % recorder.selected_device)

    print(f"Jarvis (v3.0) начал свою работу ...")
    play_sound("run")
    time.sleep(0.5)

    ltc = time.time() - 1000

    while True:
        try:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                recorder.stop()
                play_sound("greet")
                print("Yes, sir.")
                recorder.start()  # prevent self-recording
                ltc = time.time()

            while time.time() - ltc <= 10:
                pcm = recorder.read()
                sp = struct.pack("h" * len(pcm), *pcm)

                if kaldi_rec.AcceptWaveform(sp):
                    if va_respond(json.loads(kaldi_rec.Result())["text"]):
                        ltc = time.time()

                    break

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


if __name__ == '__main__':
    main()
