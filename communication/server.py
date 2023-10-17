from random import randint
from math import gcd
import json
import socket
import threading
import _thread

# Server host ip: 192.168.178.2
# Default host ip: socket.gethostbyname(socket.gethostname())

HOST = socket.gethostbyname(socket.gethostname())
PORT = 25565
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
userpass = json.load(open('userpass.json'))

def prime_filler():
    """Returns a set filled with prime numbers. May replace since it doesn't quite work the way i want it to."""
    # A set will be the collection of prime numbers,
    # where we can select random primes p and q
    prime = set()

    # Method used to fill the primes set is Sieve of
    # Eratosthenes (a method to collect prime numbers)
    # No idea how it works but it just adds prime numbers to a set
    seive = [True] * 250
    seive[0] = False
    seive[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            seive[j] = False
 
    # Filling the prime numbers
    for i in range(len(seive)):
        if seive[i]:
            prime.add(i)
    
    return prime
 
def pick_random_prime():
    """Picking a random prime number and erasing that prime number from list because p!=q."""
    prime = prime_filler()
    k = randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)
 
    ret = next(it)
    prime.remove(ret)
    return ret
 
 
def set_keys():
    """Set the keys for the RSA encryption algorhithm
    See documentation on algorithm here: https://www.geeksforgeeks.org/rsa-algorithm-cryptography/."""

    prime1 = pick_random_prime()  # First prime number
    prime2 = pick_random_prime()  # Second prime number
 
    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)
 
    public_key = 2
    while True:
        if gcd(public_key, fi) == 1:
            break
        public_key += 1
 
    # d = (k*Φ(n) + 1) / e for some integer k
 
    private_key = 2
    while True:
        if (private_key * public_key) % fi == 1:
            break
        private_key += 1

    return private_key, public_key, n


def decrypt(keys:[int, int], encrypted_number:int|float):
    """Decrypts an encrypted integer/float using a private key and additional number."""

    decrypted = 1
    while keys[0] > 0:
        decrypted *= encrypted_number
        decrypted %= keys[1]
        keys[0] -= 1
    return decrypted
 
def decoder(keys:[int, int], encoded_text:list):
    """Decodes a list of encrypted ascii numbers of letters using a private key and an additional number."""

    s = ''
    # Calling the decrypting function decoding function
    for num in encoded_text:
        s += chr(decrypt([keys[0], keys[1]], num))
    return s

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

def create_account(User:str, Pass:str):
    """Adds a new account to userpass.json."""

    global userpass
    try: userpass[User]
    except KeyError:
        keys = list(set_keys())
        keys.append(Pass)
        userpass[User] = keys
        with open('userpass.json', "w") as file:
            json.dump(userpass, file)

def request_key(User:str) -> [int, int]:
    """Function to request a public key and additional number."""

    global userpass
    try: return userpass[User][1:3:1]
    except KeyError: return KeyError

def login(User:str, encpass:list, remembered:bool=False) -> bool:
    """Attempts a login."""
    
    global userpass
    password = userpass[User][3]
    try:
        if decoder(userpass[User][0:3:2], encpass) == password:
            #  TODO Can't update userpass why? Completely blocks the code from running.
            userpass[User] = list(set_keys()) + [password]
            with open('userpass.json', "w") as file:
                json.dump(userpass, file)
            if remembered == True:
                reencpass = encoder(userpass[User][1:3:1], password)
                return reencpass
            else: return True
        else: return False
    except: return False

def Main():
    global s
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on ip: {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}. There are currently {threading.active_count()} connection(s).")
        _thread.start_new_thread(receive_messages, (conn,))
        
    

def receive_messages(conn:socket.socket):
    resultdic = {}
    while True:
        data = conn.recv(1024).decode('UTF-8')
        if data:
            print(data)
            datal = data.split(" ")
            exec ("result = "+datal[1], None, resultdic)
            try: result=resultdic["result"]
            except: pass
            resultdic = {}
            match datal[0]:
                case "func->list":
                    conn.sendall((f"{result!r}".replace(" ", "").replace("[", "").replace("]", "")).encode("UTF-8"))
                case "func->nonit":
                    conn.sendall((str(result)).encode("UTF-8"))
                case "func->None":
                    pass
                case "close":
                    s.close
                    break
                
if __name__ == "__main__":
    Main()