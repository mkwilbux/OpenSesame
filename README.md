# OpenSeshell
name change due to existing opensesame project

Project is now found at:
https://github.com/mkwilbux/Seshell

## Author: Marcia K Wilbur
## Date: 2/2025
## This is just the beginning!

Voice activated open terminal or launch terminal using vosk, kaldi and pretrained model. For different languages, get and set path for other models.

## Steps:
- Capture voice input using a microphone.
- Convert speech to text using a speech recognition engine.
- Process the text with NLP to determine intent.
- Execute terminal commands via subprocess.
- Ensure compatibility with init-based Linux systems

## How It Works:
- Uses Vosk for offline speech recognition.
- Listens for trigger words like "open terminal" or "launch terminal".
- Opens a terminal emulator based on available shells.
- Uses init-compatible commands (avoiding systemd).
- Supports multiple terminal emulators.
- Multiple language support - just add model and edit path...
