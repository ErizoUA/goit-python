import socket

host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 5000


def run_client(ip_: str, port_: int):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server = ip_, port_
        sock.connect(server)
        print(f'Connection established {server}')

        try:
            message = input("input message: ")

            sock.send(message.encode())

            response = sock.recv(1024)
            print(f'Response data: {response.decode()}')

        except KeyboardInterrupt:
            print("Destroy server")

    print(f'Data transfer completed')


if __name__ == '__main__':
    run_client(ip, port)
