import socket
from threading import Thread
import select
import utils


class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))
        self.input_stream = self.client_socket.makefile('r')
        self.output_stream = self.client_socket.makefile('w')

    def download_file(self):
        # Receive list of available files for download from server
        available_files = self.input_stream.readline().strip()
        print(available_files)

        choice = input('Entrez le nom du fichier pour télécharger: ')
        self.output_stream.write(choice + '\n')
        self.output_stream.flush()

        # Receive Huffman coding table and compressed file from server
        huffman_table = eval(self.input_stream.readline().strip())
        compressed_file = self.input_stream.readline().strip()

        # Use Huffman coding table and compressed file to decode
        huffman = utils.Huffman('')
        decoded_text = huffman.decoder_huffman(compressed_file, huffman_table)
        print("Texte décompressé:", decoded_text)

    def close_connection(self):
        self.client_socket.close()


if __name__ == '__main__':
    # Create a client and connect to the server
    client = Client('localhost', 12345)
    client.connect_to_server()
    client.download_file()
    client.close_connection()
