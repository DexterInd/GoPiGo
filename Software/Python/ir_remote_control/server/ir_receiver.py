import socket
import sys
import time
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse the port on future connections
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # enable naggle algorithm

# Bind the socket to the port
server_address = ('localhost', 21852)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

last_recv_or_code=""

# This runs in a background thread and keeps on updating a global variable so that the only the latest value is returned when the scripts asks for data
def run_server():
    global last_recv_or_code
    while True:
        # Wait for a connection
        # print 'waiting for a connection'
        connection, client_address = sock.accept()
        connection.setblocking(False)

        while True:
            try:
                msg = connection.recv(16)
                if len(msg) > 0:
                    last_recv_or_code = msg
                else:
                    last_recv_or_code = "NO_PRESS"
                    break
            except:
                continue

            time.sleep(0.6)

        connection.close()


th = threading.Thread(target=run_server)
th.daemon = True
th.start()

def nextcode():
    global last_recv_or_code
    send_back=last_recv_or_code
    last_recv_or_code=""
    return send_back
