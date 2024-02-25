from socket import socket, AF_INET, SOCK_STREAM
from json import dump, dumps, load, loads

# Server ip: 84.105.126.31
# Gopi ip: 84.105.39.48
settings = load(open("settings.json"))

def establish_connection():
    global connection_socket
    connection_socket = socket(AF_INET, SOCK_STREAM)
    connection_socket.connect((settings["host"], settings["port"]))

def receive():
    """Returns recieved messages from the server."""
    return loads(connection_socket.recv(1024).decode("UTF-8"))

def close_program():
    global connection_socket
    try:
        connection_socket.sendall(b"close")
        connection_socket.close()
    except: pass


def encoder(keys:list[int, int], message: str) -> list:
    """Encodes a string into a list of encrypted ascii numbers using a public key and an additional number."""

    def encrypt(keys:list[int, int], message:int|float) -> int:
        """Encrypts a number using a public key and an additional number."""

        encrypted_text = 1
        while keys[0] > 0:
            encrypted_text *= message
            encrypted_text %= keys[1]
            keys[0] -= 1
        return encrypted_text
    
    encoded = []
    # Calling the encrypting function in encoding function
    for letter in message:
        encoded.append(encrypt([keys[0], keys[1]], ord(letter)))
    return encoded

def login(user:str = "", password:str = "", remember:bool = False) -> bool:
    """Attempts a login"""
    global settings
    if settings["remember_me"] == True:
        encoded = settings['encpass']
        user = settings["user"]
        remember=True

    else:
        connection_socket.sendall(f"func->Any\nrequest_key\n{dumps(user)}".encode('UTF-8'))
        try: keys = list(map(int, receive()))
        except ValueError: return False
        encoded = encoder(keys,password)

    connection_socket.sendall(f"func->Any\nlogin\n{dumps(user)}\n{dumps(encoded)}\n{dumps(remember)}".encode("UTF-8"))
    reply = receive()
    if reply == True: return True
    try:
        settings["encpass"] = list(map(int, reply))
        settings["user"] = user
        settings["remember_me"] = True
        dump(settings, open("settings.json", 'w'))
        return True
    except: 
        settings["remember_me"] = False
        dump(settings, open("settings.json", 'w'))
        return False

def logout():
    # If we logout from the server the settings variable on the server doesn't get changed. For now this isn't an issue since it's only ever used right after
    # the initialization and never dumped. If it's changed so that it is dumped somewhere else in the code this could cause an issue where remembered switches
    # back to true when it shouldn't. Simple fix is to change the variable in the main.py as well as calling this function when logging out.
    global settings
    settings["remember_me"] = False
    settings["encpass"] = []
    settings["user"] = ""
    dump(settings, open("settings.json", 'w'))
    connection_socket.sendall(f"func->None\nlogout".encode('UTF-8'))

def create_account(User, Pass, remembered) -> bool:
    """Creates a new user account and adds it to userpass.json"""
    connection_socket.sendall(f"func->Any\ncreate_account\n{dumps(User)}\n{dumps(Pass)}\n{dumps(remembered)}".encode('UTF-8'))
    reply = receive()
    if reply == True: return True
    try:
        settings["encpass"] = list(map(int, reply))
        settings["user"] = User
        settings["remember_me"] = True
        dump(settings, open("settings.json", 'w'))
        return True
    except: return False

def save_data(data, datatype:str) -> None:
    connection_socket.sendall(f"func->None\nsave_data\n{dumps(data)}\n{dumps(datatype)}".encode('UTF-8'))

def request_data(datatype:str):
    connection_socket.sendall(f"func->Any\nrequest_data\n{dumps(datatype)}".encode('UTF-8'))
    return receive()