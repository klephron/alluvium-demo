import socket
import threading

import logging

PORT = 14100

# [id] = addr
CLIENTS = {}


def signal_peers(sock):
    peer1_addr = CLIENTS["peer1"]
    peer2_addr = CLIENTS["peer2"]
    # sender_addr = f"{CLIENTS['receiver'][0]} {CLIENTS['receiver'][1]}"
    # receiver_addr = f"{CLIENTS['sender'][0]} {CLIENTS['sender'][1]}"
    sock.sendto(peer1_addr.encode(), f"REGISTERED {peer2_addr}")
    sock.sendto(peer2_addr.encode(), f"REGISTERED {peer1_addr}")


def handle_client(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        if message.startswith("REGISTER"):
            id = message.split()[1]

            CLIENTS[id] = addr
            logging.info(f"{id} registered from {addr}")

            if "peer1" in CLIENTS and "peer2" in CLIENTS:
                signal_peers(sock)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("0.0.0.0", PORT))
    logging.info(f"Tracker running on port {PORT}")

    threading.Thread(target=handle_client, args=(sock,), daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
)

if __name__ == "__main__":
    main()
