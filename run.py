
import locaudio
import sys


if __name__ == "__main__":
    if len(sys.argv) == 3:
        locaudio.config.run(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 0:
        locaudio.config.run("localhost", 8000)
    else:
        raise Exception("Correct argument form not supplied")

