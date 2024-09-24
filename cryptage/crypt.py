import random

# Encode a string using the key and return bytes ready to be sent over the network
def code_str(string, key):
    asc = [ord(c) for c in string]
    asc = [l ^ key for l in asc]
    return bytes(asc)

# Decode a string using the key from the received bytes
def decode_str(strInt, key):
    conv = list(strInt)
    asc = [l ^ key for l in conv]
    return ''.join([chr(i) for i in asc])

# Client-side key exchange function
def echange_cle_client(client_socket):
    try:
        # Generate a shared key and a temporary key (both 8 bits)
        cle_p = random.getrandbits(8)
        cle_temp = random.getrandbits(8)

        # Encrypt the shared key with the temporary key
        m = cle_p ^ cle_temp

        # Send the encrypted key to the server
        data = str(m).encode('utf-8')
        client_socket.sendall(data)

        # Receive the server's response and decrypt it
        msg_c = client_socket.recv(1024)
        msg_c = int(msg_c.decode('utf-8'))

        # Decrypt the received message
        m2 = msg_c ^ cle_temp

        # Send the final verification response
        data = str(m2).encode('utf-8')
        client_socket.sendall(data)

        return cle_p
    except socket.error as e:
        print(f"Socket error during key exchange: {e}")
    except Exception as e:
        print(f"An error occurred during key exchange: {e}")
    finally:
        # Always ensure the socket is closed in case of failure (optional depending on context)
        print("Client-side key exchange complete.")


# Server-side key exchange function
def echange_cle_serveur(conn):
    try:
        # Generate a temporary key (8 bits)
        cle_temp = random.getrandbits(8)

        # Receive the encrypted message from the client
        data = conn.recv(1024)
        if not data:
            raise ConnectionError("No data received during key exchange.")
        data = int(data.decode('utf-8'))

        # Re-encrypt and send the data back to the client
        m = data ^ cle_temp
        data = str(m).encode('utf-8')
        conn.sendall(data)

        # Receive the final decrypted key and calculate the shared key
        data = conn.recv(1024)
        if not data:
            raise ConnectionError("No data received during final key exchange.")
        m = int(data.decode('utf-8'))
        cle_p = m ^ cle_temp

        return cle_p
    except socket.error as e:
        print(f"Socket error during key exchange: {e}")
    except Exception as e:
        print(f"An error occurred during key exchange: {e}")
    finally:
        # Always ensure the socket is closed in case of failure (optional depending on context)
        print("Server-side key exchange complete.")

