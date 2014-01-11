
import threading
import uuid

def run_thread(func):
    """

    Truly awesome function decorator. Truly. Freaking. Awesome.

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


def getUUID():
    return str(uuid.uuid4())


def try_get(collection, key):
    try:
        return collection[key]
    except KeyError:
        return list()

