import logging
import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Args:
    tracker_ip: str
    tracker_port: int
    id: str
    peer_id: str
    msg: str | None


@dataclass
class Ctx:
    sock: socket.socket
    tracker_inet: Tuple[str, int]
    id: str
    peer_id: str
    peer_inet: Tuple[str, int] | None
    leave: bool
    punch_thread: threading.Thread | None
    msg: str | None


def address(ip: str, port: int):
    return (ip, port)


def inet(address: str):
    ip, port = address.split(":")
    return (ip, int(port))


def signal_punch_msg(ctx: Ctx):
    assert ctx.peer_inet is not None

    for _ in range(5):
        ctx.sock.sendto(b"PUNCH", ctx.peer_inet)
        logging.info(f"punched {ctx.peer_id}{ctx.peer_inet}")
        time.sleep(0.5)

    if ctx.msg is not None:
        ctx.sock.sendto(f"MSG {ctx.msg}".encode(), ctx.peer_inet)


def handle_peer(ctx: Ctx, message: str):
    peer_id, peer_address = message.split()[1:3]
    logging.info(f"{peer_id}({peer_address}) is acked")

    peer_inet = inet(peer_address)
    ctx.peer_inet = peer_inet

    ctx.punch_thread = threading.Thread(
        target=signal_punch_msg, args=(ctx,), daemon=True
    )

    ctx.punch_thread.start()


def signal_share(ctx: Ctx):
    ctx.sock.sendto(f"SHARE {ctx.id}".encode(), ctx.tracker_inet)
    logging.info(f"sent SHARE to {ctx.tracker_inet}")


def signal_peer(ctx: Ctx):
    ctx.sock.sendto(f"PEER {ctx.id} {ctx.peer_id}".encode(), ctx.tracker_inet)
    logging.info(f"sent PEER to {ctx.tracker_inet}")


def signal_leave(ctx: Ctx):
    ctx.sock.sendto(f"LEAVE {ctx.id}".encode(), ctx.tracker_inet)
    logging.info(f"sent LEAVE to {ctx.tracker_inet}")


def handle_punch(ctx: Ctx, addr):
    logging.info(f"PUNCH from {addr}")


def handle_msg(ctx: Ctx, addr, message: str):
    msg = message[4:]
    logging.info(f"MSG from {addr}: {msg}")

    # exit on first message
    ctx.leave = True
    signal_leave(ctx)


def main(args: Args):
    logging.debug(f"{args}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))  # OS chooses port

    ctx = Ctx(
        sock=sock,
        tracker_inet=(args.tracker_ip, args.tracker_port),
        id=args.id,
        peer_id=args.peer_id,
        peer_inet=None,
        leave=False,
        punch_thread=None,
        msg=args.msg,
    )

    signal_share(ctx)

    time.sleep(2)

    if ctx.msg is not None:
        signal_peer(ctx)

    while not ctx.leave:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        if message.startswith("PEER"):
            handle_peer(ctx, message)
        elif message.startswith("PUNCH"):
            handle_punch(ctx, addr)
        elif message.startswith("MSG"):
            handle_msg(ctx, addr, message)
        else:
            logging.error(f"unhandled method {message.split()[0]}")

    if ctx.punch_thread is not None:
        ctx.punch_thread.join()
        ctx.punch_thread = None


def parse_args():
    tracker_ip, port = sys.argv[1].split(":")
    port = int(port)

    if len(sys.argv) == 5:
        msg = sys.argv[4]
    else:
        msg = None

    return Args(
        tracker_ip=tracker_ip,
        tracker_port=port,
        id=sys.argv[2],
        peer_id=sys.argv[3],
        msg=msg,
    )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG
    )

    args = parse_args()

    main(args)
