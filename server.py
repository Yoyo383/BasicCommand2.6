import socket
from datetime import datetime
import random

QUEUE_LEN = 1
REQUEST_LEN = 4
SERVER_NAME = 'the yoyo server'
IP = '127.0.0.1'
PORT = 8000


def return_time():
    """
    Returns current date and time without milliseconds.
    :return: Current date and time without milliseconds.
    :rtype: str
    """
    now = datetime.now()
    # return str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second).zfill(2)
    return str(now).split('.')[0]


def return_name():
    """
    Returns the server name.
    :return: The server name.
    :rtype: str
    """
    return SERVER_NAME


def return_rand():
    """
    Returns a random number between 1 and 10.
    :return: A random number between 1 and 10.
    :rtype: int
    """
    return random.randint(1, 10)


def request_to_response(request):
    """
    Gets the request and returns the proper response.
    :param request: The request.
    :type request: str
    :return: The proper response.
    :rtype: str
    """
    if request == 'TIME':
        return return_time()

    elif request == 'NAME':
        return return_name()

    elif request == 'RAND':
        return str(return_rand())

    elif request == 'EXIT':
        return 'Exiting.'

    else:
        return 'Invalid command.'


def connect_socket(server_socket):
    """
    Binds and connects the socket.
    :param server_socket: The socket.
    :type server_socket: socket.socket
    :return: None.
    """
    server_socket.bind((IP, PORT))
    server_socket.listen(QUEUE_LEN)


def connect_to_client(server_socket):
    """
    Waits for client to connect and returns the socket.
    :param server_socket: The server socket.
    :type server_socket: socket.socket
    :return: The client socket.
    :rtype: socket.socket
    """
    print('Waiting for client to connect...')
    client_socket, client_addr = server_socket.accept()
    return client_socket


def protocolize_content(content):
    """
    Protocolizes the content as the following: the number of bytes, followed by a $ and then the content.
    :param content: The content.
    :type content: str
    :return: The message to send.
    :rtype: str
    """
    return str(len(content)) + '$' + content


def main_loop(client_socket):
    """
    The loop where the socket waits for a request, gets the proper response, and sends it. If the request is EXIT,
    the socket closes
    :param client_socket: The client socket.
    :type client_socket: socket.socket
    :return: None.
    """
    req = ''
    while req != 'EXIT':
        req = client_socket.recv(REQUEST_LEN).decode()

        response = request_to_response(req)
        message = protocolize_content(response)

        client_socket.send(message.encode())

    client_socket.close()
    print('Client disconnected.')


def connect_client_loop(server_socket):
    """
    The server waits for a client and does the main loop. When the client disconnects, the server waits for another one.
    :param server_socket: The server socket.
    :type server_socket: socket.socket
    :return: None.
    """
    while True:
        client_socket = connect_to_client(server_socket)

        try:
            print('Client connected!')
            main_loop(client_socket)

        except socket.error as err:
            print('Client socket error: ' + str(err))

        except KeyboardInterrupt:
            print('Keyboard interrupt detected, exiting.')
            client_socket.send(protocolize_content('Server has closed, disconnecting.').encode())
            client_socket.close()
            break

        finally:
            client_socket.close()


def main():
    """
    The main function.
    :return: None.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        connect_socket(server_socket)
        connect_client_loop(server_socket)

    except socket.error as err:
        print('Server socket error: ' + str(err))

    except KeyboardInterrupt:
        print('Keyboard interrupt detected, exiting.')

    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
