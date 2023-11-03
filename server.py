import socket
from datetime import datetime
import random

QUEUE_LEN = 1
REQUEST_LEN = 4
SERVER_NAME = 'the yoyo server'

IP = '127.0.0.1'
PORT = 8000


def request_to_response(request):
    if request == 'TIME':
        now = datetime.now()
        return str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second).zfill(2)

    elif request == 'NAME':
        return SERVER_NAME

    elif request == 'RAND':
        return str(random.randint(1, 10))

    elif request == 'EXIT':
        return 'Exiting.'

    else:
        return 'Invalid command.'


def connect_socket(server_socket):
    server_socket.bind((IP, PORT))
    server_socket.listen(QUEUE_LEN)


def connect_to_client(server_socket):
    print('Waiting for client to connect...')
    client_socket, client_addr = server_socket.accept()
    return client_socket


def format_response(response):
    return str(len(response)).zfill(2) + response


def main_loop(client_socket):
    while True:
        request = client_socket.recv(REQUEST_LEN).decode()

        response = request_to_response(request)
        response = format_response(response)

        client_socket.send(response.encode())

        if 'Exiting.' in response:
            client_socket.close()
            print('Client disconnected.')
            break


def client_socket_loop(server_socket):
    # when closing client socket, wait until another client connects
    while True:
        client_socket = connect_to_client(server_socket)

        try:
            print('Client connected!')
            main_loop(client_socket)

        except socket.error as err:
            print('client socket error: ' + str(err))

        finally:
            client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        connect_socket(server_socket)
        client_socket_loop(server_socket)

    except socket.error as err:
        print('server socket error: ' + str(err))

    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
