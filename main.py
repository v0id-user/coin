from sys import argv
from server import startServer
from client import mine_and_submit, startClient


def print_usage():
    """Print usage information."""
    print("Usage:")
    print("  python main.py server           - Start the blockchain server")
    print("  python main.py client [data]    - Mine and submit a block")
    print("")
    print("Examples:")
    print("  python main.py server")
    print("  python main.py client \"My transaction data\"")
    print("  python main.py client           # Uses default data")


def main():
    """Main entry point for the blockchain application."""
    if len(argv) < 2:
        print("Error: Missing mode argument\n")
        print_usage()
        return
    
    mode = argv[1].lower()
    
    if mode == "server":
        startServer()
    elif mode == "client":
        startClient()
    
    else:
        print(f"Error: Unknown mode '{mode}'\n")
        print_usage()


if __name__ == "__main__":
    main()
