import random

#coder une string avec la clé et renvoyer des bytes pret a etre envoyé sur le réseau
def code_str(str,cle):
    asc = [ord(c) for c in str]
    asc = [l ^ cle for l in asc]
    return bytes(asc)

#decoder une string via la clé sous forme de bytes
def decode_str(strInt,cle):
    conv = list(strInt)
    asc = [l ^ cle for l in conv]
    return ( ''.join([chr(i) for i in asc]))

def echange_cle_client(client_socket):
    #generer une clé aleatoire partager de 16 bits et une clé temporaire de 16 bits aussi
    cle_p = random.getrandbits(8)
    cle_temp = random.getrandbits(8)

    #on crypte notre clé partagé
    m = cle_p ^ cle_temp

    # Convertir en chaîne de caractères et encoder en UTF-8
    data = str(m).encode('utf-8')

    # Envoyer via le socket
    client_socket.sendall(data)

    #on recoi du serveur, on decrypte et on renvoi
    msg_c = client_socket.recv(1024)
    msg_c = int(msg_c.decode('utf-8'))

    m2 = msg_c ^ cle_temp
    # Convertir en chaîne de caractères et encoder en UTF-8
    data = str(m2).encode('utf-8')

    # Envoyer via le socket
    client_socket.sendall(data)
    print(cle_p)
    return cle_p

def echange_cle_serveur(conn):
    #on genere notre cle_temp
    cle_temp = random.getrandbits(8)
    #on recoi la le chiffre
    data = conn.recv(1024)
    print("on a received")
    data = int(data.decode('utf-8'))


    #on rechiffre et on renvoi
    m = data ^ cle_temp
    data = str(m).encode('utf-8')
    conn.sendall(data)

    #on attend la reponse et on dechiffre la cle partagé
    data = conn.recv(1024)
    m = int(data.decode('utf-8'))
    cle_p = m ^ cle_temp

    print(cle_p)
    return cle_p