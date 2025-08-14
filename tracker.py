from dataclasses import dataclass
import socket
import sys
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


def signal_peer(ctx: Ctx, id: str, peer_id: str):
    peer_s_addr = ctx.peers[id]
    peer_r_addr = ctx.peers[peer_id]

    peer_s_address = address(*peer_s_addr)
    peer_r_address = address(*peer_r_addr)

    ctx.sock.sendto(f"PEER {peer_id} {peer_r_address}".encode(), peer_s_addr)
    logging.info(
        f"peer{{{id}{peer_s_addr}}} is peered with receiver {peer_id}{peer_r_addr}"
    )

    ctx.sock.sendto(f"PEER {id} {peer_s_address}".encode(), peer_r_addr)
    logging.info(
        f"peer{{{peer_id}{peer_r_addr}}} is peered with sender {id}{peer_s_addr}"
    )


def handle_share(ctx: Ctx, addr, message):
    id = message.split()[1]

    ctx.peers[id] = addr
    logging.info(f"peer{{{id}}} registered from {addr}")


def handle_peer(ctx: Ctx, message):
    id, peer_id = message.split()[1:3]
    logging.info(f"peer{{{id}}} requested peer{{{peer_id}}}")

    if peer_id in ctx.peers:
        signal_peer(ctx, id, peer_id)


def handle_leave(ctx: Ctx, message):
    id = message.split()[1]

    if id in ctx.peers:
        peer_addr = ctx.peers[id]
        del ctx.peers[id]
        logging.info(f"peer{{{id}{peer_addr}}} deleted")
    else:
        logging.warning(f"peer{{{id}}} does not exist")


def handle(ctx: Ctx):
    while True:
        data, addr = ctx.sock.recvfrom(1024)
        message = data.decode()

        if message.startswith("SHARE"):
            handle_share(ctx, addr, message)
        elif message.startswith("PEER"):
            handle_peer(ctx, message)
        elif message.startswith("LEAVE"):
            handle_leave(ctx, message)
        else:
            logging.error(f"unhandled method {message.split()[0]}")


def main(args: Args):
    logging.debug(f"{args}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ctx = Ctx(
        sock=sock,
        peers={},
    )

    sock.bind(("0.0.0.0", args.port))
    logging.info(f"tracker running on port {args.port}")

    threading.Thread(target=handle, args=(ctx,), daemon=True).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


def parse_args():
    port = int(sys.argv[1])

    return Args(
        port=port,
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
    )

    args = parse_args()

    main(args)
