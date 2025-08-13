from dataclasses import dataclass
import socket
import threading

import logging
from typing import Tuple


@dataclass
class Args:
    port: int


@dataclass
class Ctx:
    sock: socket.socket
    peers: dict[str, Tuple[str, int]]


def address(addr: str, port: int):
    return f"{addr}:{port}"


def signal_shared(ctx: Ctx):
    peer1_addr = ctx.peers["peer1"]
    peer2_addr = ctx.peers["peer2"]

    peer1_address = address(*peer1_addr)
    peer2_address = address(*peer2_addr)

    ctx.sock.sendto(f"SHARED peer2 {peer2_address}".encode(), peer1_addr)
    logging.info(f"peer peer1{peer1_addr} is signalled shared")

    ctx.sock.sendto(f"SHARED peer1 {peer1_address}".encode(), peer2_addr)
    logging.info(f"peer peer2{peer2_addr} is signalled shared")


def handle_share(ctx: Ctx, addr, message):
    id = message.split()[1]

    ctx.peers[id] = addr
    logging.info(f"{id} registered from {addr}")

    if "peer1" in ctx.peers and "peer2" in ctx.peers:
        signal_shared(ctx)


def handle_leave(ctx: Ctx, message):
    id = message.split()[1]

    if id in ctx.peers:
        peer_addr = ctx.peers[id]
        logging.info(f"peer {id}{peer_addr} deleted")
        del ctx.peers[id]
    else:
        logging.warning(f"peer {id} does not exist")


def handle(ctx: Ctx):
    while True:
        data, addr = ctx.sock.recvfrom(1024)
        message = data.decode()

        if message.startswith("SHARE"):
            handle_share(ctx, addr, message)
        elif message.startswith("LEAVE"):
            handle_leave(ctx, message)
        else:
            logging.error(f"unhandled method {message.split()[0]}")


def main(args: Args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ctx = Ctx(
        sock=sock,
        peers={},
    )

    sock.bind(("0.0.0.0", args.port))
    logging.info(f"Tracker running on port {args.port}")

    threading.Thread(target=handle, args=(ctx,), daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
    )

    args = Args(
        port=14100,
    )

    main(args)
