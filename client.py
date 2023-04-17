import logging
import socket
import threading
import time
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
server = socket.socket()
list_of_clients = []
client_name = "Client1"
client_channel_port = 9994

def ping():
    # Set up AES encryption key and IV
    key = b'0123456789abcdef'
    iv = b'fedcba9876543210'

    message = client_name + ": PING"

    while True:

        fetch_ip_adresses()
        time.sleep(5)
        try:
            for client in list_of_clients:
                if client['ip_address'] != '' and not (client_name) in client['name']:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.connect((client['ip_address'], client_channel_port))

                    # Encrypt the message using GCM
                    cipher = AES.new(key, AES.MODE_GCM, iv)
                    encrypted_message, tag = cipher.encrypt_and_digest(message.encode())

                    sock.sendall(encrypted_message)
                    print((message))

                    # Receive the encrypted response from the client and decrypt it using GCM
                    data = sock.recv(1024)
                    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
                    decrypted_message = cipher.decrypt(data)
                    print(decrypted_message.decode())
        except Exception as e:
            logger.error(e)

        finally:
            time.sleep(10)

def pong():
    # Set up AES-GCM encryption key and nonce
    key = b'0123456789abcdef'
    iv = b'fedcba9876543210'

    message = client_name + ": PONG"

    while True:
        # try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', client_channel_port))
            sock.listen(15)

            (client_socket, client_address) = sock.accept()
            data = client_socket.recv(2048)

            if data:
                # Decrypt the received message using AES-GCM
                cipher = AES.new(key, AES.MODE_GCM,iv)
                decrypted_message = cipher.decrypt(data)
                print(decrypted_message.decode())

                # Encrypt the response message using AES-GCM and send it back to the client
                cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
                # cipher.update(client_name.encode())
                encrypted_message, tag = cipher.encrypt_and_digest(message.encode())
                client_socket.sendall(encrypted_message)
                print(message)

                # print(unpad(message, 16).decode())
            else:
                print("no data")

        # except socket.error as e:
        #     logger.error("Socket error:", e)
        #
        # finally:
            time.sleep(2)

def connect_to_server(client_name = "Client1"):
    logger.info("Connection to Server.py Thread")
    host = 'localhost'
    port2 = 9995
    global sock_ssl
    sock_ssl= ssl.wrap_socket(server, cert_reqs=ssl.CERT_REQUIRED, ca_certs='server.crt')
    sock_ssl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_ssl.connect((host, port2))
    print(f"Registered with name: {client_name}")
    while True:
        sock_ssl.sendall(pad(str.encode(client_name), 16))
        time.sleep(5)

def fetch_ip_adresses(data=None):
    data=''
    while((data)==''):
        list_of_clients.clear()
        data = sock_ssl.recv(2048).decode("utf-8")
        if len(data) > 1:
            print (data)
            print(len(data))
            ips = data.strip().split(',')
            print(ips)
            if len(ips) > 0:
                for ip in ips:
                    if len(ip) > 0:
                        client = {'name': ip.split(':')[1], 'ip_address': ip.split(':')[0]}
                        if ' ' not in client['name']:
                            list_of_clients.append(client)

            logger.info(f'Current list of clients: {(list_of_clients)}')

server_thread = threading.Thread(target=connect_to_server, args=(client_name,))
server_thread.start()
time.sleep(10)
pong_thread = threading.Thread(target=pong)
ping_thread = threading.Thread(target=ping)
ping_thread.start()
pong_thread.start()
