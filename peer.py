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
            logging.info(f"received from {addr}: {data.decode()}")
        except:
            break


def handle_shared(sock: socket.socket, message: str):
    logging.info(f"peer is signalled shared")


def signal_share(args: Args, sock: socket.socket):
    tracker = address(args.tracker_ip, args.tracker_port)
    sock.sendto(f"SHARE {args.id}".encode(), tracker)
    logging.info(f"peer {args.id} sent SHARE to {tracker}")


def signal_leave(args: Args, sock: socket.socket):
    tracker = address(args.tracker_ip, args.tracker_port)
    sock.sendto(f"LEAVE {args.id}".encode(), tracker)
    logging.info(f"peer {args.id} sent LEAVE to {tracker}")


def main(args: Args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))  # OS chooses port

    signal_share(args, sock)

    while True:
        data, _ = sock.recvfrom(1024)
        message = data.decode()

        if message.startswith("SHARED"):
            handle_shared(sock, message)
            signal_leave(args, sock)
            break
        else:
            logging.error(f"unhandled method {message.split()[0]}")

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
