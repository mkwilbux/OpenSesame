# OpenSaysMe
# Author: Marcia K Wilbur
# Date: 2/2025
# This is just the beginning!

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


## Requirements:
### Install dependencies:
#### MX specific

```bash
sudo apt install python3-pip portaudio19-dev
pip install sounddevice numpy
```
#### In general

``` bash
sudo apt install vosk-api sounddevice python3-pip
pip install sounddevice vosk
```

### Get model
#### Small - fast, less accurate ~50MB
mkdir -p ~/vosk_model
cd ~/vosk_model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip

#### Best accuracy model: 3.8 gb
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip

### Run script
Run the script, speak into the microphone, and say "open terminal" to launch the terminal.
