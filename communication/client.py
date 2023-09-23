import socket
import json

# Server ip: 84.105.126.31
# Gopi ip: 84.105.39.48
HOST = "84.105.126.31"  # The server's hostname or IP address
PORT = 5050  # The port used by the server
with open("settings.json") as file:
    settings = json.load(file)

Sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Try connection, if not possible continue.
# This should become a lifecycle, where the connection would be checked and reinstantiated if False.
# TODO
# Should debate becoming threaded so it doesn't block GUI from running.
is_updating = False
def establish_connection():
    global is_updating
    if is_updating: return
    else:
        is_updating = True
        try: Sendsocket.connect((HOST, PORT))
        except:
            print("Could not connect to servers.")
            is_updating = False


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


def encoder(keys:[int, int], message: str) -> list:
    """Encodes a string into a list of encrypted ascii numbers using a public key and an additional number."""
    encoded = []
    # Calling the encrypting function in encoding function
    for letter in message:
        encoded.append(encrypt([keys[0], keys[1]], ord(letter)))
    return encoded


def login(user:str = "", password:str = "", remember:bool = False) -> bool:
    """Attempts a login"""
    global settings
    if settings["remember_me"] == True:
        try: 
            encoded = f"{settings['encpass']}".replace(" ", "")
            Sendsocket.sendall(f"func->list login(\"{settings['user']}\",{encoded},True)".encode("UTF-8"))
            settings["encpass"] = [int(i) for i in receive().split(",")]
            with open("settings.json", 'w') as file:
                json.dump(settings, file)
            return True

        except:
            settings["remember_me"] = False
            with open("settings.json", 'w') as file:
                json.dump(settings, file)
            raise ValueError("Remembered username and/or password is incorrect")
    
    else:
        Sendsocket.sendall(f"func->list request_key(\"{user}\")".encode('UTF-8'))
        try: keys = [int(i) for i in receive().split(",")]
        except ValueError: return False
        encoded = f"{encoder(keys,password)!r}".replace(" ", "")

        if remember == True:
            Sendsocket.sendall(f"func->list login(\"{user}\",{encoded},True)".encode("UTF-8"))
            try:
                settings["encpass"] = [int(i) for i in receive().split(",")]
                settings["user"] = user
                settings["remember_me"] = True
                with open("settings.json", 'w') as file:
                    json.dump(settings, file)
                return True
            except: return False
        else:
            Sendsocket.sendall(f"func->nonit login(\"{user}\",{encoded})".encode("UTF-8"))
            if receive() == "True":
                return True
            return False


def adminlogin():
    """Sets Loggedin variable to true without needing a proper login."""

    global Loggedin
    Loggedin = True


def create_account(User, Pass) -> bool:
    """Creates a new user account and adds it to userpass.json"""
    Sendsocket.sendall(f"func->None create_account(\"{User}\",\"{Pass}\")".encode('UTF-8'))
    # TODO
    # Make the server check for the username in userpass.json.
    # If username is in userpass.json the server should return False.
    # Otherwise return True, so it should be "return serverpackage".

    

    return False