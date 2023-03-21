from os import getenv
from pathlib import Path
from threading import Thread
from urllib.parse import urlencode
import sounddevice as sd
import soundfile as sf


import keyboard
import requests
import pyperclip
import time
import unicodedata
import sys



BASE_URL = getenv('VOICEVOX_BASE_URL', 'http://127.0.0.1:50021')
VOICE_ID = int(getenv('VOICE_ID', 2))

SPEED_SCALE = float(getenv('SPEED_SCALE', 1))
VOLUME_SCALE = float(getenv('VOLUME_SCALE', 1.5))
INTONATION_SCALE = float(getenv('INTONATION_SCALE', 1))
PRE_PHONEME_LENGTH = float(getenv('PRE_PHONEME_LENGTH', 0.1))
POST_PHONEME_LENGTH = float(getenv('POST_PHONEME_LENGTH', 0.1))

EXIT_PROGRAM = False

WAV_PATH = Path(__file__).resolve().parent / 'audio\\'

WAVE_FILENAME_1 = 'tts1.wav'
WAVE_FILENAME_2 = 'tts2.wav'
WAV_FILE = WAV_PATH / WAVE_FILENAME_1
IS_FIRST_WAV = True

japanese_text_found_callback = None


def speak_jp(sentence):
    global WAV_FILE

    # Callback to report found jp if exists
    if japanese_text_found_callback != None:
        japanese_text_found_callback(sentence)

    # generate initial query data
    params_encoded = urlencode({'text': sentence, 'speaker': VOICE_ID})
    r = requests.post(f'{BASE_URL}/audio_query?{params_encoded}')

    if r.status_code == 404:
        print('Unable to reach Voicevox server, ensure that it is running. or VOICEVOX_BASE_URL is set correctly.')
        return

    voicevox_query = r.json()
    voicevox_query['speedScale'] = SPEED_SCALE
    voicevox_query['volumeScale'] = VOLUME_SCALE
    voicevox_query['intonationScale'] = INTONATION_SCALE
    voicevox_query['prePhonemeLength'] = PRE_PHONEME_LENGTH

    # synth voice as wav file
    params_encoded = urlencode({'speaker': VOICE_ID})
    r = requests.post(f'{BASE_URL}/synthesis?{params_encoded}', json=voicevox_query)

    switch_wav_file()

    with open(WAV_FILE, 'wb') as outfile:
        outfile.write(r.content)

    play_voice()

def switch_wav_file():
    global WAV_FILE
    global IS_FIRST_WAV

    if IS_FIRST_WAV:
        WAV_FILE = WAV_PATH / WAVE_FILENAME_1
    else:
        WAV_FILE = WAV_PATH / WAVE_FILENAME_2

    IS_FIRST_WAV = not IS_FIRST_WAV

def play_voice():
    global WAV_FILE

    data, fs = sf.read(WAV_FILE, dtype='float32')
    sd.stop()
    sd.play(data, fs)
    # try:
    #     sd.wait()
    # except KeyboardInterrupt:
    #     print("Stopped")
    #     sd.stop()


def check_clipboard():
    global EXIT_PROGRAM
    current_text = ''
    previous_text = ''
    while EXIT_PROGRAM == False:
        current_text = pyperclip.paste()
        if current_text != previous_text:
            print('New text: ' + current_text)
            previous_text = current_text
            # Check if the new text is Japanese
            is_japanese = check_if_japanese(current_text)
            if is_japanese:
                print("New Japanese text copied to clipboard: ", current_text)
                speak_jp(current_text)
        time.sleep(0.1)

def check_if_japanese(sentence):
    try:
        return any(
            unicodedata.name(c).startswith("HIRAGANA") or
            unicodedata.name(c).startswith("KATAKANA") or
            unicodedata.name(c).startswith("CJK UNIFIED") for c in sentence)
    except ValueError:
        return False

def stop_voice_play():
    print("Killing voice.")
    sd.stop()

def run_clipboard_voice():
    print('Using voiceid : ' + str(VOICE_ID))
    print('Ctrl+D to exit')
    print('Ctrl+alt+a to kill voice')

    # Create a keyboard listener
    keyboard.add_hotkey('ctrl+alt+a', stop_voice_play)

    check_clipboard()

    print("Ending clipboard observer...")

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) > 0:
        VOICE_ID = int(args[0])

    run_clipboard_voice()

