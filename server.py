import socket
import threading
import struct

# Constants
SERVER_TCP_PORT = 9876  # Server's TCP port for incoming connections
SERVER_UDP_PORT = 1234  # Server's UDP port for listening to requests
MAGIC_COOKIE = b'\xabcddcba'  # Corrected byte sequence used to identify the protocol


# Helper function to handle client requests for both TCP and UDP
def handle_client_request(client_socket, addr, client_udp_port, file_size):
    """
    Handles both TCP and UDP file transfer for a given client. This function sends a request acknowledgment
    over TCP and then initiates a UDP transfer to the client.

    Args:
    client_socket (socket.socket): The TCP socket for communication with the client.
    addr (tuple): The address of the client (IP, port).
    client_udp_port (int): The UDP port of the client to send the data.
    file_size (int): The size of the file being transferred in bytes.
    """
    # TCP transfer
    print(f"TCP connection established with {addr}")
    client_socket.send(MAGIC_COOKIE + b'\x03')  # Send request acknowledgment to client
    client_socket.send(file_size.to_bytes(8, 'big') + b'\n')  # Send file size as a byte sequence
    client_socket.close()  # Close the TCP connection after sending the file size

    # UDP transfer
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.connect((addr[0], client_udp_port))  # Connect to client's UDP port
    udp_socket.send(MAGIC_COOKIE + b'\x03')  # Send request acknowledgment for UDP transfer
    udp_socket.send(file_size.to_bytes(8, 'big'))  # Send file size over UDP
    udp_socket.close()  # Close the UDP socket after sending the file size


# Function to listen for UDP requests and respond with offer message
def listen_for_requests():
    """
    Listens for incoming UDP requests from clients. When a request is received, the server responds
    with an offer message containing its UDP and TCP ports.

    This function runs in a separate thread to handle multiple UDP requests concurrently.
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', SERVER_UDP_PORT))  # Bind to the UDP port for listening to requests
    print(f"Server listening for UDP requests on port {SERVER_UDP_PORT}")

    while True:
        data, addr = udp_socket.recvfrom(1024)  # Receive data from clients
        if data.startswith(MAGIC_COOKIE):  # Check if data matches the MAGIC_COOKIE
            print(f"Received offer request from {addr}")
            # Prepare the offer message containing server's UDP and TCP ports
            offer_msg = MAGIC_COOKIE + b'\x02' + struct.pack("!H", SERVER_UDP_PORT) + struct.pack("!H", SERVER_TCP_PORT)
            udp_socket.sendto(offer_msg, addr)  # Send the offer message back to the client


# Main function to initialize the server and accept TCP connections
def main():
    """
    The main server function that listens for incoming TCP connections, accepts requests from clients,
    and initiates file transfers using both TCP and UDP connections.

    This function also starts the UDP request listener in a separate thread to handle UDP requests concurrently.
    """
    # Create and configure the TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', SERVER_TCP_PORT))  # Bind server to TCP port
    server_socket.listen(5)  # Set the server to listen for up to 5 incoming connections
    print(f"Server listening for TCP connections on port {SERVER_TCP_PORT}")

    # Start the UDP listener in a separate thread (daemon thread)
    threading.Thread(target=listen_for_requests, daemon=True).start()

    while True:
        # Accept incoming TCP connection requests
        client_socket, addr = server_socket.accept()
        print(f"Connection received from {addr}")

        # Receive file size information from the client
        file_size_bytes = client_socket.recv(8)  # Receive 8 bytes containing the file size
        file_size = int.from_bytes(file_size_bytes, 'big')  # Convert the received bytes to an integer (file size)

        # Handle the client request in a separate thread to allow multiple clients
        threading.Thread(target=handle_client_request, args=(client_socket, addr, SERVER_UDP_PORT, file_size)).start()


# Entry point for the script
if __name__ == '__main__':
    main()  # Start the server execution
