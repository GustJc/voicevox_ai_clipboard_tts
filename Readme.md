# Voicevox clipboard AI

Simple clipboard monitor application.

When it detects a japanese text in the clipboard it will make a request to voicevox
to get the audio file generated and play it.

## How to use

You need to have voicevox running (see section bellow)

Execute it from the 'clipboard_voice_ui'.

```bash
python clipboard_voice_ui.py
```

Select the voice and style for the voices.
You can choose to copy from the clipboard or write the text on the box and click
the 'play voice' button.

### UI shortcuts

- `ctrl+alt+a` | Stop playing voice
- `win+z` | Play voice button shortcut
- `win+c` | Toggle auto-play from clipboard


## Running voicevox

Download a version of voicevox for your system https://github.com/VOICEVOX/voicevox/releases

It is highly recommended to use the GPU version if you can. 
It generates the voices almost instantaneously and uses almost nothing on the GPU and CPU.

Benchmark on my system (i7-7700 3.6GHz, Nvidea 1070)
- GPU version: 1-2 seconds delay. GPU goes up to 80% usage
- GPU version: instant. CPU and GPU are not affected. Maybe 1-5% increase.

### Important notes on how to use GPU version

It is important to notice that even if you download the GPU version, it will most likelly run with CPU.
You need to path the --use_gpu args
```bash
./run.exe --use_gpu --cpu_num_threads 2
```

### Warnings with Voicevox version 0.4.15 (pre-release)
The DirectML GPU version didn't work for me. It got an exception when trying to generate the voice.

I had to use the CUDA GPU version.