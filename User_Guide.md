# Voice Command Center - User Guide

## Introduction
The **Voice Command Center** allows you to control your Linux system using voice commands. It uses **Vosk** for speech recognition and **Piper TTS** for voice responses.

## Installation
### 1. Install Required Dependencies
Run the following command:
```bash
sudo apt update && sudo apt install -y piper sounddevice vosk firefox gimp
pip install piper-tts
```

### 2. Download Vosk Speech Model
```bash
mkdir -p ~/vosk_model
cd ~/vosk_model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### 3. Verify Piper TTS
Run:
```bash
python -c "import piper_tts; piper_tts.PiperVoice('en_US').speak('Installation complete!')"
```
If you hear the voice, it's installed correctly.

## Running the Program
To start the Voice Command Center, run:
```bash
python voice_terminal.py
```

## Available Voice Commands

| **Command**                     | **Action**                                    |
|----------------------------------|----------------------------------------------|
| "open terminal"                 | Launches a terminal                          |
| "open gnu image manipulator"    | Opens GIMP                                   |
| "open firefox to [website]"      | Opens Firefox to the specified website       |
| "toggle voice"                   | Enables/disables voice output               |
| "exit" / "quit" / "shutdown"    | Stops the program                           |

## Example Commands
- **"open terminal"** → Launches terminal
- **"open gnu image manipulator"** → Opens GIMP
- **"open firefox to fsf.org"** → Opens Firefox to fsf.org
- **"toggle voice"** → Enables/disables voice feedback

Now you're ready to control Linux with your voice! 🎙️🚀
