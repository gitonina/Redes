#!/usr/bin/python3
# Echo client program

import jsockets
import sys, threading

def Rdr(s, total_bytes):
    received_bytes = 0
    while received_bytes < total_bytes:
        try:
            data = s.recv(buffer_size)
        except:
            data = None
        if not data: 
            break
        sys.stdout.buffer.write(data)
        received_bytes += len(data)

if len(sys.argv) != 4:
    print('Use: ' + sys.argv[0] + ' size host port')
    sys.exit(1)

buffer_size = int(sys.argv[1])
s = jsockets.socket_tcp_connect(sys.argv[2], sys.argv[3])
if s is None:
    print('could not open socket')
    sys.exit(1)

total_bytes = 0
for line in sys.stdin.buffer:
    total_bytes += len(line)

sys.stdin.seek(0) 


newthread = threading.Thread(target=Rdr, args=(s, total_bytes))
newthread.start()

sent_bytes = 0
while sent_bytes < total_bytes:
    chunk = sys.stdin.buffer.read(buffer_size)
    if not chunk:
        break
    s.send(chunk)
    sent_bytes += len(chunk)


newthread.join()  
s.close()