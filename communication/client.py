import communication.server

User="Gopi"
Pass="!Walls4balls"
Loggedin=False

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
    Loggedin = communication.server.login(User, encoder(communication.server.reqkey(User), Pass))
    if not Loggedin: raise ValueError("Password or username was incorrect.")
    return True

def adminlogin():
    """Sets Loggedin variable to true without needing a proper login."""

    global Loggedin
    Loggedin = True

    
if __name__ == "__main__":
    communication.server.createacc(User, Pass)
    login(User, Pass)
    print(Loggedin)