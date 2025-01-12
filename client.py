import socket
import threading
import time

# Constants
MAGIC_COOKIE = b'\xabcddcba'  # Corrected byte sequence used to identify the protocol
SERVER_IP = '127.0.0.1'  # Localhost IP address (same computer)
SERVER_TCP_PORT = 9876  # TCP port number on which the server listens
SERVER_UDP_PORT = 1234  # UDP port number on which the server listens

# Function to handle TCP connection and file transfer
def tcp_transfer(file_size):
    """
    Establishes a TCP connection to the server, sends a request with the file size,
    and measures the time it takes to simulate a transfer.

    Args:
    file_size (int): The size of the file being transferred, in bytes.
    """
    # Create TCP socket and connect to server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((SERVER_IP, SERVER_TCP_PORT))

    # Send request to server: MAGIC_COOKIE + a request type (0x03)
    # Followed by the file size (8 bytes)
    tcp_socket.send(MAGIC_COOKIE + b'\x03')  # Send request acknowledgment
    tcp_socket.send(file_size.to_bytes(8, 'big') + b'\n')  # Send the file size

    # Simulate file transfer by receiving a response from the server
    start_time = time.time()  # Start the timer
    tcp_socket.recv(1024)  # Simulate data reception
    end_time = time.time()  # End the timer

    # Print the time taken for the TCP transfer
    print(f"TCP transfer finished, time: {end_time - start_time} seconds")
    tcp_socket.close()  # Close the socket after transfer is complete

# Function to handle UDP connection and file transfer
def udp_transfer(file_size):
    """
    Establishes a UDP connection to the server, sends a request with the file size,
    and measures the time it takes to simulate a transfer.

    Args:
    file_size (int): The size of the file being transferred, in bytes.
    """
    # Create UDP socket and connect to server
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.connect((SERVER_IP, SERVER_UDP_PORT))

    # Send request to server: MAGIC_COOKIE + a request type (0x03)
    # Followed by the file size (8 bytes)
    udp_socket.send(MAGIC_COOKIE + b'\x03')
    udp_socket.send(file_size.to_bytes(8, 'big'))

    # Simulate file transfer by receiving a response from the server
    start_time = time.time()  # Start the timer
    udp_socket.recv(1024)  # Simulate data reception
    end_time = time.time()  # End the timer

    # Print the time taken for the UDP transfer
    print(f"UDP transfer finished, time: {end_time - start_time} seconds")
    udp_socket.close()  # Close the socket after transfer is complete

# Function to handle both TCP and UDP connections in parallel
def handle_connections(file_size, tcp_count, udp_count):
    """
    Creates and manages multiple TCP and UDP connections to the server in parallel.
    Each connection sends a request with the specified file size.

    Args:
    file_size (int): The size of the file being transferred, in bytes.
    tcp_count (int): The number of parallel TCP connections to create.
    udp_count (int): The number of parallel UDP connections to create.
    """
    threads = []  # List to store all thread objects

    # Create TCP connections in parallel
    for _ in range(tcp_count):
        thread = threading.Thread(target=tcp_transfer, args=(file_size,))
        threads.append(thread)
        thread.start()  # Start each TCP transfer thread

    # Create UDP connections in parallel
    for _ in range(udp_count):
        thread = threading.Thread(target=udp_transfer, args=(file_size,))
        threads.append(thread)
        thread.start()  # Start each UDP transfer thread

    # Wait for all threads to finish before continuing
    for thread in threads:
        thread.join()

# Main function to start the program
def main():
    """
    The main function that prompts the user for file size, number of TCP connections,
    and number of UDP connections, then starts the transfer process.
    """
    # Get file size, number of TCP and UDP connections from the user
    file_size = int(input("Enter file size (in bytes): "))
    tcp_count = int(input("Enter number of TCP connections: "))
    udp_count = int(input("Enter number of UDP connections: "))

    print("Starting the transfers...")  # Notify the user that transfers are starting
    handle_connections(file_size, tcp_count, udp_count)  # Handle both TCP and UDP connections
    print("All transfers complete, listening for offers again...")  # Notify the user that all transfers are complete

# Entry point for the script
if __name__ == '__main__':
    main()  # Start the program execution
