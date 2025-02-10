import os
import subprocess
import queue
import sounddevice as sd
import vosk
import json
import threading

def open_terminal():
    """Function to open a terminal based on available shells."""
    shells = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "lxterminal", "mate-terminal", "terminator"]
    for shell in shells:
        if subprocess.call(["which", shell], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.Popen([shell], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)  # Suppress KDE warnings
            print(f"Opened {shell}")
            return
    print("No supported terminal emulator found.")

def purge_systemd():
    """Prompts user before attempting to purge systemd."""
    confirm = input("Are you sure you want to purge systemd? This may break your system! (y/N): ")
    if confirm.lower() == "y":
        print("Purging systemd...")
        subprocess.run(["sudo", "apt-get", "purge", "--auto-remove", "systemd"], stderr=subprocess.DEVNULL)  # Waits for password input
    else:
        print("Systemd purge canceled.")

def open_firefox(website):
    """Opens Firefox and navigates to the specified website."""
    if not website.startswith("http"):
        website = "https://" + website
    print(f"Opening Firefox to {website}...")
    subprocess.Popen(["firefox", website], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def format_website(website):
    """Formats spoken website names correctly, preventing unwanted dots."""
    website = website.strip().lower()
    words = website.split()

    # If the user spells out a website (e.g., "f s f o r g"), join without dots
    if all(len(word) == 1 for word in words):
        website = "".join(words)
    elif len(words) > 1 and words[-1] in ["com", "org", "net", "edu", "gov", "io"]:
        website = "".join(words[:-1]) + "." + words[-1]  # Convert "fsf org" to "fsf.org"
    elif not any(ext in website for ext in [".com", ".org", ".net", ".edu", ".gov", ".io"]):
        website += ".com"  # Default to .com if no domain is found

    return website

def recognize_speech():
    """Recognizes speech and checks for command trigger."""
    model_path = os.path.expanduser("~/vosk_model/vosk-model-small-en-us-0.15")
    if not os.path.exists(model_path):
        print("Error: Vosk model not found. Please check the path.")
        return

    try:
        model = vosk.Model(model_path)
    except Exception as e:
        print(f"Error loading Vosk model: {e}")
        return

    q = queue.Queue()

    def callback(indata, frames, time, status):
        try:
            if status:
                print(status)
            q.put(bytes(indata))  # Ensure proper byte conversion
        except Exception as e:
            print(f"Callback error: {e}")

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            recognizer = vosk.KaldiRecognizer(model, 16000)
            print("Listening...")

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
                    elif "purge systemd" in command or "system day" in command or "system d" in command:
                        purge_systemd()
                    elif "open firefox to" in command:
                        words = command.split("to")
                        if len(words) > 1:
                            website = format_website(words[1].strip())
                            open_firefox(website)
                    elif "exit" in command:
                        print("Exiting...")
                        stop_listening()
                        break
    except OSError as e:
        print(f"Error: {e}. Ensure your microphone is accessible and working.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def start_listening():
    global listening
    listening = True
    threading.Thread(target=recognize_speech, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    print("Stopped listening.")

if __name__ == "__main__":
    print("Voice Command Center - Command Line Version")
    print("Say 'open terminal' to launch a terminal, 'purge systemd' to remove systemd, 'open firefox to [website]' to open a website, or 'exit' to stop listening.")
    start_listening()
    while listening:
        pass
