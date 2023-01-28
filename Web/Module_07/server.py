import socket
from concurrent.futures import ThreadPoolExecutor


host = socket.gethostname()
port = 5000
message = 'OK'


def run_server(host_, port_):

    def handle(sock: socket.socket, address: str):
        print(f'Connection established {address}')

        while True:
            received = sock.recv(1024)
            if not received:
                break
            data = received.decode()
            print(f'Data received: {data}')
            sock.send(message.encode())
        print(f'Socket connection closed {address}')
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_, port_))
    server_socket.listen(2)

    with ThreadPoolExecutor(2) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f'Destroy server')
        finally:
            server_socket.close()


if __name__ == '__main__':
    run_server(host, port)
