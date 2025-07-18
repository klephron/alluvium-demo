import socket
import threading
import time

TRACKER_ADDR = ("<TRACKER_IP>", 9999)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 0))  # OS chooses port


def listen():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"Received from {addr}: {data.decode()}")
        except:
            break


sock.sendto(b"REGISTER sender", TRACKER_ADDR)

peer_ip = None
peer_port = None
while peer_ip is None:
    data, addr = sock.recvfrom(1024)
    parts = data.decode().split()
    if len(parts) == 2:
        peer_ip, peer_port = parts[0], int(parts[1])
        print(f"Peer (receiver) info: {peer_ip}:{peer_port}")

threading.Thread(target=listen, daemon=True).start()

# Send punching packets to peer
for _ in range(5):
    sock.sendto(b"hole punch", (peer_ip, peer_port))
    time.sleep(0.5)

# Send actual message
sock.sendto(b"Hello from sender", (peer_ip, peer_port))

while True:
    time.sleep(1)
