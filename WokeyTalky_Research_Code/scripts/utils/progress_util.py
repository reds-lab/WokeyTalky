import time
import sys

def progress_bar(duration):
    for i in range(duration):
        time.sleep(1)
        progress = (i + 1) / duration
        bar_length = 20
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        percent = int(progress * 100)
        sys.stdout.write(f'\rWaiting... [{bar}] {percent}%')
        sys.stdout.flush()
    sys.stdout.write('\n')