# Voice Terminal Opener
# Author: Marcia Wilbur
# Description: A voice-activated tool for Linux using Vosk for speech recognition and pyttsx3 for voice output.
# This script allows users to open a terminal, purge systemd, open Firefox to a spoken website, toggle voice feedback, and exit the application via voice commands.

import os
import subprocess
import queue
import sounddevice as sd
import vosk
import json
import threading
import pyttsx3

# Initialize TTS engine globally
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Select the first available voice (change if needed)
engine.setProperty("rate", 150)  # Adjust speed (default ~200)

# Global flag to enable or disable voice output
enable_voice = True  # Set to False to disable voice output

def toggle_voice():
    """Toggles voice output on or off."""
    global enable_voice
    enable_voice = not enable_voice
    status = "enabled" if enable_voice else "disabled"
    print(f"Voice output {status}.")
    speak(f"Voice output {status}.")

def speak(text):
    """Uses text-to-speech to confirm actions if enabled."""
    if enable_voice:
        engine.say(text)
        engine.runAndWait()

def open_terminal():
    """Function to open a terminal based on available shells."""
    shells = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "lxterminal", "mate-terminal", "terminator"]
    for shell in shells:
        if subprocess.call(["which", shell], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.Popen([shell], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(f"Opened {shell}")
            speak("Terminal opened.")
            return
    print("No supported terminal emulator found.")
    speak("No supported terminal emulator found.")

def purge_systemd():
    """Prompts user before attempting to purge systemd."""
    confirm = input("Are you sure you want to purge systemd? This may break your system! (y/N): ")
    if confirm.lower() == "y":
        print("Purging systemd...")
        speak("Purging systemd. Please wait.")
        subprocess.run(["sudo", "apt-get", "purge", "--auto-remove", "systemd"], stderr=subprocess.DEVNULL)
        speak("Systemd purge completed.")
    else:
        print("Systemd purge canceled.")
        speak("Systemd purge canceled.")

def format_website(website):
    """Formats spoken website names correctly, ensuring proper domain formatting."""
    website = website.strip().lower()
    words = website.split()

    # Replace 'dot' with '.' if mistakenly transcribed
    formatted_words = []
    for i, word in enumerate(words):
        if word == "dot":
            formatted_words.append(".")
        elif i > 0 and words[i - 1] not in ["dot", "."] and word in ["com", "org", "net", "edu", "gov", "io"]:
            formatted_words.append("." + word)  # Ensure correct domain formatting
        else:
            formatted_words.append(word)

    website = "".join(formatted_words)

    # Ensure a default domain if none is found
    if not any(website.endswith(ext) for ext in [".com", ".org", ".net", ".edu", ".gov", ".io"]):
        website += ".com"

    return website

def open_firefox(website):
    """Opens Firefox and navigates to the specified website."""
    website = format_website(website)
    if not website.startswith("http"):
        website = "https://" + website
    print(f"Opening Firefox to {website}...")
    speak(f"Opening Firefox to {website}.")
    subprocess.Popen(["firefox", website], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def stop_application():
    """Stops the application gracefully."""
    global listening
    listening = False
    print("Shutting down voice command center...")
    speak("Shutting down voice command center.")
    stop_listening()
    os._exit(0)

def recognize_speech():
    """Recognizes speech and checks for command triggers."""
    model_path = os.path.expanduser("~/vosk_model/vosk-model-small-en-us-0.15")
    if not os.path.exists(model_path):
        print("Error: Vosk model not found. Please check the path.")
        speak("Error. Vosk model not found.")
        return

    try:
        model = vosk.Model(model_path)
    except Exception as e:
        print(f"Error loading Vosk model: {e}")
        speak("Error loading Vosk model.")
        return

    q = queue.Queue()

    def callback(indata, frames, time, status):
        try:
            if status:
                print(status)
            q.put(bytes(indata))
        except Exception as e:
            print(f"Callback error: {e}")

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
            recognizer = vosk.KaldiRecognizer(model, 16000)
            print("Listening...")
            speak("Listening.")

            global listening
            listening = True
            while listening:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    command = result.get("text", "").lower()
                    print(f"Recognized: {command}")

                    if "open terminal" in command or "launch terminal" in command:
                        open_terminal()
                    elif "purge systemd" in command:
                        purge_systemd()
                    elif "open firefox to" in command:
                        words = command.split("to")
                        if len(words) > 1:
                            website = words[1].strip()
                            open_firefox(website)
                    elif "toggle voice" in command:
                        toggle_voice()
                    elif "exit" in command or "quit" in command or "shutdown" in command:
                        stop_application()
                        break
    except OSError as e:
        print(f"Error: {e}. Ensure your microphone is accessible and working.")
        speak("Error. Please check the microphone.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("Unexpected error occurred.")

def start_listening():
    global listening
    listening = True
    threading.Thread(target=recognize_speech, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    print("Stopped listening.")
    speak("Stopped listening.")

if __name__ == "__main__":
    print("Voice Command Center - Command Line Version")
    speak("Voice Command Center activated.")
    start_listening()
    while listening:
        pass
