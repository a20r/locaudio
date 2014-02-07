
import locaudio
import sys
import socket

if __name__ == "__main__":
    if len(sys.argv) == 3:
        locaudio.run(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:
        ip_addr = socket.gethostbyname(socket.getfqdn())
        locaudio.run(ip_addr, 8000, sys.argv[1])
    else:
        raise Exception("Correct argument form not supplied")

