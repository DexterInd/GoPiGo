import socket
import sys
import time
import threading

NO_PRESS = "NO_KEYPRESS"
last_recv_or_code = NO_PRESS
previous_keypress = NO_PRESS


def run_server():
    '''
    # This runs in a background thread and keeps on updating a global variable so that the only the latest value is returned when the scripts asks for data
    '''
    global last_recv_or_code

    # each loop handles one keypress at a time
    # so there's only going to be a new socket for each loop
    while True:
        try:
            connection, client_address = sock.accept() # accept a new client
            connection.setblocking(True) # set connection to blocking mode

        except socket.timeout:

            # if we encounter a timeout, then it means nothing is pressed at the given moment
            last_recv_or_code = NO_PRESS
            continue

        # read a maximum of 16 characters
        # since it's a blocking method
        # we can be sure we're getting a non-empty string
        last_recv_or_code = connection.recv(16)

        # on each loop, close the given socket
        connection.close()

    sys.exit(0)

def nextcode(consume=True):
    '''
    Returns the key that was last read by the background thread.
    If consume is set to True, this key will only be returned once.
    If consume is set to False, this key will be returned until changed
    '''
    global last_recv_or_code
    global previous_keypress

    send_back=last_recv_or_code

    # print("send_back: {} previous_keypress: {}".format(send_back,previous_keypress))

    if consume:
        if previous_keypress == send_back:
            return ""
        if send_back == NO_PRESS:
            # we're now getting a NO_PRESS, key has been released
            # send an empty string but remember state
            previous_keypress = send_back
            return ""

    previous_keypress = send_back

    return send_back


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse the port on future connections
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # enable naggle algorithm

# Bind the socket to the port
server_address = ('localhost', 21852)
print ('starting up on %s port %s' % server_address)
try:
    sock.bind(server_address)
except OSError:  # Address already in use so we're fine. Means the module has been imported twice
    print("Address already in use. Assuming it's another ir_receiver server and that all is fine.")
sock.listen(1)
sock.settimeout(0.5) # socket timeout

th = threading.Thread(target=run_server)
th.daemon = True
th.start()

