from socket import socket, AF_INET, SOCK_STREAM
from json import dump, load

# Server ip: 84.105.126.31
# Gopi ip: 84.105.39.48
with open("settings.json") as file:
    settings = load(file)

def establish_connection():
    global Sendsocket
    Sendsocket = socket(AF_INET, SOCK_STREAM)
    Sendsocket.connect((settings["host"], settings["port"]))

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
        encoded = f"{settings['encpass']}".replace(" ", "")
        user = settings["user"]
        remember=True

    else:
        Sendsocket.sendall(f"func->list Accounts.request_key(\"{user}\")".encode('UTF-8'))
        try: keys = [int(i) for i in receive().split(",")]
        except ValueError: return False
        encoded = f"{encoder(keys,password)!r}".replace(" ", "")

    if remember == True:
        Sendsocket.sendall(f"func->list Accounts.login(\"{user}\",{encoded},True)".encode("UTF-8"))
        try:
            settings["encpass"] = [int(i) for i in receive().split(",")]
            settings["user"] = user
            settings["remember_me"] = True
            with open("settings.json", 'w') as file:
                dump(settings, file)
            return True
        except:
            settings["remember_me"] = False
            with open("settings.json", 'w') as file:
                dump(settings, file)
            return False
    else:
        Sendsocket.sendall(f"func->nonit Accounts.login(\"{user}\",{encoded})".encode("UTF-8"))
        if receive() == "True":
            return True
        return False

def logout():
     # If we logout from the server the settings variable on the server doesn't get changed. For now this isn't an issue since it's only ever used right after
     # the initialization and never dumped. If it's changed so that it is dumped somewhere else in the code this could cause an issue where remembered switches
     # back to true when it shouldn't. Simple fix is to change the variable in the main.py as well as calling this function when logging out.
    global settings
    settings["remember_me"] = False
    with open("settings.json", 'w') as file:
        dump(settings, file)

def close_program():
    global Sendsocket
    try:
        Sendsocket.sendall(b"close")
        Sendsocket.close()
    except: pass

def create_account(User, Pass, remembered) -> bool:
    """Creates a new user account and adds it to userpass.json"""
    if remembered == True:
        Sendsocket.sendall(f"func->list Accounts.create_account(\"{User}\",\"{Pass}\",{remembered})".encode('UTF-8'))
        try:
            settings["encpass"] = [int(i) for i in receive().split(",")]
            settings["user"] = User
            settings["remember_me"] = True
            with open("settings.json", 'w') as file:
                dump(settings, file)
            return True
        except:
            return False
    else:
        if receive() == "True": return True
        return False