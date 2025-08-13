import logging
import socket
import sys
import threading
import time
from dataclasses import dataclass


@dataclass
class Args:
    tracker_ip: str
    tracker_port: int
    id: str


def address(addr: str, port: int):
    return (addr, port)


def listen(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            logging.info(f"Received from {addr}: {data.decode()}")
        except:
            break


def handle_shared(sock: socket.socket, msg: str):
    method, peer_addr = msg.split()[0:2]
    logging.info(f"Peer is signalled {method} with addr {peer_addr}")


def main(args: Args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))  # OS chooses port

    tracker = address(args.tracker_ip, args.tracker_port)
    sock.sendto(f"SHARE {args.id}".encode(), tracker)
    logging.info(f"peer {args.id} sent SHARE to {tracker}")

    # signalled shared
    data, _ = sock.recvfrom(1024)
    msg = data.decode()
    method = msg.split()[0]

    if method == "SHARED":
        handle_shared(sock, msg)

    # threading.Thread(target=listen, daemon=True, args=(sock,)).start()

    # # Send punching packets to peer
    # for _ in range(5):
    #     sock.sendto(b"hole punch", (peer_ip, peer_port))
    #     time.sleep(0.5)

    # # Send actual message
    # sock.sendto(b"Hello from sender", (peer_ip, peer_port))

    # while True:
    #     time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
    )

    args = Args(
        tracker_ip="localhost",
        tracker_port=14100,
        id=sys.argv[1],
    )

    main(args)
