import socket
import threading
import random
from cryptage.crypt import echange_cle_client, decode_str, code_str, echange_cle_serveur



# Fonction pour recevoir des messages en continu depuis le serveur
def receive_messages(client_socket,cle_p):
    while True:
        try:
            # On essaie de recevoir des données du serveur
            data = client_socket.recv(1024)
            if data:
                data = decode_str(data,cle_p)
                print(f"\nServer: {data}")
            else:
                # Si aucune donnée reçue, on peut penser que la connexion est fermée
                print("Connection closed by server.")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# Fonction principale pour le client
def client_program():
    ip_server = '127.0.0.1'  # Adresse du serveur
    port_server = 1111       # Port du serveur

    # Créer un socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connexion au serveur
    client_socket.connect((ip_server, port_server))
    print("Connected to the server.")

    #juste apres la connexion il faut des echange en dur qui vont permette le cryptage de la conversation
############################################# ECHANGE DE CLE ####################################################

    cle_p = echange_cle_client(client_socket)

############################################# ECHANGE DE CLE ####################################################

    # Démarrer un thread pour recevoir les messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,cle_p,))
    receive_thread.daemon = True  # Le thread se termine automatiquement lorsque le programme principal se termine
    receive_thread.start()

    

    # Boucle pour envoyer des messages au serveur
    try:
        while True:
            message = input("You: ")  # Entrer un message via le clavier
            if message.lower() == 'quit':
                break  # Quitter la boucle si l'utilisateur tape 'quit'
            msg = code_str(message,cle_p)
            client_socket.sendall(msg)#.encode('utf-8'))  # Envoyer le message au serveur
    except KeyboardInterrupt:
        print("\nClient disconnected.")
    finally:
        client_socket.close()  # Fermer le socket proprement

# Démarrer le client
client_program()



