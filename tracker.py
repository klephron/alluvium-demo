import socket
import threading

clients = {}


def handle_client(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        if message.startswith("REGISTER"):
            role = message.split()[1]
            clients[role] = addr
            print(f"{role} registered from {addr}")
            if "sender" in clients and "receiver" in clients:
                # Send peer info to both
                sender_addr = f"{clients['receiver'][0]} {clients['receiver'][1]}"
                receiver_addr = f"{clients['sender'][0]} {clients['sender'][1]}"
                sock.sendto(sender_addr.encode(), clients["sender"])
                sock.sendto(receiver_addr.encode(), clients["receiver"])


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9999))
print("Tracker running on port 9999")
threading.Thread(target=handle_client, args=(sock,), daemon=True).start()

try:
    while True:
        pass
except KeyboardInterrupt:
    pass
