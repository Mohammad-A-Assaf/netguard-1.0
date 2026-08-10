import socket
import struct # pack numbers into bytes. DNS header need 2-bytes in gif enain format


def parse_domain(data , offset=12):
	"""
		Parse domain name from
		DNS query starting
		at offset.
	"""

	labels = [] # empty list to collect parts
	while True: # keep going until we hit 0 in length
		length = data[offset] # read 1 byte: how long is next label?
		if length == 0: # If 0, we're done.
			offset += 1
			break
		offset += 1 # Move past the length Byte.
		label = data[offset:offset + length].decode('ascii') # read the label and covert it to text
		labels.append(label) # save it in the empty list 
		offset += length # move past this label
	return '.'.join(labels), offset + 1 # join with dots, return poistion after 0


def build_response(data): 
	#copy transaction ID from query (bytes 0-1)
	tid = data[:2]

	#Flags: QR = 1 (response), AA = 1 (authoritative), RCODE = 0 (no error)
	#0x8180 in hex = 1000000110000000 in binary
	flags = b'\x81\x80'

	# Counts: QDCOUNT=1, ANCOUNT=0, NSCOUNT=0,ARCOUNT=0
	# '>HHHH' means 4 unsigned 16-bit integers,big endian
	counts = struct.pack('>HHHH',1,0,0,0)
	header = tid + flags + counts
	_, offset = parse_domain(data)
	offset += 4
	question = data[12:offset]
	return header + question


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket.socket() creates a new network socket, AF_INET Address family:IPV4, SOCK_DGRAM Sockettype: datagram(UDP)
sock.bind(("0.0.0.0",2053))

print("Listening on UDP 2053...")

while True:
	data, addr = sock.recvfrom(512) #wait for UDP packet	
	domain, _ = parse_domain(data) #extract the domain name
	print(f"Query for : {domain}")

	#Forward to ISP DNS Server

	upstream = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	upstream.settimeout(5)

	try:
		upstream.sendto(data, ("192.168.10.1", 53))
		response,_ = upstream.recvfrom(512)
		sock.sendto(response, addr)
		print("FOrwarded to ISP")
	except socket.timeout:
		print("Upstream timeout, no response")
		
		response = build_response(data)
		sock.sendto(response,addr)
