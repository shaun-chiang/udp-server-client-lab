import socket
import sys
import hashlib
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 5555)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
received_data = []
m = hashlib.md5()


def verify_incoming_data(data):
    data_list = data.split(",", 2)
    m.update(data_list[0] + "," + data_list[1] + ",")
    if not data_list[2] == m.digest()[:4]:
        print('WARNING: #{0} segment is corrupted'.format(data_list[0]))


def verify_received_data_order(received_data):
    segment_number = 0
    sorted(received_data, key=lambda x: x.split(",")[0])
    for data in received_data:
        if segment_number != int(data.split(",")[0]):
            print("WARNING: ERROR AT {0}".format(data))
        segment_number += len(data)


while True:
    data, address = sock.recvfrom(4096)
    if data == "END":
        break
    received_data.append(data)
    verify_incoming_data(data)

    print >> sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >> sys.stderr, data

verify_received_data_order(received_data)
