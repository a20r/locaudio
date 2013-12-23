
import threading

def run_thread(func):
    """

    Truly awesome function decorator. Truly. Fucking. Awesome.

    """

    thread = threading.Thread(target=func)
    thread.setDaemon(True)
    thread.start()


def on_import(func):
    func()

