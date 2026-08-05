import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",2053))

print("Listening on UDP 53...")

while True:
	data, addr = sock.recvfrom(512)
	print(f"Got {len(data)} bytes from {addr}")

	sock.sendto(data, addr)
	print("Sent response back")
