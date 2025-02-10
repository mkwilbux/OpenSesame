import os
import subprocess
import queue
import sounddevice as sd
import vosk
import json

def open_terminal():
    """Function to open a terminal based on available shells."""
    shells = ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "lxterminal", "mate-terminal", "terminator"]
    for shell in shells:
        if subprocess.call(["which", shell], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.Popen([shell], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)  # Suppress KDE warnings
            print(f"Opened {shell}")
            return
    print("No supported terminal emulator found.")

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
                print(status, flush=True)
            q.put(bytes(indata))  # Ensure proper byte conversion
        except Exception as e:
            print(f"Callback error: {e}")

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            recognizer = vosk.KaldiRecognizer(model, 16000)
            print("Listening...")

            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    command = result.get("text", "").lower()
                    print("Recognized:", command)

                    if "open terminal" in command or "launch terminal" in command:
                        open_terminal()
                        break
                    elif "exit" in command:
                        print("Exiting...")
                        break
    except OSError as e:
        print(f"Error: {e}. Ensure your microphone is accessible and working.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    recognize_speech()
