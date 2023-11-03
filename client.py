import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.connect(('127.0.0.1', 8000))

    while True:
        server_socket.send(input('> ').encode())
        byte_count = int(server_socket.recv(2).decode())
        response = server_socket.recv(byte_count).decode()
        print(response)
        if response == 'Exiting.':
            break

except socket.error as err:
    print(str(err))

finally:
    server_socket.close()
