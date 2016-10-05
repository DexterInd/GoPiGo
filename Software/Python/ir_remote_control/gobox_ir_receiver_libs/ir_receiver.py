import socket
import sys
import time
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        
        try:
            # print 'connection from', client_address
            while True:
                data = connection.recv(16)
                if data:
                    # print data
                    last_recv_or_code=data
                else:
                    break
        except:
			last_recv_or_code=-1
        finally:
            connection.close()

th = threading.Thread(target=run_server)
th.daemon = True
th.start()

def nextcode():
    global last_recv_or_code
    send_back=last_recv_or_code
    last_recv_or_code=""
    return send_back
