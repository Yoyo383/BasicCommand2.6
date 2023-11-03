import socket
from datetime import datetime
import random

QUEUE_LEN = 1
REQUEST_LEN = 4
SERVER_NAME = 'the worst server'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_response(req):
    if req == 'TIME':
        now = datetime.now()
        return str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second).zfill(2)
    elif req == 'NAME':
        return SERVER_NAME
    elif req == 'RAND':
        return str(random.randint(1, 10))
    elif req == 'EXIT':
        return 'Exiting.'
    else:
        return 'Invalid command.'


try:
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen(QUEUE_LEN)
    while True:
        print('Waiting for client to connect...')
        client_socket, client_addr = server_socket.accept()

        try:
            print('Client connected!')
            while True:
                request = client_socket.recv(REQUEST_LEN).decode()
                response = get_response(request)
                response = str(len(response)).zfill(2) + response
                client_socket.send(response.encode())
                if 'Exiting.' in response:
                    client_socket.close()
                    break

        except socket.error as err:
            print('client socket error: ' + str(err))

        finally:
            client_socket.close()

except socket.error as err:
    print('server socket error: ' + str(err))

finally:
    server_socket.close()
