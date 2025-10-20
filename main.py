from sys import argv
from server import startServer
def main():
    isServer = argv[1] == "server"

    if isServer:
        startServer()

if __name__ == "__main__":
    main()
