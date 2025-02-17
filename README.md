# OpenSeshell
name change due to existing opensesame project

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

============================================

#  openSesame - Installation & User Guide
## Author: Marcia Wilbur
### Installation
#### Step 1: Install Dependencies
Run the following command to install required packages:

```bash
sudo apt update && sudo apt install -y piper sounddevice vosk
pip install piper-tts
```
### Step 2: Download Vosk Speech Model
```bash
mkdir -p ~/vosk_model
cd ~/vosk_model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```
### Step 3: Verify Piper TTS 
For voice feedback and responses (toggle voice to disable/enable - enabled by default). Test if Piper is working by running:

```
python -c "import piper_tts; piper_tts.PiperVoice('en_US').speak('Installation complete!')"
```

If you hear the voice, it's installed correctly.

## How to Use openSesame
#### Run the Program
Start the Voice Terminal Opener by running:

```
python3 openSesame_x.x.x-x.py
```

## Available Voice Commands

### Command	Action

"open terminal"	Launches a terminal

"purge systemd"	Prompts to remove systemd

"open firefox to [site]"	Opens Firefox to the website

"toggle voice"	Enables/disables voice output

"exit"	Stops the program

### Example Commands

"open firefox to fsf org"

"toggle voice"

"exit"

Now you’re ready to control your Linux system using voice commands.

- Change language by changing model
- Add more features by projects implementing AI in their apps. Idea - fork or work with apps.

  # Todo
  - log control
  - add use cases
  - user experience - what do users/developers want.
 
    Example: Content creators might want to just convert jpg files to png. Command line simple.
    Example: Users might want to take screen capture in the background with scrot

Also: add and restore abandoned Software.
fuly customizale!

