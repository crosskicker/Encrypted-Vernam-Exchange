import socket
import threading
import random
from cryptage.crypt import echange_cle_client, decode_str, code_str, echange_cle_serveur

# Function to continuously receive messages from the client
def receive_messages(conn, cle_p):
    while True:
        try:
            # Try to receive data from the client
            data = conn.recv(1024)
            if data:
                # Decode the received message
                data = decode_str(data, cle_p)
                print(f"\nClient: {data}")
            else:
                # Connection closed by the client
                print("Connection closed by client.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Create a server socket and bind it to localhost on port 1111
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5656))

server_socket.listen(5) 
conn, addr = server_socket.accept()

# Perform the key exchange with the client
cle_p = echange_cle_serveur(conn)

# Start a thread to receive messages from the client
receive_thread = threading.Thread(target=receive_messages, args=(conn, cle_p,))
receive_thread.daemon = True  # The thread will exit when the main program exits
receive_thread.start()

try:
    while True:
        message = input("You: ")  # Enter a message via keyboard
        if message.lower() == 'quit':
            break  # Exit the loop if the user types 'quit'
        # Encrypt and send the message to the client
        msg = code_str(message, cle_p)
        conn.sendall(msg)
except KeyboardInterrupt:
    print("\nServer disconnected.")
finally:
    # Properly close the socket
    conn.close()
