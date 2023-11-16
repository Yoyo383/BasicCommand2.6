import socket

IP = '127.0.0.1'
PORT = 8000
COMMANDS = ['TIME', 'NAME', 'RAND', 'EXIT']

SERVER_CLOSED_MSG = 'Server has closed, disconnecting.'


def get_response(server_socket):
    """
    Gets the response from the server and extracts the content.
    :param server_socket: The socket.
    :type server_socket: socket.socket
    :return: The content of the response.
    :rtype: str
    """
    count = 0

    char = server_socket.recv(1).decode()
    while char != '$':
        count = count * 10 + int(char)
        char = server_socket.recv(1).decode()

    return server_socket.recv(count).decode()


def is_cmd_valid(cmd):
    """
    Checks if the entered command is valid.
    :param cmd: The command.
    :type cmd: str
    :return: Whether the command is valid.
    :rtype: bool
    """
    return cmd in COMMANDS


def main_loop(server_socket):
    """
    The user enters a command, if it's valid the client sends it and gets the response, then prints the response. If
    user enters EXIT, the client disconnects. Loops until user enters EXIT.
    :param server_socket: The socket.
    :type server_socket: socket.socket
    :return: None
    """
    req = ''
    while req != 'EXIT':
        print('Enter one of the following commands: TIME | NAME | RAND | EXIT')
        req = input('> ')

        if is_cmd_valid(req):
            server_socket.send(req.encode())

            response = get_response(server_socket)
            print(response)
            if response == SERVER_CLOSED_MSG:
                break
        else:
            print('Invalid command.')


def main():
    """
    The main function.
    :return: None.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.connect((IP, PORT))
        main_loop(server_socket)

    except socket.error as err:
        print('Socket error: ' + str(err))

    except KeyboardInterrupt:
        server_socket.send('EXIT'.encode())

    finally:
        server_socket.close()


if __name__ == '__main__':
    assert is_cmd_valid('TIME')
    assert is_cmd_valid('RAND')
    assert is_cmd_valid('NAME')
    assert is_cmd_valid('EXIT')
    assert not is_cmd_valid('I HAVE THE HIGH GROUND')
    main()
