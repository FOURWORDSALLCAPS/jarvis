import time
from json import loads
from random import randint
from struct import pack
from subprocess import Popen

import config
from base import kaldi_rec, porcupine, recorder
from fuzzywuzzy import fuzz
from integrations.openai_api import gpt_answer
from silero_tts.silero_tts import SileroTTS
from simpleaudio import WaveObject
from yaml import safe_load

VA_CMD_LIST = safe_load(
    open("../commands/commands.yaml", encoding="utf8"),
)


def play_sound(filename):
    filepath = "../sound/"
    filepath += filename
    wave_obj = WaveObject.from_wave_file(filepath)
    wave_obj.play()


def va_respond(voice: str):
    print(f"Распознано: {voice}")

    cmd = recognize_cmd(voice)

    print(cmd)

    if cmd["cmd"] and len(cmd["cmd"].strip()) <= 0:
        return False
    elif cmd["percent"] < 70 or cmd["cmd"] not in VA_CMD_LIST.keys():
        if fuzz.ratio(voice.join(voice.split()[:1]).strip(), "скажи") > 75:
            play_sound("ready.wav")
            response = gpt_answer(voice)
            tts = SileroTTS(
                model_id="v4_ru",
                language="ru",
                speaker="aidar",
                sample_rate=48000,
                device="cpu",
            )
            tts.tts(response, "../sound/gpt_answer.wav")

            filename = "../sound/gpt_answer.wav"
            wave_obj = WaveObject.from_wave_file(filename)
            wave_obj.play()
            time.sleep(1)
            return False
        else:
            play_sound("not_found.wav")
            time.sleep(1)
        return False
    else:
        execute_cmd(cmd["cmd"])
        return True


def recognize_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    rc = {"cmd": "", "percent": 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)

            if vrt > rc["percent"]:
                rc["cmd"] = c
                rc["percent"] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == "open_google":
        Popen(["osascript", "../commands/run_google.scpt"])
        play_sound(f"ok{randint(1, 3)}.wav")

    elif cmd == "open_minecraft":
        Popen(["osascript", "../commands/run_minecraft.scpt"])
        play_sound(f"ok{randint(1, 3)}.wav")

    elif cmd == "thanks":
        play_sound("thanks.wav")

    elif cmd == "stupid":
        play_sound("stupid.wav")

    elif cmd == "off":
        play_sound("off.wav")
        time.sleep(1)

        porcupine.delete()
        exit(0)


def main():
    recorder.start()
    print("Jarvis (v3.0) начал свою работу ...")
    play_sound("run.wav")
    time.sleep(0.5)
    ltc = time.time() - 1000

    while True:
        try:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                recorder.stop()
                play_sound(f"greet{randint(1, 3)}.wav")
                print("Yes, sir.")
                recorder.start()
                ltc = time.time()

            while time.time() - ltc <= 10:
                pcm = recorder.read()
                sp = pack("h" * len(pcm), *pcm)

                if kaldi_rec.AcceptWaveform(sp):
                    if va_respond(loads(kaldi_rec.Result())["text"]):
                        ltc = time.time()

                    break

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


if __name__ == "__main__":
    main()
