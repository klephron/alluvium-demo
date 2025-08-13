import socket
import threading

import logging

PORT = 14100

# [id] = addr
CLIENTS = {}


def address(addr: str, port: int):
    return f"{addr}:{port}"


def signal_shared(sock: socket.socket):
    peer1_addr = CLIENTS["peer1"]
    peer2_addr = CLIENTS["peer2"]

    peer1_address = address(*peer1_addr)
    peer2_address = address(*peer2_addr)

    sock.sendto(f"SHARED {peer2_address}".encode(), peer1_addr)
    logging.info(f"peer peer1{peer1_addr} is signalled shared")

    sock.sendto(f"SHARED {peer1_address}".encode(), peer2_addr)
    logging.info(f"peer peer2{peer2_addr} is signalled shared")


def handle_share(addr, message):
    id = message.split()[1]

    CLIENTS[id] = addr
    logging.info(f"{id} registered from {addr}")


def handle(sock: socket.socket):
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        if message.startswith("SHARE"):
            handle_share(addr, message)

        if "peer1" in CLIENTS and "peer2" in CLIENTS:
            signal_shared(sock)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(("0.0.0.0", PORT))
    logging.info(f"Tracker running on port {PORT}")

    threading.Thread(target=handle, args=(sock,), daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
    )

    main()
