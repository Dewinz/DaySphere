import socket

# Server ip: 84.105.126.31
# Gopi ip: 84.105.39.48
HOST = "84.105.126.31"  # The server's hostname or IP address
PORT = 5050  # The port used by the server

User="Gopi"
Pass="!Walls4balls"
Loggedin=False

Sendsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Sendsocket.connect((HOST, PORT))

def receive():
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

def login(User:str, Pass:str) -> bool:
    """Attempts a login"""

    global Loggedin
    try:
        Sendsocket.sendall(f"func->list reqkey(\"{User}\")".encode('UTF-8'))
        keys = [int(receive()), int(receive())]

        encoded = f"{encoder(keys,Pass)!r}".replace(" ", "")

        Sendsocket.sendall(f"func->nonit login(\"{User}\",{encoded})".encode("UTF-8"))
        Loggedin = receive() == "True"
        print(Loggedin)
    except:
        pass

    if not Loggedin: raise ValueError("Password or username was incorrect.")
    return True

def adminlogin():
    """Sets Loggedin variable to true without needing a proper login."""

    global Loggedin
    Loggedin = True

def create_account(User, Pass):
    """Creates a new user account and adds it to userpass.json"""

    Sendsocket.sendall(f"func->None createacc(\"{User}\",\"{Pass}\")".encode('UTF-8'))

if __name__ == "__main__":
    login(User, Pass)
    print(f"Loggedin {Loggedin!r}")
    Sendsocket.sendall(b"close")