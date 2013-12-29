
import threading

def run_thread(func):
    """

    Truly awesome function decorator. Truly. Fucking. Awesome.

    """

    thread = threading.Thread(target=func)
    thread.setDaemon(True)
    thread.start()


already_imported = list()
def on_import(func):
    global already_imported
    name = func.__name__ + " " + func.__module__
    if not name in already_imported:
        already_imported.append(name)
        func()

