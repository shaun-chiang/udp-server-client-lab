import socket
import sys
import time
import hashlib

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('10.0.0.2', 5555)

# Input bit per second here
bit_per_second = 1600000.0
byte_per_second = bit_per_second / 8.0
segment_number = 0
message = str(segment_number) + "," + 'This is the message.  It will be repeated,'

while (segment_number <= (byte_per_second + len(message))):
    message = str(segment_number) + "," + 'This is the message.  It will be repeated,'
    m = hashlib.md5()
    m.update(message)
    message += m.digest()[:4]
    # Send data
    #print >> sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)
    segment_number += len(message)
    time.sleep((len(message)+27) / byte_per_second)


print >> sys.stderr, 'sending "%s"' % "END"
sent = sock.sendto("END", server_address)
print >> sys.stderr, 'closing socket'
sock.close()
