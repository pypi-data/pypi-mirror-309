import time
import threading
from .core import generate_joke

def start_joke_stream(interval=5, duration=30):
    """Start a stream of jokes at a specified interval and duration."""
    def joke_stream():
        end_time = time.time() + duration
        while time.time() < end_time:
            print("Joke Stream:", generate_joke())
            time.sleep(interval)
    
    # Запуск потока для чисел
    thread = threading.Thread(target=joke_stream)
    thread.start()
