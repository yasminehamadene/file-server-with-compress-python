

import os
import socket
from threading import Thread
import select
import utils


class Service:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.input_stream = client_socket.makefile('r')
        self.output_stream = client_socket.makefile('w')

    def handle_client(self):
        # Send list of available files for download
        available_files = ', '.join(os.listdir('.'))
        self.output_stream.write(f'Available files: {available_files}\n')
        self.output_stream.flush()

        # Wait for client's choice
        ready = select.select([self.input_stream], [], [])
        if ready[0]:
            choice = self.input_stream.readline().strip()
            file_path = os.path.join(os.getcwd(), choice)
            huffman = utils.Huffman(file_path)
            huffman.generate_huffman_list()
            huffman.generate_huffman_tree()
            huffman.coder()
            huffman_table = huffman._Huffman__huffman_dict
            compressed_text = huffman.coder_huffman(huffman.read_file(),huffman_table)
            self.output_stream.write(str(huffman_table) + '\n')
            self.output_stream.write(compressed_text + '\n')
            self.output_stream.flush()
        else:
            # Client did not respond within 10 seconds
            pass

        print("fermeture connexion")

        # Close connection with client
        self.client_socket.close()


def handle_client(client_socket):
    service = Service(client_socket)
    service.handle_client()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server running {}".format(12345))
    server_socket.bind(('localhost', 12345))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    start_server()
