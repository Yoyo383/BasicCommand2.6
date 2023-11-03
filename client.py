import socket

IP = '127.0.0.1'
PORT = 8000


def get_response(server_socket):
    byte_count = int(server_socket.recv(2).decode())
    return server_socket.recv(byte_count).decode()


def main_loop(server_socket):
    while True:
        server_socket.send(input('> ').encode())

        response = get_response(server_socket)
        print(response)

        if response == 'Exiting.':
            break


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.connect((IP, PORT))
        main_loop(server_socket)

    except socket.error as err:
        print(str(err))

    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
