import socket
import json

# Server ip: 84.105.126.31
# Gopi ip: 84.105.39.48
HOST = "84.105.126.31"  # The server's hostname or IP address
PORT = 5050  # The port used by the server


Sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Try connection, if not possible continue.
# This should become a lifecycle, where the connection would be checked and reinstantiated if False.
# TODO
# Should become threaded so it doesn't block GUI from running.
try: Sendsocket.connect((HOST, PORT))
except: print("Could not connect to server.")

Loggedin = False

def receive():
    """Returns recieved messages from the server."""
    return Sendsocket.recv(1024).decode("UTF-8")


def encrypt(keys:[int, int], message:int|float) -> int:
    """Encrypts a number using a public key and an additional number."""

    encrypted_text = 1
    while keys[0] > 0:
        encrypted_text *= message
        encrypted_text %= keys[1]
        keys[0] -= 1
    return encrypted_text


def save_remember_me(save):
    with open("settings.json", 'w') as file:
        json.dump({"remember_me": save}, file)


def encoder(keys:[int, int], message: str) -> list:
    """Encodes a string into a list of encrypted ascii numbers using a public key and an additional number."""
    encoded = []
    # Calling the encrypting function in encoding function
    for letter in message:
        encoded.append(encrypt([keys[0], keys[1]], ord(letter)))
    return encoded


def login(User:str, Pass:str) -> bool:
    """Attempts a login"""
    
    global Loggedin
    try:
        Sendsocket.sendall(f"func->list reqkey(\"{User}\")".encode('UTF-8'))
        keys = [int(receive()), int(receive())]

        encoded = f"{encoder(keys,Pass)!r}".replace(" ", "")

        Sendsocket.sendall(f"func->nonit login(\"{User}\",{encoded})".encode("UTF-8"))
        if receive() == "True":
            return True
        return False
    except:
        pass

    if not Loggedin:
        return False
    return True


def adminlogin():
    """Sets Loggedin variable to true without needing a proper login."""

    global Loggedin
    Loggedin = True


def create_account(User, Pass) -> bool:
    """Creates a new user account and adds it to userpass.json"""

    # TODO
    # Make the server check for the username in userpass.json.
    # If username is in userpass.json the server should return False.
    # Otherwise return True, so it should be "return serverpackage".

    

    return False