import socket
import threading
import time

TRACKER_ADDR = ("<TRACKER_IP>", 9999)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 0))  # OS chooses port
local_port = sock.getsockname()[1]


def listen():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"Received from {addr}: {data.decode()}")
        except:
            break


sock.sendto(b"REGISTER receiver", TRACKER_ADDR)

threading.Thread(target=listen, daemon=True).start()

# Wait for peer info and send initial punching packets
peer_ip = None
peer_port = None
while peer_ip is None:
    data, addr = sock.recvfrom(1024)
    parts = data.decode().split()
    if len(parts) == 2:
        peer_ip, peer_port = parts[0], int(parts[1])
        print(f"Peer (sender) info: {peer_ip}:{peer_port}")
        for _ in range(5):  # Punching packets
            sock.sendto(b"hole punch", (peer_ip, peer_port))
            time.sleep(0.5)

while True:
    time.sleep(1)
