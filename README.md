# Jarvis v3.0
Simple Voice Assistant made as an experiment using [Silero](https://github.com/snakers4/silero-models) & [Vosk](https://pypi.org/project/vosk/).
<br>Later on [Picovoice Porcupine Wake Word Detection](https://picovoice.ai/platform/porcupine/) & [ChatGPT](https://chat.openai.com/) was added.

# OS
The code works strictly under MacOS.
The original is written in Rust and works under Windows.

# Installation
Install dependencies into the virtual environment
```sh
pip install -r requirements.txt
```

Create a `.env` file in the root of the project, similar to the `example.env`

Run script

```sh
python main.py
```

And don't forget to put models of Vosk to main folder.<br>
You can get the latest from the [official website.](https://alphacephei.com/vosk/models)
<br>The one I was using is `small`.
<br>p.s. If you don't understand how to install or where to put the Vosk model, I've made a [screenshot](https://i.imgur.com/N3bu2lC.png) for you.

# Python version
I was using Python `3.9.10`.

# Author
(2025) Vladimir Zaitsev

# Forked from 
[Abraham Tugalov](https://github.com/Priler/jarvis)
