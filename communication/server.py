from random import randint
from math import gcd
import json
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 25565
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def primefiller():
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
 
def pickrandomprime():
    """Picking a random prime number and erasing that prime number from list because p!=q."""
    prime = primefiller()
    k = randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)
 
    ret = next(it)
    prime.remove(ret)
    return ret
 
 
def setkeys():
    """Set the keys for the RSA encryption algorhithm
    See documentation on algorithm here: https://www.geeksforgeeks.org/rsa-algorithm-cryptography/."""

    prime1 = pickrandomprime()  # First prime number
    prime2 = pickrandomprime()  # Second prime number
 
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

def createacc(User:str, Pass:str):
    """Adds a new account to userpass.json."""

    with open('userpass.json') as file:
        userpass = json.load(file)
    keys = list(setkeys())
    keys.append(Pass)
    userpass[User] = keys
    with open('userpass.json', "w") as file:
        json.dump(userpass, file)

def reqkey(User:str) -> [int, int]:
    """Function to request a public key and additional number."""

    with open('userpass.json') as file:
        userpass = json.load(file)
    try: return userpass[User][1:3:1]
    except KeyError: return KeyError

def login(User:str, encpass:list) -> bool:
    """Attempts a login."""
    
    with open('userpass.json') as file:
        userpass = json.load(file)
    
    try: return decoder(userpass[User][0:3:2], encpass) == userpass[User][3]
    except: return False



s.bind((HOST, PORT))
s.listen()
print(f"Listening on ip: {HOST}:{PORT}")
conn, addr = s.accept()
with conn:
    while True:
        data = conn.recv(1024).decode('UTF-8')
        if data:
            print(data)
            datal = data.split(" ")
            match datal[0]:
                case "func->list":
                    exec (f"try: [conn.sendall(str(i).encode(\"UTF-8\")) for i in {datal[1]}]\nexcept: conn.sendall(str({datal[1]}).encode(\"UTF-8\"))")
                case "func->nonit":
                    exec ("conn.sendall(str({}).encode(\"UTF-8\"))".format(datal[1]))
                case "func->None":
                    exec (datal[1])
                case "close":
                    s.close
                    break