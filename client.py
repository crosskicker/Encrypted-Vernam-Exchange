import socket
import threading
import random
from cryptage.crypt import echange_cle_client, decode_str, code_str, echange_cle_serveur

# Function to continuously receive messages from the server
def receive_messages(client_socket, cle_p):
    while True:
        try:
            # Try to receive data from the server
            data = client_socket.recv(1024)
            if data:
                # Decode the received message
                data = decode_str(data, cle_p)
                print(f"\nServer: {data}")
            else:
                # Connection closed by the server
                print("Connection closed by server.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Main function for the client
def client_program():
    ip_server = '127.0.0.1'  # Server address
    port_server = 5656       # Server port

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((ip_server, port_server))
    print("Connected to the server.")

    # Perform the key exchange for encrypted communication
    cle_p = echange_cle_client(client_socket)

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, cle_p,))
    receive_thread.daemon = True  # The thread will exit when the main program exits
    receive_thread.start()

    # Loop to send messages to the server
    try:
        while True:
            message = input("You: ")  # Enter a message via keyboard
            if message.lower() == 'quit':
                break  # Exit if the user types 'quit'
            # Encrypt and send the message
            msg = code_str(message, cle_p)
            client_socket.sendall(msg)
    except KeyboardInterrupt:
        print("\nClient disconnected.")
    finally:
        # Properly close the socket
        client_socket.close()

# Start the client program
client_program()
