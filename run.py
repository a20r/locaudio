
import locaudio
import sys


if __name__ == "__main__":
    if len(sys.argv) == 4:
        locaudio.detectionserver.run(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:
        locaudio.detectionserver.run("localhost", 8000, sys.argv[1])
    else:
        raise Exception("Not enough arguments supplied")

